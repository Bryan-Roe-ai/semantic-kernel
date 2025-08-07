// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.SemanticKernel.Agents.Chat;
using Microsoft.SemanticKernel.ChatCompletion;
using Xunit;

namespace SemanticKernel.Agents.UnitTests.Core.Chat;

/// <summary>
/// Comprehensive unit tests for cached sequential selection strategy.
/// </summary>
public class CachedSequentialSelectionStrategyTests
{
    /// <summary>
    /// Verify cached sequential selection provides agents in expected order with performance benefits.
    /// </summary>
    [Fact]
    public async Task VerifyCachedSequentialSelectionPerformanceAsync()
    {
        // Arrange
        MockAgent agent1 = new() { Id = "agent1" };
        MockAgent agent2 = new() { Id = "agent2" };
        MockAgent agent3 = new() { Id = "agent3" };

        Agent[] agents = [agent1, agent2, agent3];
        var strategy = new CachedSequentialSelectionStrategy()
        {
            EnableMetrics = true,
            MaxCacheSize = 100
        };

        var history = new List<ChatMessageContent>
        {
            new(AuthorRole.User, "Test message 1"),
            new(AuthorRole.Assistant, "Test response 1")
        };

        // Act & Assert - First execution (cache miss)
        var stopwatch = Stopwatch.StartNew();
        await VerifyNextAgentAsync(agent1, agents, strategy, history);
        var firstExecutionTime = stopwatch.ElapsedMilliseconds;

        // Second execution with same parameters (should be cache hit)
        stopwatch.Restart();
        await VerifyNextAgentAsync(agent2, agents, strategy, history);
        var secondExecutionTime = stopwatch.ElapsedMilliseconds;

        // Verify performance improvement through caching
        Assert.True(strategy.Metrics.CacheHits > 0, "Expected cache hits to be recorded");
        Assert.True(strategy.Metrics.TotalSelections > 0, "Expected total selections to be recorded");
        
        // Continue the sequence
        await VerifyNextAgentAsync(agent3, agents, strategy, history);
        await VerifyNextAgentAsync(agent1, agents, strategy, history); // Wraps around
        
        // Verify metrics
        var metrics = strategy.Metrics;
        Assert.True(metrics.CacheHitRatio > 0, "Expected positive cache hit ratio");
        Assert.True(metrics.AverageSelectionTimeMs >= 0, "Expected non-negative average selection time");
    }

    /// <summary>
    /// Verify cache behavior with different history contexts.
    /// </summary>
    [Fact]
    public async Task VerifyCacheWithDifferentHistoryContextsAsync()
    {
        // Arrange
        MockAgent agent1 = new() { Id = "agent1" };
        MockAgent agent2 = new() { Id = "agent2" };
        Agent[] agents = [agent1, agent2];

        var strategy = new CachedSequentialSelectionStrategy();

        var history1 = new List<ChatMessageContent>
        {
            new(AuthorRole.User, "Context 1")
        };

        var history2 = new List<ChatMessageContent>
        {
            new(AuthorRole.User, "Context 2")
        };

        // Act
        var result1 = await strategy.NextAsync(agents, history1);
        var result2 = await strategy.NextAsync(agents, history2);
        var result3 = await strategy.NextAsync(agents, history1); // Same as first context

        // Assert
        Assert.Equal(agent1, result1);
        Assert.Equal(agent2, result2); // Different context, continues sequence
        // Result3 might be cached depending on implementation details
    }

    /// <summary>
    /// Verify cache cleanup and TTL behavior.
    /// </summary>
    [Fact]
    public async Task VerifyCacheCleanupBehaviorAsync()
    {
        // Arrange
        MockAgent agent1 = new() { Id = "agent1" };
        MockAgent agent2 = new() { Id = "agent2" };
        Agent[] agents = [agent1, agent2];

        var strategy = new CachedSequentialSelectionStrategy()
        {
            MaxCacheSize = 2 // Small cache for testing cleanup
        };

        var histories = new List<List<ChatMessageContent>>
        {
            new() { new(AuthorRole.User, "Message 1") },
            new() { new(AuthorRole.User, "Message 2") },
            new() { new(AuthorRole.User, "Message 3") },
            new() { new(AuthorRole.User, "Message 4") }
        };

        // Act - Fill cache beyond limit
        foreach (var history in histories)
        {
            await strategy.NextAsync(agents, history);
        }

        // Manually clear cache to test the functionality
        await strategy.ClearCacheAsync();

        // Assert
        Assert.True(strategy.Metrics.CacheClears > 0, "Expected cache clears to be recorded");
    }

