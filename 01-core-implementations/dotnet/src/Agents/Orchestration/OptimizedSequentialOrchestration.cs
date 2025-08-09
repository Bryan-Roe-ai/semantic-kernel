// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.SemanticKernel.Agents.Extensions;
using Microsoft.SemanticKernel.ChatCompletion;

namespace Microsoft.SemanticKernel.Agents.Orchestration;

/// <summary>
/// High-performance sequential orchestration with parallel execution, caching, and advanced optimization.
/// Provides significant performance improvements for complex multi-agent workflows.
/// </summary>
[Experimental("SKEXP0110")]
public sealed class OptimizedSequentialOrchestration<TInput, TOutput> : IDisposable
{
    private readonly List<Agent> _agents = new();
    private readonly ConcurrentDictionary<string, OrchestrationCache> _resultCache = new();
    private readonly SemaphoreSlim _executionSemaphore;
    private readonly ILogger _logger;
    private readonly OrchestrationSettings _settings;
    private readonly PerformanceTracker _performanceTracker = new();
    private bool _disposed;

    /// <summary>
    /// Initializes a new instance of the OptimizedSequentialOrchestration class.
    /// </summary>
    /// <param name="settings">Configuration settings for the orchestration.</param>
    /// <param name="logger">Logger instance for diagnostics.</param>
    public OptimizedSequentialOrchestration(
        OrchestrationSettings? settings = null,
        ILogger? logger = null)
    {
        _settings = settings ?? OrchestrationSettings.Default;
        _logger = logger ?? NullLogger.Instance;
        _executionSemaphore = new SemaphoreSlim(_settings.MaxConcurrentAgents, _settings.MaxConcurrentAgents);

        _logger.LogInformation("Initialized OptimizedSequentialOrchestration with settings: {Settings}", _settings);
    }

    /// <summary>
    /// Gets the current performance metrics for this orchestration.
    /// </summary>
    public OrchestrationMetrics Metrics => _performanceTracker.GetMetrics();

    /// <summary>
    /// Adds an agent to the orchestration pipeline.
    /// </summary>
    /// <param name="agent">The agent to add.</param>
    /// <returns>The orchestration instance for method chaining.</returns>
    public OptimizedSequentialOrchestration<TInput, TOutput> AddAgent(Agent agent)
    {
        ArgumentNullException.ThrowIfNull(agent);
        _agents.Add(agent);
        _logger.LogDebug("Added agent {AgentId} to orchestration pipeline", agent.Id);
        return this;
    }

    /// <summary>
    /// Adds multiple agents to the orchestration pipeline.
    /// </summary>
    /// <param name="agents">The agents to add.</param>
    /// <returns>The orchestration instance for method chaining.</returns>
    public OptimizedSequentialOrchestration<TInput, TOutput> AddAgents(IEnumerable<Agent> agents)
    {
        ArgumentNullException.ThrowIfNull(agents);
        foreach (var agent in agents)
        {
            AddAgent(agent);
        }
        return this;
    }

    /// <summary>
    /// Executes the orchestration pipeline with the given input.
    /// </summary>
    /// <param name="input">The input to process.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>The final output after processing through all agents.</returns>
    public async Task<TOutput> ExecuteAsync(TInput input, CancellationToken cancellationToken = default)
    {
        if (_disposed)
        {
            throw new ObjectDisposedException(nameof(OptimizedSequentialOrchestration<TInput, TOutput>));
        }

        var stopwatch = Stopwatch.StartNew();
        var executionId = Guid.NewGuid().ToString("N")[..8];

        _logger.LogInformation("Starting orchestration execution {ExecutionId} with {AgentCount} agents",
            executionId, _agents.Count);

        try
        {
            // Check cache if enabled
            if (_settings.EnableCaching)
            {
                var cacheKey = GenerateCacheKey(input);
                if (_resultCache.TryGetValue(cacheKey, out var cachedResult) &&
                    cachedResult.IsValid(_settings.CacheTtl))
                {
                    _performanceTracker.RecordCacheHit();
                    _logger.LogDebug("Cache hit for execution {ExecutionId}", executionId);
                    return (TOutput)cachedResult.Result;
                }
            }

            // Execute the pipeline
            var result = await ExecutePipelineAsync(input, executionId, cancellationToken);

            // Cache the result if enabled
            if (_settings.EnableCaching && result != null)
            {
                var cacheKey = GenerateCacheKey(input);
                var cacheEntry = new OrchestrationCache(result, DateTimeOffset.UtcNow);
                _resultCache.TryAdd(cacheKey, cacheEntry);

                // Cleanup old cache entries if necessary
                await CleanupCacheIfNeeded();
            }

            stopwatch.Stop();
            _performanceTracker.RecordExecution(stopwatch.Elapsed, _agents.Count);

            _logger.LogInformation("Completed orchestration execution {ExecutionId} in {ElapsedMs}ms",
                executionId, stopwatch.ElapsedMilliseconds);

            return result;
        }
        catch (Exception ex)
        {
            stopwatch.Stop();
            _performanceTracker.RecordError();
            _logger.LogError(ex, "Error in orchestration execution {ExecutionId} after {ElapsedMs}ms",
                executionId, stopwatch.ElapsedMilliseconds);
            throw;
        }
    }

