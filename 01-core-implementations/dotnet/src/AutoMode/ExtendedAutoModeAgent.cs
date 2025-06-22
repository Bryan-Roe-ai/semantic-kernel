// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Agents;
using System.Text.Json;
using System.Diagnostics;
using System.IO;

namespace SemanticKernel.AutoMode;

/// <summary>
/// Extended auto mode agent for ultra-long-term stability and autonomous operation.
/// Implements robust error handling, self-maintenance, and observability for months-long continuous operation.
/// </summary>
public class ExtendedAutoModeAgent : IDisposable
{
    private readonly ILogger<ExtendedAutoModeAgent> _logger;
    private readonly IConfiguration _configuration;
    private readonly Kernel _kernel;
    private readonly CancellationTokenSource _cancellationTokenSource;
    private readonly ConcurrentDictionary<string, object> _state;
    private readonly Timer _healthCheckTimer;
    private readonly Timer _maintenanceTimer;
    private readonly SemaphoreSlim _operationSemaphore;
    private readonly ExtendedAutoModeOptions _options;
    
    private bool _isRunning;
    private bool _disposed;
    private DateTime _lastHealthCheck;
    private DateTime _startTime;
    private int _operationCount;
    private int _errorCount;

    /// <summary>
    /// Initializes a new instance of the <see cref="ExtendedAutoModeAgent"/> class.
    /// </summary>
    /// <param name="kernel">The semantic kernel instance.</param>
    /// <param name="logger">Logger for diagnostics and monitoring.</param>
    /// <param name="configuration">Configuration settings.</param>
    /// <param name="options">Extended auto mode options.</param>
    public ExtendedAutoModeAgent(
        Kernel kernel,
        ILogger<ExtendedAutoModeAgent> logger,
        IConfiguration configuration,
        ExtendedAutoModeOptions? options = null)
    {
        _kernel = kernel ?? throw new ArgumentNullException(nameof(kernel));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _configuration = configuration ?? throw new ArgumentNullException(nameof(configuration));
        _options = options ?? new ExtendedAutoModeOptions();
        
        _cancellationTokenSource = new CancellationTokenSource();
        _state = new ConcurrentDictionary<string, object>();
        _operationSemaphore = new SemaphoreSlim(_options.MaxConcurrentOperations, _options.MaxConcurrentOperations);
        
        _startTime = DateTime.UtcNow;
        _lastHealthCheck = DateTime.UtcNow;
        
        // Initialize health check timer
        _healthCheckTimer = new Timer(
            PerformHealthCheck,
            null,
            TimeSpan.FromMinutes(1),
            TimeSpan.FromMinutes(_options.HealthCheckIntervalMinutes));
            
        // Initialize maintenance timer
        _maintenanceTimer = new Timer(
            PerformMaintenance,
            null,
            TimeSpan.FromHours(1),
            TimeSpan.FromHours(_options.MaintenanceIntervalHours));
            
        _logger.LogInformation("ExtendedAutoModeAgent initialized successfully");
    }

    /// <summary>
    /// Starts the extended auto mode operation.
    /// </summary>
    /// <param name="cancellationToken">Cancellation token for stopping the operation.</param>
    /// <returns>A task representing the asynchronous operation.</returns>
    public async Task StartAsync(CancellationToken cancellationToken = default)
    {
        if (_isRunning)
        {
            _logger.LogWarning("ExtendedAutoModeAgent is already running");
            return;
        }

        _logger.LogInformation("Starting ExtendedAutoModeAgent for long-term operation");
        
        try
        {
            _isRunning = true;
            
            // Initialize state
            await InitializeStateAsync(cancellationToken);
            
            // Start main operation loop
            await RunMainLoopAsync(cancellationToken);
        }
        catch (OperationCanceledException)
        {
            _logger.LogInformation("ExtendedAutoModeAgent operation was cancelled");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Critical error in ExtendedAutoModeAgent");
            throw;
        }
        finally
        {
            _isRunning = false;
            _logger.LogInformation("ExtendedAutoModeAgent stopped");
        }
    }

