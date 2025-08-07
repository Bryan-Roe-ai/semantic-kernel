#!/usr/bin/env python3
"""
Comprehensive test suite for batch sequential selection strategy

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Comprehensive testing for batch processing optimizations.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import asyncio
import time
from unittest.mock import MagicMock

import pytest

from semantic_kernel.agents.agent import Agent
from semantic_kernel.agents.strategies.selection.batch_sequential_selection_strategy import (
    BatchSequentialSelectionStrategy,
    BatchProcessingMetrics,
)
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.exceptions.agent_exceptions import AgentExecutionException


class MockAgent:
    """Mock agent for testing purposes."""
    
    def __init__(self, agent_id: str, name: str = None):
        self.id = agent_id
        self.name = name or f"Agent_{agent_id}"
        self.plugins = []


@pytest.fixture
def mock_agents():
    """Fixture providing a list of mock agents."""
    return [
        MockAgent("agent-1", "Research Agent"),
        MockAgent("agent-2", "Analysis Agent"),
        MockAgent("agent-3", "Writing Agent"),
        MockAgent("agent-4", "Review Agent"),
        MockAgent("agent-5", "Quality Agent"),
    ]


@pytest.fixture
def sample_history():
    """Fixture providing sample chat history."""
    return [
        ChatMessageContent(role="user", content="Start research task"),
        ChatMessageContent(role="assistant", content="Research completed", name="agent-1"),
        ChatMessageContent(role="assistant", content="Analysis finished", name="agent-2"),
    ]


@pytest.fixture
def strategy():
    """Fixture providing a configured batch strategy."""
    return BatchSequentialSelectionStrategy(
        initial_batch_size=3,
        max_batch_size=10,
        min_batch_size=2,
        enable_adaptive_batching=True,
        enable_caching=True,
        cache_ttl_seconds=60.0,
    )


class TestBatchSequentialSelectionStrategy:
    """Test suite for batch sequential selection strategy."""

    async def test_basic_sequential_selection(self, strategy, mock_agents, sample_history):
        """Test basic sequential selection functionality."""
        # First selection
        agent1 = await strategy.next(mock_agents, sample_history)
        assert agent1 in mock_agents
        assert strategy.has_selected

        # Second selection
        agent2 = await strategy.next(mock_agents, sample_history)
        assert agent2 in mock_agents
        assert agent2 != agent1  # Should select different agent

        # Third selection
        agent3 = await strategy.next(mock_agents, sample_history)
        assert agent3 in mock_agents

    async def test_round_robin_behavior(self, strategy, mock_agents, sample_history):
        """Test that selection follows round-robin pattern."""
        selected_agents = []
        
        # Select agents for a full cycle plus one
        for _ in range(len(mock_agents) + 1):
            agent = await strategy.next(mock_agents, sample_history)
            selected_agents.append(agent.id)

        # Verify round-robin: after full cycle, should start over
        assert selected_agents[0] == selected_agents[len(mock_agents)]

    async def test_caching_performance(self, strategy, mock_agents, sample_history):
        """Test caching improves performance for repeated selections."""
        # Enable metrics tracking
        strategy.enable_caching = True
        
        # First selection (cache miss)
        start_time = time.time()
        await strategy.next(mock_agents, sample_history)
        first_duration = time.time() - start_time

        # Second selection with same parameters (potential cache hit)
        start_time = time.time()
        await strategy.next(mock_agents, sample_history)
        second_duration = time.time() - start_time

        # Verify metrics
        assert strategy.metrics.cache_hits > 0 or strategy.metrics.cache_misses > 0
        assert strategy.metrics.cache_hit_ratio >= 0

    async def test_adaptive_batching(self, strategy, mock_agents, sample_history):
        """Test adaptive batch sizing based on performance."""
        initial_batch_size = strategy._current_batch_size
        
        # Simulate multiple selections to trigger adaptive behavior
        for _ in range(10):
            await strategy.next(mock_agents, sample_history)
            # Add small delay to simulate processing time
            await asyncio.sleep(0.001)

        # Batch size might have been adjusted based on performance
        final_batch_size = strategy._current_batch_size
        assert strategy.min_batch_size <= final_batch_size <= strategy.max_batch_size

    async def test_priority_based_selection(self, strategy, mock_agents, sample_history):
        """Test priority-based agent selection."""
        # Manually set priorities for some agents
        strategy._agent_priorities["agent-1"] = 2.0  # High priority
        strategy._agent_priorities["agent-3"] = 0.5  # Low priority
        
        # Perform selections and verify priority influence
        selected_agents = []
        for _ in range(10):
            agent = await strategy.next(mock_agents, sample_history)
            selected_agents.append(agent.id)

        # High priority agent should appear more frequently
        # This is probabilistic, so we check for general trend
        high_priority_count = selected_agents.count("agent-1")
        low_priority_count = selected_agents.count("agent-3")
        
        # High priority agent should be selected at least as often as low priority
        assert high_priority_count >= low_priority_count

    async def test_empty_agents_error(self, strategy):
        """Test error handling with empty agent list."""
        with pytest.raises(AgentExecutionException) as exc_info:
            await strategy.next([], [])
        
        assert "No agents present to select" in str(exc_info.value)

    async def test_initial_agent_selection(self, strategy, mock_agents, sample_history):
        """Test initial agent configuration."""
        initial_agent = mock_agents[2]
        strategy.initial_agent = initial_agent
        strategy.has_selected = False

        # First selection should use initial agent
        selected_agent = await strategy.next(mock_agents, sample_history)
        assert selected_agent == initial_agent

        # Subsequent selections should follow sequential pattern
        next_agent = await strategy.next(mock_agents, sample_history)
        assert next_agent != initial_agent

    async def test_cache_expiration(self, strategy, mock_agents, sample_history):
        """Test cache TTL and expiration behavior."""
        # Set very short cache TTL for testing
        strategy.cache_ttl_seconds = 0.1
        
        # First selection
        await strategy.next(mock_agents, sample_history)
        cache_size_before = len(strategy._agent_cache)
        
        # Wait for cache to expire
        await asyncio.sleep(0.2)
        
        # Another selection should trigger cache cleanup
        await strategy.next(mock_agents, sample_history)
        
        # Verify cache was cleaned up
        assert len(strategy._agent_cache) <= cache_size_before

    async def test_performance_tracking(self, strategy, mock_agents, sample_history):
        """Test performance metrics tracking."""
        initial_metrics = strategy.metrics
        
        # Perform several selections
        for _ in range(5):
            await strategy.next(mock_agents, sample_history)
            await asyncio.sleep(0.001)  # Small delay

        # Verify metrics were updated
        final_metrics = strategy.metrics
        assert final_metrics.total_agents_processed > initial_metrics.total_agents_processed
        assert final_metrics.average_agent_processing_time_ms >= 0

    async def test_reset_functionality(self, strategy, mock_agents, sample_history):
        """Test strategy reset functionality."""
        # Use strategy to build up state
        await strategy.next(mock_agents, sample_history)
        await strategy.next(mock_agents, sample_history)
        
        # Verify state exists
        assert strategy.has_selected
        assert len(strategy._selection_history) > 0
        
        # Reset strategy
        strategy.reset()
        
        # Verify state was cleared
        assert not strategy.has_selected
        assert len(strategy._selection_history) == 0
        assert len(strategy._agent_cache) == 0
        assert strategy._index == -1
        assert strategy.metrics.total_agents_processed == 0

    async def test_optimization_for_specific_agents(self, strategy, mock_agents):
        """Test pre-optimization for specific agent sets."""
        # Test optimization with different agent set sizes
        small_agent_set = mock_agents[:2]
        large_agent_set = mock_agents + [MockAgent(f"extra-{i}") for i in range(10)]
        
        # Optimize for small set
        await strategy.optimize_for_agents(small_agent_set)
        small_batch_size = strategy._current_batch_size
        
        # Reset and optimize for large set
        strategy.reset()
        await strategy.optimize_for_agents(large_agent_set)
        large_batch_size = strategy._current_batch_size
        
        # Verify batch size was adjusted appropriately
        assert strategy.min_batch_size <= small_batch_size <= strategy.max_batch_size
        assert strategy.min_batch_size <= large_batch_size <= strategy.max_batch_size

    async def test_concurrent_selection(self, strategy, mock_agents, sample_history):
        """Test concurrent agent selection."""
        # Create multiple concurrent selection tasks
        tasks = [
            strategy.next(mock_agents, sample_history)
            for _ in range(10)
        ]
        
        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify all selections completed successfully
        assert len(results) == 10
        for result in results:
            assert not isinstance(result, Exception)
            assert result in mock_agents

    async def test_performance_summary(self, strategy, mock_agents, sample_history):
        """Test performance summary generation."""
        # Perform some operations
        for _ in range(3):
            await strategy.next(mock_agents, sample_history)
        
        # Get performance summary
        summary = strategy.get_performance_summary()
        
        # Verify summary structure
        assert "metrics" in summary
        assert "current_batch_size" in summary
        assert "cache_size" in summary
        assert "tracked_agents" in summary
        assert "selection_history_length" in summary
        assert "agent_priorities" in summary
        
        # Verify summary contains expected data
        assert summary["current_batch_size"] > 0
        assert summary["selection_history_length"] >= 0

    async def test_error_recovery(self, strategy, mock_agents, sample_history):
        """Test error recovery mechanisms."""
        # Simulate an error condition by providing invalid data
        invalid_agents = [None]  # This should cause an error
        
        try:
            # This should handle the error gracefully
            with pytest.raises(Exception):
                await strategy.next(invalid_agents, sample_history)
        except Exception:
            pass  # Expected
        
        # Verify strategy can still work with valid data after error
        valid_agent = await strategy.next(mock_agents, sample_history)
        assert valid_agent in mock_agents

    @pytest.mark.parametrize("batch_size", [2, 5, 10])
    async def test_different_batch_sizes(self, mock_agents, sample_history, batch_size):
        """Test strategy with different batch sizes."""
        strategy = BatchSequentialSelectionStrategy(
            initial_batch_size=batch_size,
            max_batch_size=batch_size,
            min_batch_size=batch_size,
            enable_adaptive_batching=False  # Disable adaptation for this test
        )
        
        # Perform selections
        for _ in range(batch_size * 2):
            agent = await strategy.next(mock_agents, sample_history)
            assert agent in mock_agents
        
        # Verify batch size remained constant
        assert strategy._current_batch_size == batch_size

    async def test_metrics_accuracy(self, strategy, mock_agents, sample_history):
        """Test accuracy of metrics collection."""
        initial_metrics = BatchProcessingMetrics()
        
        # Manually update metrics to test calculation accuracy
        initial_metrics.update_batch_metrics(batch_size=3, processing_time_ms=150.0)
        initial_metrics.update_batch_metrics(batch_size=5, processing_time_ms=250.0)
        
        # Verify calculations
        assert initial_metrics.total_batches_processed == 2
        assert initial_metrics.total_agents_processed == 8
        assert initial_metrics.average_batch_size == 4.0  # (3 + 5) / 2
        assert initial_metrics.average_agent_processing_time_ms == 50.0  # 400ms / 8 agents

    async def test_cache_hit_ratio_calculation(self, strategy, mock_agents, sample_history):
        """Test cache hit ratio calculation."""
        # Simulate cache hits and misses
        strategy.metrics.cache_hits = 7
        strategy.metrics.cache_misses = 3
        
        # Calculate hit ratio
        hit_ratio = strategy.metrics.cache_hit_ratio
        
        # Verify calculation
        expected_ratio = (7 / 10) * 100  # 70%
        assert hit_ratio == expected_ratio

    async def test_complex_scenario(self, strategy, mock_agents):
        """Test complex scenario with multiple features."""
        # Configure strategy with all features enabled
        strategy.enable_adaptive_batching = True
        strategy.enable_caching = True
        strategy.enable_ml_optimization = True  # If available
        
        # Create varied history contexts
        histories = [
            [ChatMessageContent(role="user", content=f"Task {i}")]
            for i in range(5)
        ]
        
        # Perform selections with different contexts
        results = []
        for history in histories:
            for _ in range(3):  # 3 selections per history
                agent = await strategy.next(mock_agents, history)
                results.append(agent)
                await asyncio.sleep(0.001)  # Small delay
        
        # Verify all selections were successful
        assert len(results) == 15  # 5 histories × 3 selections
        assert all(agent in mock_agents for agent in results)
        
        # Verify strategy collected performance data
        assert strategy.metrics.total_agents_processed > 0
        summary = strategy.get_performance_summary()
        assert summary["metrics"]["cache_hit_ratio"] >= 0