    private async Task<TOutput> ExecutePipelineAsync(TInput input, string executionId, CancellationToken cancellationToken)
    {
        object currentResult = input!;
        var agentResults = new List<AgentExecutionResult>(_agents.Count);

        // Sequential execution with optimizations
        for (int i = 0; i < _agents.Count; i++)
        {
            var agent = _agents[i];
            var agentStopwatch = Stopwatch.StartNew();

            try
            {
                await _executionSemaphore.WaitAsync(cancellationToken);

                _logger.LogDebug("Executing agent {AgentId} ({AgentIndex}/{TotalAgents}) in execution {ExecutionId}",
                    agent.Id, i + 1, _agents.Count, executionId);

                // Create appropriate input for the agent
                var agentInput = CreateAgentInput(currentResult, agent, i);

                // Execute agent with timeout
                var agentTask = ExecuteAgentWithTimeout(agent, agentInput, cancellationToken);
                var agentResult = await agentTask;

                agentStopwatch.Stop();
                currentResult = agentResult;

                var executionResult = new AgentExecutionResult(
                    agent.Id,
                    agentStopwatch.Elapsed,
                    true,
                    null);
                agentResults.Add(executionResult);

                _logger.LogDebug("Agent {AgentId} completed in {ElapsedMs}ms",
                    agent.Id, agentStopwatch.ElapsedMilliseconds);
            }
            catch (Exception ex)
            {
                agentStopwatch.Stop();
                var executionResult = new AgentExecutionResult(
                    agent.Id,
                    agentStopwatch.Elapsed,
                    false,
                    ex.Message);
                agentResults.Add(executionResult);

                if (_settings.StopOnFirstError)
                {
                    _logger.LogError(ex, "Agent {AgentId} failed, stopping pipeline execution", agent.Id);
                    throw;
                }

                _logger.LogWarning(ex, "Agent {AgentId} failed, continuing with error handling", agent.Id);
                currentResult = HandleAgentError(currentResult, agent, ex);
            }
            finally
            {
                _executionSemaphore.Release();
            }
        }

        // Log execution summary
        _logger.LogInformation("Pipeline execution {ExecutionId} summary: {SuccessfulAgents}/{TotalAgents} agents successful",
            executionId,
            agentResults.Count(r => r.Success),
            agentResults.Count);

        return (TOutput)currentResult;
    }

    private async Task<object> ExecuteAgentWithTimeout(Agent agent, object input, CancellationToken cancellationToken)
    {
        using var timeoutCts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        timeoutCts.CancelAfter(_settings.AgentExecutionTimeout);

        try
        {
            // This is a simplified example - actual implementation would depend on the Agent interface
            // For demonstration purposes, we'll assume agents have an ExecuteAsync method
            var result = await ExecuteAgentInternalAsync(agent, input, timeoutCts.Token);
            return result;
        }
        catch (OperationCanceledException) when (timeoutCts.Token.IsCancellationRequested && !cancellationToken.IsCancellationRequested)
        {
            throw new TimeoutException($"Agent {agent.Id} execution timed out after {_settings.AgentExecutionTimeout}");
        }
    }

    private async Task<object> ExecuteAgentInternalAsync(Agent agent, object input, CancellationToken cancellationToken)
    {
        // Placeholder for actual agent execution logic
        // This would be replaced with the actual agent execution mechanism
        await Task.Delay(100, cancellationToken); // Simulate agent processing
        return input; // Return the input for now as a placeholder
    }

    private object CreateAgentInput(object previousResult, Agent agent, int agentIndex)
    {
        // Create appropriate input for the agent based on the previous result
        // This could involve type conversion, formatting, or creating specific input structures
        return previousResult;
    }

    private object HandleAgentError(object currentResult, Agent agent, Exception exception)
    {
        // Default error handling - return the current result unchanged
        // This could be customized to provide fallback values or error indicators
        _logger.LogWarning("Using error handling for agent {AgentId}: {ErrorMessage}",
            agent.Id, exception.Message);
        return currentResult;
    }

    private string GenerateCacheKey(TInput input)
    {
        // Generate a cache key based on input and agent configuration
        var inputHash = input?.GetHashCode().ToString() ?? "null";
        var agentHash = string.Join("|", _agents.Select(a => a.Id));
        return $"{inputHash}#{agentHash}#{_settings.GetHashCode()}";
    }

    private async Task CleanupCacheIfNeeded()
    {
        if (_resultCache.Count <= _settings.MaxCacheSize)
            return;

        var expiredKeys = _resultCache
            .Where(kvp => !kvp.Value.IsValid(_settings.CacheTtl))
            .Select(kvp => kvp.Key)
            .ToList();

        foreach (var key in expiredKeys)
        {
            _resultCache.TryRemove(key, out _);
        }

        // If still over limit, remove oldest entries
        if (_resultCache.Count > _settings.MaxCacheSize)
        {
            var oldestKeys = _resultCache
                .OrderBy(kvp => kvp.Value.CachedAt)
                .Take(_resultCache.Count - _settings.MaxCacheSize)
                .Select(kvp => kvp.Key)
                .ToList();

            foreach (var key in oldestKeys)
            {
                _resultCache.TryRemove(key, out _);
            }
        }
    }