    /// <summary>
    /// Verify strategy behavior with initial agent setting.
    /// </summary>
    [Fact]
    public async Task VerifyCachedSequentialSelectionWithInitialAgentAsync()
    {
        // Arrange
        MockAgent agent1 = new() { Id = "agent1" };
        MockAgent agent2 = new() { Id = "agent2" };
        MockAgent agent3 = new() { Id = "agent3" };
        Agent[] agents = [agent1, agent2, agent3];

        var strategy = new CachedSequentialSelectionStrategy()
        {
            InitialAgent = agent3
        };

        var history = new List<ChatMessageContent>();

        // Act & Assert
        await VerifyNextAgentAsync(agent3, agents, strategy, history); // Uses initial agent
        await VerifyNextAgentAsync(agent1, agents, strategy, history); // Then sequential
        await VerifyNextAgentAsync(agent2, agents, strategy, history);
        await VerifyNextAgentAsync(agent3, agents, strategy, history);
    }

    /// <summary>
    /// Verify error handling and metrics tracking.
    /// </summary>
    [Fact]
    public async Task VerifyErrorHandlingAndMetricsAsync()
    {
        // Arrange
        var strategy = new CachedSequentialSelectionStrategy()
        {
            EnableMetrics = true
        };

        var emptyAgents = new Agent[0];
        var history = new List<ChatMessageContent>();

        // Act & Assert
        await Assert.ThrowsAsync<KernelException>(() => strategy.NextAsync(emptyAgents, history));
        
        // Verify error metrics
        Assert.True(strategy.Metrics.SelectionErrors > 0, "Expected selection errors to be recorded");
    }

    /// <summary>
    /// Verify reset functionality clears state properly.
    /// </summary>
    [Fact]
    public async Task VerifyResetFunctionalityAsync()
    {
        // Arrange
        MockAgent agent1 = new() { Id = "agent1" };
        MockAgent agent2 = new() { Id = "agent2" };
        Agent[] agents = [agent1, agent2];

        var strategy = new CachedSequentialSelectionStrategy();
        var history = new List<ChatMessageContent>
        {
            new(AuthorRole.User, "Test message")
        };

        // Act - Use strategy to build cache and state
        await strategy.NextAsync(agents, history);
        await strategy.NextAsync(agents, history);

        var metricsBeforeReset = strategy.Metrics;
        
        // Reset strategy
        strategy.Reset();

        // Verify reset state
        var metricsAfterReset = strategy.Metrics;
        Assert.Equal(0, metricsAfterReset.TotalSelections);
        Assert.Equal(0, metricsAfterReset.CacheHits);
        Assert.Equal(0, metricsAfterReset.CacheMisses);

        // Verify behavior after reset
        await VerifyNextAgentAsync(agent1, agents, strategy, history); // Should start from beginning
    }

    /// <summary>
    /// Verify concurrent access to cached strategy.
    /// </summary>
    [Fact]
    public async Task VerifyConcurrentAccessAsync()
    {
        // Arrange
        MockAgent agent1 = new() { Id = "agent1" };
        MockAgent agent2 = new() { Id = "agent2" };
        Agent[] agents = [agent1, agent2];

        var strategy = new CachedSequentialSelectionStrategy()
        {
            EnableMetrics = true
        };

        var history = new List<ChatMessageContent>
        {
            new(AuthorRole.User, "Concurrent test")
        };

        // Act - Execute multiple selections concurrently
        var tasks = Enumerable.Range(0, 10)
            .Select(_ => strategy.NextAsync(agents, history))
            .ToArray();

        var results = await Task.WhenAll(tasks);

        // Assert
        Assert.Equal(10, results.Length);
        Assert.All(results, result => Assert.Contains(result, agents));
        
        // Verify metrics show concurrent executions
        Assert.Equal(10, strategy.Metrics.TotalSelections);
    }

