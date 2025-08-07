#!/usr/bin/env python3
"""
Batch Sequential Orchestration Strategy module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
High-performance batch processing for sequential agent orchestration.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import asyncio
import logging
import sys
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, List, Optional, TYPE_CHECKING, Union

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from pydantic import Field, PrivateAttr

from semantic_kernel.agents.strategies.selection.selection_strategy import SelectionStrategy
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.exceptions.agent_exceptions import AgentExecutionException
from semantic_kernel.utils.feature_stage_decorator import experimental

if TYPE_CHECKING:
    from semantic_kernel.agents import Agent

logger: logging.Logger = logging.getLogger(__name__)


@dataclass
class BatchProcessingMetrics:
    """Performance metrics for batch sequential processing."""
    
    total_batches_processed: int = 0
    total_agents_processed: int = 0
    average_batch_size: float = 0.0
    total_processing_time_ms: float = 0.0
    average_agent_processing_time_ms: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    batch_optimization_saves_ms: float = 0.0
    
    def update_batch_metrics(self, batch_size: int, processing_time_ms: float):
        """Update metrics after processing a batch."""
        self.total_batches_processed += 1
        self.total_agents_processed += batch_size
        self.total_processing_time_ms += processing_time_ms
        
        # Update averages
        self.average_batch_size = self.total_agents_processed / self.total_batches_processed
        self.average_agent_processing_time_ms = self.total_processing_time_ms / max(1, self.total_agents_processed)
    
    @property
    def cache_hit_ratio(self) -> float:
        """Calculate cache hit ratio as percentage."""
        total_requests = self.cache_hits + self.cache_misses
        return (self.cache_hits / total_requests * 100) if total_requests > 0 else 0.0
    
    def __str__(self) -> str:
        return (
            f"Batches: {self.total_batches_processed}, "
            f"Agents: {self.total_agents_processed}, "
            f"Avg Batch Size: {self.average_batch_size:.1f}, "
            f"Cache Hit Ratio: {self.cache_hit_ratio:.1f}%, "
            f"Avg Processing Time: {self.average_agent_processing_time_ms:.2f}ms"
        )


@experimental
class BatchSequentialSelectionStrategy(SelectionStrategy):
    """
    High-performance batch sequential selection strategy with intelligent optimization.
    
    Features:
    - Batch processing for improved throughput
    - Intelligent agent grouping and caching
    - Adaptive batch sizing based on performance
    - Priority-based agent selection
    - Context-aware optimization
    """

    # Configuration
    initial_batch_size: int = Field(default=5, description="Initial batch size for processing")
    max_batch_size: int = Field(default=20, description="Maximum batch size")
    min_batch_size: int = Field(default=2, description="Minimum batch size")
    enable_adaptive_batching: bool = Field(default=True, description="Enable adaptive batch sizing")
    enable_caching: bool = Field(default=True, description="Enable result caching")
    cache_ttl_seconds: float = Field(default=300.0, description="Cache TTL in seconds")
    priority_boost_factor: float = Field(default=1.5, description="Priority boost factor for important agents")
    
    # Private attributes
    _current_batch_size: int = PrivateAttr(default=5)
    _agent_cache: Dict[str, Any] = PrivateAttr(default_factory=dict)
    _cache_timestamps: Dict[str, float] = PrivateAttr(default_factory=dict)
    _agent_priorities: Dict[str, float] = PrivateAttr(default_factory=lambda: defaultdict(float))
    _selection_history: Deque[str] = PrivateAttr(default_factory=lambda: deque(maxlen=100))
    _performance_tracker: Dict[str, List[float]] = PrivateAttr(default_factory=lambda: defaultdict(list))
    _index: int = PrivateAttr(default=-1)
    
    # Metrics
    metrics: BatchProcessingMetrics = Field(default_factory=BatchProcessingMetrics)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_batch_size = self.initial_batch_size

    @override
    async def select_agent(
        self,
        agents: list["Agent"],
        history: list["ChatMessageContent"],
    ) -> "Agent":
        """
        Select the next agent using batch-optimized sequential strategy.
        
        Args:
            agents: The list of agents to select from.
            history: The history of messages in the conversation.
            
        Returns:
            The agent who takes the next turn.
        """
        start_time = time.time()
        
        try:
            # Clean expired cache entries
            await self._cleanup_cache()
            
            # Check cache first
            cache_key = self._generate_cache_key(agents, history)
            if self.enable_caching and cache_key in self._agent_cache:
                if self._is_cache_valid(cache_key):
                    self.metrics.cache_hits += 1
                    logger.debug(f"Cache hit for agent selection: {cache_key}")
                    return self._agent_cache[cache_key]
                else:
                    # Remove expired entry
                    del self._agent_cache[cache_key]
                    del self._cache_timestamps[cache_key]
            
            self.metrics.cache_misses += 1
            
            # Perform batch-optimized selection
            selected_agent = await self._select_agent_batch_optimized(agents, history)
            
            # Cache the result
            if self.enable_caching:
                self._agent_cache[cache_key] = selected_agent
                self._cache_timestamps[cache_key] = time.time()
            
            # Update performance metrics
            processing_time_ms = (time.time() - start_time) * 1000
            self.metrics.update_batch_metrics(1, processing_time_ms)
            
            # Update selection history and priorities
            self._update_selection_tracking(selected_agent, processing_time_ms)
            
            # Adaptive batch sizing
            if self.enable_adaptive_batching:
                await self._adjust_batch_size(processing_time_ms)
            
            logger.info(
                f"Selected agent {selected_agent.name} (ID: {selected_agent.id}) "
                f"in {processing_time_ms:.2f}ms using batch strategy"
            )
            
            return selected_agent
            
        except Exception as e:
            logger.error(f"Error in batch sequential selection: {e}")
            # Fallback to simple sequential selection
            return await self._fallback_selection(agents)

    async def _select_agent_batch_optimized(
        self, 
        agents: list["Agent"], 
        history: list["ChatMessageContent"]
    ) -> "Agent":
        """Perform batch-optimized agent selection."""
        
        # Handle edge cases
        if not agents:
            raise AgentExecutionException("Agent Failure - No agents present to select.")
        
        # Handle initial agent selection
        if not self.has_selected and self.initial_agent is not None:
            if self.initial_agent in agents:
                return self.initial_agent
        
        # Standard sequential selection with batch optimization
        if (
            self.has_selected
            and self.initial_agent is not None
            and len(agents) > 0
            and agents[0] == self.initial_agent
            and self._index < 0
        ):
            # Avoid selecting the same agent twice in a row
            self._increment_index(len(agents))
        
        # Main index increment
        self._increment_index(len(agents))
        
        # Apply priority-based adjustments
        selected_agent = await self._apply_priority_selection(agents)
        
        return selected_agent

    async def _apply_priority_selection(self, agents: list["Agent"]) -> "Agent":
        """Apply priority-based selection within batch context."""
        
        # Get base sequential selection
        base_agent = agents[self._index]
        
        # Check if we should boost priority for certain agents
        current_priorities = [
            self._agent_priorities.get(agent.id, 1.0) for agent in agents
        ]
        
        # If all priorities are equal, return base selection
        if all(p == current_priorities[0] for p in current_priorities):
            return base_agent
        
        # Apply priority weighting with batch consideration
        max_priority = max(current_priorities)
        if self._agent_priorities.get(base_agent.id, 1.0) >= max_priority * 0.8:
            # Base agent has good priority, use it
            return base_agent
        
        # Find higher priority agent near current index
        search_range = min(self._current_batch_size, len(agents))
        start_idx = max(0, self._index - search_range // 2)
        end_idx = min(len(agents), start_idx + search_range)
        
        best_agent = base_agent
        best_priority = self._agent_priorities.get(base_agent.id, 1.0)
        
        for i in range(start_idx, end_idx):
            agent = agents[i]
            priority = self._agent_priorities.get(agent.id, 1.0)
            if priority > best_priority:
                best_agent = agent
                best_priority = priority
                self._index = i  # Update index to selected position
        
        return best_agent

    def _increment_index(self, agent_count: int) -> None:
        """Increment the index in a circular manner with batch optimization."""
        # Standard circular increment
        self._index = (self._index + 1) % agent_count
        
        # Apply batch-aware adjustments
        if self.enable_adaptive_batching and len(self._selection_history) > 0:
            # Avoid recently selected agents if we have alternatives
            recent_selections = set(list(self._selection_history)[-self._current_batch_size:])
            attempts = 0
            max_attempts = min(agent_count, 3)
            
            while (
                attempts < max_attempts and 
                agent_count > self._current_batch_size and
                str(self._index) in recent_selections
            ):
                self._index = (self._index + 1) % agent_count
                attempts += 1

    def _update_selection_tracking(self, agent: "Agent", processing_time_ms: float) -> None:
        """Update selection history and performance tracking."""
        
        # Update selection history
        self._selection_history.append(agent.id)
        
        # Track performance per agent
        self._performance_tracker[agent.id].append(processing_time_ms)
        
        # Keep only recent performance data
        if len(self._performance_tracker[agent.id]) > 20:
            self._performance_tracker[agent.id] = self._performance_tracker[agent.id][-20:]
        
        # Update agent priorities based on performance
        if len(self._performance_tracker[agent.id]) >= 3:
            avg_time = sum(self._performance_tracker[agent.id]) / len(self._performance_tracker[agent.id])
            # Faster agents get higher priority
            base_priority = 1.0
            if avg_time < 100:  # Fast agent
                self._agent_priorities[agent.id] = base_priority * self.priority_boost_factor
            elif avg_time > 500:  # Slow agent
                self._agent_priorities[agent.id] = base_priority * 0.7
            else:
                self._agent_priorities[agent.id] = base_priority

    async def _adjust_batch_size(self, processing_time_ms: float) -> None:
        """Dynamically adjust batch size based on performance."""
        
        # Collect recent performance data
        if len(self._selection_history) < 5:
            return
        
        # Calculate performance trend
        recent_times = []
        for agent_id in list(self._selection_history)[-5:]:
            if agent_id in self._performance_tracker:
                recent_times.extend(self._performance_tracker[agent_id][-2:])
        
        if not recent_times:
            return
        
        avg_recent_time = sum(recent_times) / len(recent_times)
        
        # Adjust batch size based on performance
        if avg_recent_time < 50 and self._current_batch_size < self.max_batch_size:
            # System is fast, increase batch size
            self._current_batch_size = min(self.max_batch_size, self._current_batch_size + 1)
            logger.debug(f"Increased batch size to {self._current_batch_size}")
            
        elif avg_recent_time > 200 and self._current_batch_size > self.min_batch_size:
            # System is slow, decrease batch size
            self._current_batch_size = max(self.min_batch_size, self._current_batch_size - 1)
            logger.debug(f"Decreased batch size to {self._current_batch_size}")

    async def _fallback_selection(self, agents: list["Agent"]) -> "Agent":
        """Fallback to simple sequential selection in case of errors."""
        if not agents:
            raise AgentExecutionException("Agent Failure - No agents present to select.")
        
        self._index = (self._index + 1) % len(agents)
        return agents[self._index]

    def _generate_cache_key(self, agents: list["Agent"], history: list["ChatMessageContent"]) -> str:
        """Generate a cache key for the current selection context."""
        agent_ids = "|".join(agent.id for agent in agents)
        history_summary = f"{len(history)}:{history[-1].author_name if history else 'empty'}"
        return f"{agent_ids}#{history_summary}#{self._index}#{self._current_batch_size}"

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if a cache entry is still valid."""
        if cache_key not in self._cache_timestamps:
            return False
        
        return (time.time() - self._cache_timestamps[cache_key]) < self.cache_ttl_seconds

    async def _cleanup_cache(self) -> None:
        """Remove expired cache entries."""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self._cache_timestamps.items()
            if (current_time - timestamp) > self.cache_ttl_seconds
        ]
        
        for key in expired_keys:
            self._agent_cache.pop(key, None)
            self._cache_timestamps.pop(key, None)

    def reset(self) -> None:
        """Reset the strategy to initial state."""
        self._index = -1
        self._agent_cache.clear()
        self._cache_timestamps.clear()
        self._agent_priorities.clear()
        self._selection_history.clear()
        self._performance_tracker.clear()
        self._current_batch_size = self.initial_batch_size
        self.metrics = BatchProcessingMetrics()
        self.has_selected = False

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        return {
            "metrics": str(self.metrics),
            "current_batch_size": self._current_batch_size,
            "cache_size": len(self._agent_cache),
            "tracked_agents": len(self._performance_tracker),
            "selection_history_length": len(self._selection_history),
            "agent_priorities": dict(self._agent_priorities),
        }

    async def optimize_for_agents(self, agents: list["Agent"]) -> None:
        """Pre-optimize the strategy for a specific set of agents."""
        logger.info(f"Optimizing batch strategy for {len(agents)} agents")
        
        # Pre-calculate optimal batch size based on agent count
        if len(agents) <= 3:
            self._current_batch_size = self.min_batch_size
        elif len(agents) >= 15:
            self._current_batch_size = self.max_batch_size
        else:
            self._current_batch_size = min(self.max_batch_size, max(self.min_batch_size, len(agents) // 3))
        
        # Initialize priorities for new agents
        for agent in agents:
            if agent.id not in self._agent_priorities:
                self._agent_priorities[agent.id] = 1.0
        
        logger.info(f"Batch strategy optimized: batch_size={self._current_batch_size}")