    /// <summary>
    /// Stops the extended auto mode operation gracefully.
    /// </summary>
    /// <returns>A task representing the asynchronous operation.</returns>
    public async Task StopAsync()
    {
        if (!_isRunning)
        {
            return;
        }

        _logger.LogInformation("Stopping ExtendedAutoModeAgent gracefully");
        
        _cancellationTokenSource.Cancel();
        
        // Wait for current operations to complete
        var timeout = TimeSpan.FromSeconds(30);
        var stopwatch = Stopwatch.StartNew();
        
        while (_isRunning && stopwatch.Elapsed < timeout)
        {
            await Task.Delay(100);
        }
        
        if (_isRunning)
        {
            _logger.LogWarning("ExtendedAutoModeAgent did not stop within timeout period");
        }
        
        await SaveStateAsync();
        _logger.LogInformation("ExtendedAutoModeAgent stopped successfully");
    }

    /// <summary>
    /// Gets the current status of the auto mode agent.
    /// </summary>
    /// <returns>Status information.</returns>
    public ExtendedAutoModeStatus GetStatus()
    {
        return new ExtendedAutoModeStatus
        {
            IsRunning = _isRunning,
            StartTime = _startTime,
            LastHealthCheck = _lastHealthCheck,
            OperationCount = _operationCount,
            ErrorCount = _errorCount,
            Uptime = DateTime.UtcNow - _startTime,
            MemoryUsageMB = GC.GetTotalMemory(false) / (1024 * 1024),
            StateCount = _state.Count
        };
    }

    private async Task InitializeStateAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Initializing ExtendedAutoModeAgent state");
        
