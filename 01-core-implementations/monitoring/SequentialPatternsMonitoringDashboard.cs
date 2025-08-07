// Sequential Patterns Performance Monitoring Dashboard
// Copyright (c) 2025 Bryan Roe
// Licensed under the MIT License

using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace SemanticKernel.Agents.Strategies.Selection.Monitoring
{
    /// <summary>
    /// Real-time performance monitoring dashboard for sequential patterns
    /// </summary>
    public class SequentialPatternsMonitoringDashboard
    {
        private readonly ILogger<SequentialPatternsMonitoringDashboard> _logger;
        private readonly ConcurrentDictionary<string, MetricCollector> _metricCollectors;
        private readonly Timer _reportingTimer;
        private readonly DashboardConfiguration _configuration;
        
        public event EventHandler<PerformanceAlertEventArgs>? PerformanceAlert;
        public event EventHandler<DashboardUpdateEventArgs>? DashboardUpdate;
        
        public SequentialPatternsMonitoringDashboard(
            ILogger<SequentialPatternsMonitoringDashboard> logger,
            DashboardConfiguration? configuration = null)
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            _configuration = configuration ?? new DashboardConfiguration();
            _metricCollectors = new ConcurrentDictionary<string, MetricCollector>();
            
            _reportingTimer = new Timer(
                GenerateReport, 
                null, 
                _configuration.ReportingIntervalMs, 
                _configuration.ReportingIntervalMs);
            
            _logger.LogInformation("Sequential Patterns Monitoring Dashboard initialized");
        }
        
        /// <summary>
        /// Start monitoring a specific strategy instance
        /// </summary>
        public void StartMonitoring(string strategyId, ISelectionStrategy strategy)
        {
            var collector = new MetricCollector(strategyId, _configuration);
            _metricCollectors.TryAdd(strategyId, collector);
            
            // Hook into strategy events if available
            if (strategy is ICachedSequentialSelectionStrategy cachedStrategy)
            {
                cachedStrategy.CacheHit += (sender, e) => collector.RecordCacheHit();
                cachedStrategy.CacheMiss += (sender, e) => collector.RecordCacheMiss();
            }
            
            if (strategy is IBatchSequentialSelectionStrategy batchStrategy)
            {
                batchStrategy.BatchProcessed += (sender, e) => collector.RecordBatchOperation(e.BatchSize, e.ProcessingTimeMs);
            }
            
            _logger.LogInformation("Started monitoring strategy: {StrategyId}", strategyId);
        }
        
        /// <summary>
        /// Stop monitoring a specific strategy instance
        /// </summary>
        public void StopMonitoring(string strategyId)
        {
            if (_metricCollectors.TryRemove(strategyId, out var collector))
            {
                collector.Dispose();
                _logger.LogInformation("Stopped monitoring strategy: {StrategyId}", strategyId);
            }
        }
        
        /// <summary>
        /// Record a selection operation for monitoring
        /// </summary>
        public void RecordSelection(string strategyId, TimeSpan selectionTime, bool success, int agentCount, int historyLength)
        {
            if (_metricCollectors.TryGetValue(strategyId, out var collector))
            {
                collector.RecordSelection(selectionTime, success, agentCount, historyLength);
                
                // Check for performance alerts
                CheckPerformanceThresholds(strategyId, collector);
            }
        }
        
        /// <summary>
        /// Get current dashboard data for all monitored strategies
        /// </summary>
        public DashboardData GetCurrentDashboardData()
        {
            var strategies = new List<StrategyMetrics>();
            
            foreach (var kvp in _metricCollectors)
            {
                var metrics = kvp.Value.GetCurrentMetrics();
                strategies.Add(new StrategyMetrics
                {
                    StrategyId = kvp.Key,
                    TotalOperations = metrics.TotalOperations,
                    SuccessfulOperations = metrics.SuccessfulOperations,
                    AverageResponseTime = metrics.AverageResponseTime,
                    OperationsPerSecond = metrics.OperationsPerSecond,
                    CacheHitRate = metrics.CacheHitRate,
                    ErrorRate = metrics.ErrorRate,
                    LastUpdateTime = metrics.LastUpdateTime
                });
            }
            
            return new DashboardData
            {
                Strategies = strategies,
                GeneratedAt = DateTime.UtcNow,
                TotalStrategiesMonitored = strategies.Count,
                OverallOperationsPerSecond = strategies.Sum(s => s.OperationsPerSecond),
                OverallSuccessRate = strategies.Count > 0 ? strategies.Average(s => s.SuccessfulOperations / (double)Math.Max(s.TotalOperations, 1)) : 0
            };
        }
        
        /// <summary>
        /// Export historical data for analysis
        /// </summary>
        public async Task<string> ExportHistoricalDataAsync(TimeSpan timeRange)
        {
            var endTime = DateTime.UtcNow;
            var startTime = endTime - timeRange;
            
            var exportData = new
            {
                ExportedAt = endTime,
                TimeRange = new { Start = startTime, End = endTime },
                Strategies = _metricCollectors.Select(kvp => new
                {
                    StrategyId = kvp.Key,
                    Metrics = kvp.Value.GetHistoricalMetrics(startTime, endTime)
                }).ToArray()
            };
            
            return JsonSerializer.Serialize(exportData, new JsonSerializerOptions 
            { 
                WriteIndented = true 
            });
        }
        
        private void GenerateReport(object? state)
        {
            try
            {
                var dashboardData = GetCurrentDashboardData();
                
                _logger.LogInformation(
                    "Performance Report - Strategies: {StrategyCount}, Total Ops/sec: {TotalOpsPerSec:F2}, Success Rate: {SuccessRate:P2}",
                    dashboardData.TotalStrategiesMonitored,
                    dashboardData.OverallOperationsPerSecond,
                    dashboardData.OverallSuccessRate);
                
                // Detailed per-strategy logging
                foreach (var strategy in dashboardData.Strategies)
                {
                    _logger.LogDebug(
                        "Strategy {StrategyId}: Ops/sec={OpsPerSec:F2}, Cache Hit Rate={CacheHitRate:P2}, Error Rate={ErrorRate:P2}",
                        strategy.StrategyId,
                        strategy.OperationsPerSecond,
                        strategy.CacheHitRate,
                        strategy.ErrorRate);
                }
                
                // Trigger dashboard update event
                DashboardUpdate?.Invoke(this, new DashboardUpdateEventArgs(dashboardData));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating performance report");
            }
        }
        
        private void CheckPerformanceThresholds(string strategyId, MetricCollector collector)
        {
            var metrics = collector.GetCurrentMetrics();
            var alerts = new List<PerformanceAlert>();
            
            // Check response time threshold
            if (metrics.AverageResponseTime.TotalMilliseconds > _configuration.ResponseTimeThresholdMs)
            {
                alerts.Add(new PerformanceAlert
                {
                    Type = AlertType.HighResponseTime,
                    Message = $"Average response time ({metrics.AverageResponseTime.TotalMilliseconds:F2}ms) exceeds threshold ({_configuration.ResponseTimeThresholdMs}ms)",
                    Severity = AlertSeverity.Warning,
                    Value = metrics.AverageResponseTime.TotalMilliseconds,
                    Threshold = _configuration.ResponseTimeThresholdMs
                });
            }
            
            // Check error rate threshold
            if (metrics.ErrorRate > _configuration.ErrorRateThreshold)
            {
                alerts.Add(new PerformanceAlert
                {
                    Type = AlertType.HighErrorRate,
                    Message = $"Error rate ({metrics.ErrorRate:P2}) exceeds threshold ({_configuration.ErrorRateThreshold:P2})",
                    Severity = AlertSeverity.Critical,
                    Value = metrics.ErrorRate,
                    Threshold = _configuration.ErrorRateThreshold
                });
            }
            
            // Check low throughput threshold
            if (metrics.OperationsPerSecond < _configuration.MinOperationsPerSecond)
            {
                alerts.Add(new PerformanceAlert
                {
                    Type = AlertType.LowThroughput,
                    Message = $"Operations per second ({metrics.OperationsPerSecond:F2}) below threshold ({_configuration.MinOperationsPerSecond})",
                    Severity = AlertSeverity.Warning,
                    Value = metrics.OperationsPerSecond,
                    Threshold = _configuration.MinOperationsPerSecond
                });
            }
            
            // Check cache hit rate for cached strategies
            if (metrics.CacheHitRate < _configuration.MinCacheHitRate && metrics.TotalCacheOperations > 100)
            {
                alerts.Add(new PerformanceAlert
                {
                    Type = AlertType.LowCacheHitRate,
                    Message = $"Cache hit rate ({metrics.CacheHitRate:P2}) below threshold ({_configuration.MinCacheHitRate:P2})",
                    Severity = AlertSeverity.Info,
                    Value = metrics.CacheHitRate,
                    Threshold = _configuration.MinCacheHitRate
                });
            }
            
            // Trigger alerts
            foreach (var alert in alerts)
            {
                _logger.LogWarning("Performance Alert for {StrategyId}: {Message}", strategyId, alert.Message);
                PerformanceAlert?.Invoke(this, new PerformanceAlertEventArgs(strategyId, alert));
            }
        }
        
        public void Dispose()
        {
            _reportingTimer?.Dispose();
            
            foreach (var collector in _metricCollectors.Values)
            {
                collector.Dispose();
            }
            
            _metricCollectors.Clear();
        }
    }
    
    /// <summary>
    /// Collects metrics for a specific strategy instance
    /// </summary>
    public class MetricCollector : IDisposable
    {
        private readonly string _strategyId;
        private readonly DashboardConfiguration _configuration;
        private readonly object _lock = new object();
        
        // Counters
        private long _totalOperations;
        private long _successfulOperations;
        private long _cacheHits;
        private long _cacheMisses;
        private long _totalBatchOperations;
        
        // Timing
        private readonly List<TimeSpan> _recentResponseTimes;
        private readonly List<DateTime> _operationTimestamps;
        
        // Historical data
        private readonly ConcurrentQueue<MetricSnapshot> _historicalSnapshots;
        
        public MetricCollector(string strategyId, DashboardConfiguration configuration)
        {
            _strategyId = strategyId;
            _configuration = configuration;
            _recentResponseTimes = new List<TimeSpan>();
            _operationTimestamps = new List<DateTime>();
            _historicalSnapshots = new ConcurrentQueue<MetricSnapshot>();
        }
        
        public void RecordSelection(TimeSpan responseTime, bool success, int agentCount, int historyLength)
        {
            lock (_lock)
            {
                Interlocked.Increment(ref _totalOperations);
                
                if (success)
                {
                    Interlocked.Increment(ref _successfulOperations);
                }
                
                _recentResponseTimes.Add(responseTime);
                _operationTimestamps.Add(DateTime.UtcNow);
                
                // Keep only recent data
                var cutoffTime = DateTime.UtcNow - TimeSpan.FromMinutes(_configuration.RecentDataWindowMinutes);
                
                while (_recentResponseTimes.Count > _configuration.MaxRecentSamples)
                {
                    _recentResponseTimes.RemoveAt(0);
                }
                
                while (_operationTimestamps.Count > 0 && _operationTimestamps[0] < cutoffTime)
                {
                    _operationTimestamps.RemoveAt(0);
                }
            }
        }
        
        public void RecordCacheHit()
        {
            Interlocked.Increment(ref _cacheHits);
        }
        
        public void RecordCacheMiss()
        {
            Interlocked.Increment(ref _cacheMisses);
        }
        
        public void RecordBatchOperation(int batchSize, double processingTimeMs)
        {
            Interlocked.Increment(ref _totalBatchOperations);
        }
        
        public CurrentMetrics GetCurrentMetrics()
        {
            lock (_lock)
            {
                var now = DateTime.UtcNow;
                var windowStart = now - TimeSpan.FromMinutes(_configuration.RecentDataWindowMinutes);
                
                var recentOperations = _operationTimestamps.Count(t => t >= windowStart);
                var operationsPerSecond = recentOperations / _configuration.RecentDataWindowMinutes / 60.0;
                
                var averageResponseTime = _recentResponseTimes.Count > 0 
                    ? TimeSpan.FromTicks((long)_recentResponseTimes.Average(t => t.Ticks))
                    : TimeSpan.Zero;
                
                var totalCacheOperations = _cacheHits + _cacheMisses;
                var cacheHitRate = totalCacheOperations > 0 ? (double)_cacheHits / totalCacheOperations : 0;
                
                var errorRate = _totalOperations > 0 ? 1.0 - ((double)_successfulOperations / _totalOperations) : 0;
                
                return new CurrentMetrics
                {
                    TotalOperations = _totalOperations,
                    SuccessfulOperations = _successfulOperations,
                    AverageResponseTime = averageResponseTime,
                    OperationsPerSecond = operationsPerSecond,
                    CacheHitRate = cacheHitRate,
                    ErrorRate = errorRate,
                    TotalCacheOperations = totalCacheOperations,
                    LastUpdateTime = now
                };
            }
        }
        
        public List<MetricSnapshot> GetHistoricalMetrics(DateTime startTime, DateTime endTime)
        {
            return _historicalSnapshots
                .Where(s => s.Timestamp >= startTime && s.Timestamp <= endTime)
                .OrderBy(s => s.Timestamp)
                .ToList();
        }
        
        public void Dispose()
        {
            // Cleanup resources if needed
        }
    }
    
    #region Data Models
    
    public class DashboardConfiguration
    {
        public int ReportingIntervalMs { get; set; } = 30000; // 30 seconds
        public int RecentDataWindowMinutes { get; set; } = 5;
        public int MaxRecentSamples { get; set; } = 1000;
        public double ResponseTimeThresholdMs { get; set; } = 1000;
        public double ErrorRateThreshold { get; set; } = 0.05; // 5%
        public double MinOperationsPerSecond { get; set; } = 1.0;
        public double MinCacheHitRate { get; set; } = 0.80; // 80%
    }
    
    public class DashboardData
    {
        public List<StrategyMetrics> Strategies { get; set; } = new();
        public DateTime GeneratedAt { get; set; }
        public int TotalStrategiesMonitored { get; set; }
        public double OverallOperationsPerSecond { get; set; }
        public double OverallSuccessRate { get; set; }
    }
    
    public class StrategyMetrics
    {
        public string StrategyId { get; set; } = string.Empty;
        public long TotalOperations { get; set; }
        public long SuccessfulOperations { get; set; }
        public TimeSpan AverageResponseTime { get; set; }
        public double OperationsPerSecond { get; set; }
        public double CacheHitRate { get; set; }
        public double ErrorRate { get; set; }
        public DateTime LastUpdateTime { get; set; }
    }
    
    public class CurrentMetrics
    {
        public long TotalOperations { get; set; }
        public long SuccessfulOperations { get; set; }
        public TimeSpan AverageResponseTime { get; set; }
        public double OperationsPerSecond { get; set; }
        public double CacheHitRate { get; set; }
        public double ErrorRate { get; set; }
        public long TotalCacheOperations { get; set; }
        public DateTime LastUpdateTime { get; set; }
    }
    
    public class MetricSnapshot
    {
        public DateTime Timestamp { get; set; }
        public long TotalOperations { get; set; }
        public double OperationsPerSecond { get; set; }
        public double AverageResponseTimeMs { get; set; }
        public double CacheHitRate { get; set; }
        public double ErrorRate { get; set; }
    }
    
    public class PerformanceAlert
    {
        public AlertType Type { get; set; }
        public string Message { get; set; } = string.Empty;
        public AlertSeverity Severity { get; set; }
        public double Value { get; set; }
        public double Threshold { get; set; }
    }
    
    public enum AlertType
    {
        HighResponseTime,
        HighErrorRate,
        LowThroughput,
        LowCacheHitRate
    }
    
    public enum AlertSeverity
    {
        Info,
        Warning,
        Critical
    }
    
    public class PerformanceAlertEventArgs : EventArgs
    {
        public string StrategyId { get; }
        public PerformanceAlert Alert { get; }
        
        public PerformanceAlertEventArgs(string strategyId, PerformanceAlert alert)
        {
            StrategyId = strategyId;
            Alert = alert;
        }
    }
    
    public class DashboardUpdateEventArgs : EventArgs
    {
        public DashboardData DashboardData { get; }
        
        public DashboardUpdateEventArgs(DashboardData dashboardData)
        {
            DashboardData = dashboardData;
        }
    }
    
    #endregion
    
    #region Strategy Interfaces
    
    public interface ICachedSequentialSelectionStrategy
    {
        event EventHandler CacheHit;
        event EventHandler CacheMiss;
    }
    
    public interface IBatchSequentialSelectionStrategy
    {
        event EventHandler<BatchProcessedEventArgs> BatchProcessed;
    }
    
    public class BatchProcessedEventArgs : EventArgs
    {
        public int BatchSize { get; }
        public double ProcessingTimeMs { get; }
        
        public BatchProcessedEventArgs(int batchSize, double processingTimeMs)
        {
            BatchSize = batchSize;
            ProcessingTimeMs = processingTimeMs;
        }
    }
    
    #endregion
}