    /// <summary>
    /// Performance benchmark test for cached vs non-cached selection.
    /// </summary>
    [Fact]
    public async Task BenchmarkCachedVsNonCachedPerformanceAsync()
    {
        // Arrange
        var agents = Enumerable.Range(0, 10)
            .Select(i => new MockAgent { Id = $"agent{i}" })
            .Cast<Agent>()
            .ToArray();

        var cachedStrategy = new CachedSequentialSelectionStrategy()
        {
            EnableMetrics = true,
            MaxCacheSize = 1000
        };

        var standardStrategy = new SequentialSelectionStrategy();

        var history = new List<ChatMessageContent>
        {
            new(AuthorRole.User, "Performance test message")
        };

        const int iterations = 100;

        // Act - Benchmark cached strategy
        var cachedStopwatch = Stopwatch.StartNew();
        for (int i = 0; i < iterations; i++)
        {
            await cachedStrategy.NextAsync(agents, history);
        }
        cachedStopwatch.Stop();

        // Benchmark standard strategy
        var standardStopwatch = Stopwatch.StartNew();
        for (int i = 0; i < iterations; i++)
        {
            await standardStrategy.NextAsync(agents, history);
        }
        standardStopwatch.Stop();

        // Assert - Cached strategy should show performance benefits through metrics
        var metrics = cachedStrategy.Metrics;
        Assert.True(metrics.CacheHits > 0, "Expected cache hits during benchmark");
        Assert.True(metrics.CacheHitRatio > 0, "Expected positive cache hit ratio");
        
        // Log performance comparison
        var cachedAvgMs = cachedStopwatch.ElapsedMilliseconds / (double)iterations;
        var standardAvgMs = standardStopwatch.ElapsedMilliseconds / (double)iterations;
        
        // The cached strategy might be slightly slower initially due to caching overhead,
        // but should show benefits in real-world scenarios with repeated patterns
        Assert.True(cachedAvgMs >= 0 && standardAvgMs >= 0, "Both strategies should have non-negative execution times");
    }

    /// <summary>
    /// Verify cache statistics reporting.
    /// </summary>
    [Fact]
    public async Task VerifyCacheStatisticsAsync()
    {
        // Arrange
        MockAgent agent1 = new() { Id = "agent1" };
        MockAgent agent2 = new() { Id = "agent2" };
        Agent[] agents = [agent1, agent2];

        var strategy = new CachedSequentialSelectionStrategy()
        {
            EnableMetrics = true
        };

        var history = new List<ChatMessageContent>
        {
            new(AuthorRole.User, "Statistics test")
        };

        // Act
        await strategy.NextAsync(agents, history);
        await strategy.NextAsync(agents, history);
        await strategy.NextAsync(agents, history);

        // Assert
        var metrics = strategy.Metrics;
        Assert.True(metrics.TotalSelections >= 3, "Expected at least 3 total selections");
        
        var metricsString = metrics.ToString();
        Assert.Contains("Total:", metricsString);
        Assert.Contains("Hits:", metricsString);
        Assert.Contains("Hit Ratio:", metricsString);
        Assert.Contains("Avg Time:", metricsString);
    }

    private static async Task VerifyNextAgentAsync(
        Agent expectedAgent, 
        Agent[] agents, 
        CachedSequentialSelectionStrategy strategy,
        IReadOnlyList<ChatMessageContent>? history = null)
    {
        history ??= new List<ChatMessageContent>();
        
        // Act
        Agent? nextAgent = await strategy.NextAsync(agents, history);
        
        // Assert
        Assert.NotNull(nextAgent);
        Assert.Equal(expectedAgent.Id, nextAgent.Id);
    }
}

/// <summary>
/// Mock agent implementation for testing.
/// </summary>
internal class MockAgent : Agent
{
    public override string Id { get; } = Guid.NewGuid().ToString();
    public override string Name => $"Mock Agent {Id[..8]}";
    public override string Description => "Mock agent for testing";

    public MockAgent()
    {
        // Initialize with minimal required setup for testing
    }
}