        try
        {
            // Load previous state if exists
            var stateFile = Path.Combine(_options.StateDirectory, "extended_auto_mode_state.json");
            if (File.Exists(stateFile))
            {
                var stateJson = await File.ReadAllTextAsync(stateFile, cancellationToken);
                var previousState = JsonSerializer.Deserialize<Dictionary<string, object>>(stateJson);
                
                if (previousState != null)
                {
                    foreach (var kvp in previousState)
                    {
                        _state.TryAdd(kvp.Key, kvp.Value);
                    }
                }
                
                _logger.LogInformation("Loaded {StateCount} state entries from previous session", _state.Count);
            }
            
            // Initialize default state values
            _state.TryAdd("session_id", Guid.NewGuid().ToString());
            _state.TryAdd("initialized_at", DateTime.UtcNow);
            _state.TryAdd("kernel_plugins_count", _kernel.Plugins.Count);
            
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error initializing state");
            throw;
        }
    }

    private async Task RunMainLoopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Starting main operation loop");
        
        while (!cancellationToken.IsCancellationRequested && _isRunning)
        {
            try
            {
                await _operationSemaphore.WaitAsync(cancellationToken);
                
                try
                {
                    await ProcessOperationAsync(cancellationToken);
                    Interlocked.Increment(ref _operationCount);
                }
                finally
                {
                    _operationSemaphore.Release();
                }
                
                // Adaptive delay based on system load
                var delay = CalculateAdaptiveDelay();
                await Task.Delay(delay, cancellationToken);
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in main operation loop");
                Interlocked.Increment(ref _errorCount);
                
                // Exponential backoff on errors
                var errorDelay = Math.Min(TimeSpan.FromMinutes(1), TimeSpan.FromSeconds(Math.Pow(2, Math.Min(_errorCount, 10))));
                await Task.Delay(errorDelay, cancellationToken);
            }
        }
    }

    private async Task ProcessOperationAsync(CancellationToken cancellationToken)
    {
        // This is where the main semantic kernel operations would be performed
        // For now, we'll implement a basic operation that could be extended
        
        var operationId = Guid.NewGuid().ToString();
        _logger.LogDebug("Processing operation {OperationId}", operationId);
        
        try
        {
            // Example: Execute a kernel function
            var arguments = new KernelArguments
            {
                ["operation_id"] = operationId,
                ["timestamp"] = DateTime.UtcNow,
                ["state_count"] = _state.Count
            };
            
            // Update state with operation info
            _state.AddOrUpdate($"last_operation_{operationId}", DateTime.UtcNow, (k, v) => DateTime.UtcNow);
            
            // Simulate processing
            await Task.Delay(100, cancellationToken);
            
            _logger.LogDebug("Completed operation {OperationId}", operationId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing operation {OperationId}", operationId);
            throw;
        }
    }

    private TimeSpan CalculateAdaptiveDelay()
    {
        // Calculate delay based on system metrics
        var baseDelay = _options.BaseOperationDelayMs;
        var currentMemory = GC.GetTotalMemory(false);
        var memoryPressure = currentMemory / (1024.0 * 1024.0 * 1024.0); // GB
        
        // Increase delay if memory usage is high
        if (memoryPressure > 2.0)
        {
            baseDelay *= 2;
        }
        else if (memoryPressure > 1.0)
        {
            baseDelay = (int)(baseDelay * 1.5);
        }
        
        return TimeSpan.FromMilliseconds(baseDelay);
    }

    private async void PerformHealthCheck(object? state)
    {
        try
        {
            _logger.LogDebug("Performing health check");
            
            var status = GetStatus();
            
            // Check memory usage
            if (status.MemoryUsageMB > _options.MaxMemoryUsageMB)
            {
                _logger.LogWarning("High memory usage detected: {MemoryUsageMB}MB", status.MemoryUsageMB);
                GC.Collect();
                GC.WaitForPendingFinalizers();
                GC.Collect();
            }
            
            // Check error rate
            var errorRate = _operationCount > 0 ? (double)_errorCount / _operationCount : 0;
            if (errorRate > _options.MaxErrorRate)
            {
                _logger.LogWarning("High error rate detected: {ErrorRate:P2}", errorRate);
            }
            
            _lastHealthCheck = DateTime.UtcNow;
            
            // Log health status
            _logger.LogInformation("Health check completed - Uptime: {Uptime}, Operations: {Operations}, Errors: {Errors}, Memory: {Memory}MB",
                status.Uptime, status.OperationCount, status.ErrorCount, status.MemoryUsageMB);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during health check");
        }
    }

    private async void PerformMaintenance(object? state)
    {
        try
        {
            _logger.LogInformation("Performing system maintenance");
            
            // Clean up old state entries
            await CleanupStateAsync();
            
            // Save current state
            await SaveStateAsync();
            
            // Force garbage collection
            GC.Collect();
            GC.WaitForPendingFinalizers();
            GC.Collect();
            
            _logger.LogInformation("System maintenance completed");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during system maintenance");
        }
    }

    private async Task CleanupStateAsync()
    {
        var cutoffTime = DateTime.UtcNow.AddHours(-_options.StateRetentionHours);
        var keysToRemove = new List<string>();
        
        foreach (var kvp in _state)
        {
            if (kvp.Key.StartsWith("last_operation_") && kvp.Value is DateTime operationTime)
            {
                if (operationTime < cutoffTime)
                {
                    keysToRemove.Add(kvp.Key);
                }
            }
        }
        
        foreach (var key in keysToRemove)
        {
            _state.TryRemove(key, out _);
        }
        
        if (keysToRemove.Count > 0)
        {
            _logger.LogDebug("Cleaned up {Count} old state entries", keysToRemove.Count);
        }
        
        await Task.CompletedTask;
    }

    private async Task SaveStateAsync()
    {
        try
        {
            if (!Directory.Exists(_options.StateDirectory))
            {
                Directory.CreateDirectory(_options.StateDirectory);
            }
            
            var stateFile = Path.Combine(_options.StateDirectory, "extended_auto_mode_state.json");
            var stateJson = JsonSerializer.Serialize(_state.ToDictionary(kvp => kvp.Key, kvp => kvp.Value), new JsonSerializerOptions { WriteIndented = true });
            
            await File.WriteAllTextAsync(stateFile, stateJson);
            _logger.LogDebug("State saved to {StateFile}", stateFile);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error saving state");
        }
    }

    /// <summary>
    /// Disposes the ExtendedAutoModeAgent and releases all resources.
    /// </summary>
    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        _disposed = true;
        
        _cancellationTokenSource?.Cancel();
        _healthCheckTimer?.Dispose();
        _maintenanceTimer?.Dispose();
        _operationSemaphore?.Dispose();
        _cancellationTokenSource?.Dispose();
        
        // Save final state
        try
        {
            SaveStateAsync().GetAwaiter().GetResult();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error saving final state during disposal");
        }
        
        _logger.LogInformation("ExtendedAutoModeAgent disposed");
    }
}