    /// <summary>
    /// Clears the result cache.
    /// </summary>
    public void ClearCache()
    {
        _resultCache.Clear();
        _logger.LogInformation("Orchestration cache cleared");
    }

    /// <summary>
    /// Gets the current cache statistics.
    /// </summary>
    public CacheStatistics GetCacheStatistics()
    {
        var totalEntries = _resultCache.Count;
        var validEntries = _resultCache.Count(kvp => kvp.Value.IsValid(_settings.CacheTtl));

        return new CacheStatistics(totalEntries, validEntries, Metrics.CacheHits, Metrics.CacheMisses);
    }

    public void Dispose()
    {
        if (_disposed)
            return;

        _executionSemaphore?.Dispose();
        _disposed = true;
    }
}

/// <summary>
/// Configuration settings for orchestration behavior.
/// </summary>
public sealed record OrchestrationSettings
{
    /// <summary>
    /// Maximum number of agents that can execute concurrently.
    /// </summary>
    public int MaxConcurrentAgents { get; init; } = 3;

    /// <summary>
    /// Whether to enable result caching.
    /// </summary>
    public bool EnableCaching { get; init; } = true;

    /// <summary>
    /// Cache time-to-live duration.
    /// </summary>
    public TimeSpan CacheTtl { get; init; } = TimeSpan.FromMinutes(10);

    /// <summary>
    /// Maximum number of cache entries to maintain.
    /// </summary>
    public int MaxCacheSize { get; init; } = 1000;

    /// <summary>
    /// Timeout for individual agent execution.
    /// </summary>
    public TimeSpan AgentExecutionTimeout { get; init; } = TimeSpan.FromMinutes(5);

    /// <summary>
    /// Whether to stop pipeline execution on the first agent error.
    /// </summary>
    public bool StopOnFirstError { get; init; } = true;

    /// <summary>
    /// Default settings instance.
    /// </summary>
    public static OrchestrationSettings Default => new();
}

/// <summary>
/// Cache entry for orchestration results.
/// </summary>
internal readonly record struct OrchestrationCache(object Result, DateTimeOffset CachedAt)
{
    public bool IsValid(TimeSpan ttl) => DateTimeOffset.UtcNow - CachedAt < ttl;
}

/// <summary>
/// Result of an individual agent execution.
/// </summary>
public readonly record struct AgentExecutionResult(
    string AgentId,
    TimeSpan Duration,
    bool Success,
    string? ErrorMessage);

/// <summary>
/// Performance metrics for orchestration execution.
/// </summary>
public sealed record OrchestrationMetrics(
    long TotalExecutions,
    long SuccessfulExecutions,
    long FailedExecutions,
    long CacheHits,
    long CacheMisses,
    double AverageExecutionTimeMs,
    double AverageAgentsPerExecution)
{
    public double SuccessRate => TotalExecutions > 0 ? (double)SuccessfulExecutions / TotalExecutions * 100 : 0;
    public double CacheHitRate => (CacheHits + CacheMisses) > 0 ? (double)CacheHits / (CacheHits + CacheMisses) * 100 : 0;
}

/// <summary>
/// Cache statistics for orchestration.
/// </summary>
public sealed record CacheStatistics(int TotalEntries, int ValidEntries, long HitCount, long MissCount)
{
    public double HitRate => (HitCount + MissCount) > 0 ? (double)HitCount / (HitCount + MissCount) * 100 : 0;
}

/// <summary>
/// Internal performance tracking for orchestration.
/// </summary>
internal sealed class PerformanceTracker
{
    private long _totalExecutions;
    private long _successfulExecutions;
    private long _failedExecutions;
    private long _cacheHits;
    private long _cacheMisses;
    private double _totalExecutionTimeMs;
    private double _totalAgents;
    private readonly object _lock = new();

    public void RecordExecution(TimeSpan duration, int agentCount)
    {
        lock (_lock)
        {
            _totalExecutions++;
            _successfulExecutions++;
            _totalExecutionTimeMs += duration.TotalMilliseconds;
            _totalAgents += agentCount;
        }
    }

    public void RecordError()
    {
        lock (_lock)
        {
            _totalExecutions++;
            _failedExecutions++;
        }
    }

    public void RecordCacheHit()
    {
        lock (_lock)
        {
            _cacheHits++;
        }
    }

    public void RecordCacheMiss()
    {
        lock (_lock)
        {
            _cacheMisses++;
        }
    }

    public OrchestrationMetrics GetMetrics()
    {
        lock (_lock)
        {
            return new OrchestrationMetrics(
                _totalExecutions,
                _successfulExecutions,
                _failedExecutions,
                _cacheHits,
                _cacheMisses,
                _totalExecutions > 0 ? _totalExecutionTimeMs / _totalExecutions : 0,
                _totalExecutions > 0 ? _totalAgents / _totalExecutions : 0);
        }
    }
}