/// <summary>
/// Configuration options for the ExtendedAutoModeAgent.
/// </summary>
public class ExtendedAutoModeOptions
{
    /// <summary>
    /// Gets or sets the maximum number of concurrent operations.
    /// </summary>
    public int MaxConcurrentOperations { get; set; } = 5;

    /// <summary>
    /// Gets or sets the base delay between operations in milliseconds.
    /// </summary>
    public int BaseOperationDelayMs { get; set; } = 1000;

    /// <summary>
    /// Gets or sets the health check interval in minutes.
    /// </summary>
    public int HealthCheckIntervalMinutes { get; set; } = 5;

    /// <summary>
    /// Gets or sets the maintenance interval in hours.
    /// </summary>
    public int MaintenanceIntervalHours { get; set; } = 24;

    /// <summary>
    /// Gets or sets the maximum memory usage in MB before warnings.
    /// </summary>
    public long MaxMemoryUsageMB { get; set; } = 2048;

    /// <summary>
    /// Gets or sets the maximum acceptable error rate (0.0 to 1.0).
    /// </summary>
    public double MaxErrorRate { get; set; } = 0.05;

    /// <summary>
    /// Gets or sets the state retention time in hours.
    /// </summary>
    public int StateRetentionHours { get; set; } = 168; // 7 days

    /// <summary>
    /// Gets or sets the directory for storing state files.
    /// </summary>
    public string StateDirectory { get; set; } = "./state";
}

/// <summary>
/// Status information for the ExtendedAutoModeAgent.
/// </summary>
public class ExtendedAutoModeStatus
{
    /// <summary>
    /// Gets or sets a value indicating whether the agent is currently running.
    /// </summary>
    public bool IsRunning { get; set; }

    /// <summary>
    /// Gets or sets the start time of the agent.
    /// </summary>
    public DateTime StartTime { get; set; }

    /// <summary>
    /// Gets or sets the last health check time.
    /// </summary>
    public DateTime LastHealthCheck { get; set; }

    /// <summary>
    /// Gets or sets the total number of operations performed.
    /// </summary>
    public int OperationCount { get; set; }

    /// <summary>
    /// Gets or sets the total number of errors encountered.
    /// </summary>
    public int ErrorCount { get; set; }

    /// <summary>
    /// Gets or sets the uptime of the agent.
    /// </summary>
    public TimeSpan Uptime { get; set; }

    /// <summary>
    /// Gets or sets the current memory usage in MB.
    /// </summary>
    public long MemoryUsageMB { get; set; }

    /// <summary>
    /// Gets or sets the number of state entries.
    /// </summary>
    public int StateCount { get; set; }

    /// <summary>
    /// Gets the error rate as a percentage.
    /// </summary>
    public double ErrorRate => OperationCount > 0 ? (double)ErrorCount / OperationCount : 0.0;
}
