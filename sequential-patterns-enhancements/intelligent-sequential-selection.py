#!/usr/bin/env python3
"""
Intelligent Sequential Selection System

This module provides advanced sequential selection strategies that enhance
the existing Semantic Kernel selection capabilities with intelligent agent
coordination, adaptive selection algorithms, and performance optimization.

Features:
- Multi-criteria agent selection with dynamic weighting
- Learning-based selection strategies with historical optimization
- Context-aware selection with environmental adaptation
- Load balancing and performance-driven selection
- Fairness and diversity-aware selection algorithms
- Real-time selection strategy adaptation
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import uuid
import random
import statistics
from collections import defaultdict, deque
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SelectionStrategy(Enum):
    """Types of selection strategies."""
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    PERFORMANCE_BASED = "performance_based"
    LOAD_BALANCED = "load_balanced"
    CAPABILITY_MATCHED = "capability_matched"
    ADAPTIVE_LEARNING = "adaptive_learning"
    MULTI_CRITERIA = "multi_criteria"
    FAIRNESS_AWARE = "fairness_aware"
    DIVERSITY_OPTIMIZED = "diversity_optimized"

class AgentStatus(Enum):
    """Status of agents in the selection pool."""
    AVAILABLE = "available"
    BUSY = "busy"
    OVERLOADED = "overloaded"
    MAINTENANCE = "maintenance"
    FAILED = "failed"
    DISABLED = "disabled"

class SelectionCriteria(Enum):
    """Criteria for agent selection."""
    PERFORMANCE = "performance"
    AVAILABILITY = "availability"
    CAPABILITY = "capability"
    COST = "cost"
    RELIABILITY = "reliability"
    RESPONSE_TIME = "response_time"
    SUCCESS_RATE = "success_rate"
    SPECIALIZATION = "specialization"
    WORKLOAD = "workload"

@dataclass
class AgentCapability:
    """Represents an agent's capability in a specific area."""
    capability_id: str
    name: str
    proficiency_level: float  # 0.0 to 1.0
    experience_count: int = 0
    last_used: Optional[float] = None
    success_rate: float = 1.0
    average_response_time: float = 1.0

@dataclass
class AgentProfile:
    """Comprehensive profile of an agent for selection purposes."""
    agent_id: str
    name: str
    
    # Capabilities and specializations
    capabilities: Dict[str, AgentCapability] = field(default_factory=dict)
    specializations: Set[str] = field(default_factory=set)
    
    # Performance metrics
    overall_performance_score: float = 1.0
    recent_performance_scores: deque = field(default_factory=lambda: deque(maxlen=50))
    success_rate: float = 1.0
    average_response_time: float = 1.0
    
    # Availability and load
    status: AgentStatus = AgentStatus.AVAILABLE
    current_load: float = 0.0  # 0.0 to 1.0
    max_concurrent_tasks: int = 1
    active_tasks: int = 0
    
    # Cost and resource information
    cost_per_task: float = 1.0
    resource_requirements: Dict[str, float] = field(default_factory=dict)
    
    # Historical data
    total_tasks_completed: int = 0
    total_execution_time: float = 0.0
    last_selection_time: Optional[float] = None
    selection_count: int = 0
    
    # Learning and adaptation data
    learning_rate: float = 0.1
    adaptation_history: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class SelectionContext:
    """Context information for agent selection decisions."""
    task_type: str
    required_capabilities: Set[str] = field(default_factory=set)
    priority: int = 0
    deadline: Optional[float] = None
    resource_constraints: Dict[str, float] = field(default_factory=dict)
    performance_requirements: Dict[str, float] = field(default_factory=dict)
    context_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SelectionResult:
    """Result of an agent selection operation."""
    selected_agent: Optional[AgentProfile]
    selection_score: float
    selection_rationale: str
    alternative_agents: List[Tuple[AgentProfile, float]] = field(default_factory=list)
    selection_time: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SelectionMetrics:
    """Metrics for monitoring selection performance."""
    total_selections: int = 0
    successful_selections: int = 0
    failed_selections: int = 0
    average_selection_time: float = 0.0
    
    # Fairness metrics
    agent_selection_counts: Dict[str, int] = field(default_factory=dict)
    selection_distribution_variance: float = 0.0
    
    # Performance metrics
    average_task_performance: float = 0.0
    selection_accuracy: float = 0.0  # How often the selected agent performs well
    
    # Adaptation metrics
    strategy_adaptations: int = 0
    learning_improvements: float = 0.0

class BaseSelectionStrategy(ABC):
    """Base class for agent selection strategies."""
    
    def __init__(self, name: str):
        self.name = name
        self.metrics = SelectionMetrics()
        self.selection_history: deque = deque(maxlen=1000)
    
    @abstractmethod
    async def select_agent(self, 
                         agents: List[AgentProfile],
                         context: SelectionContext) -> SelectionResult:
        """Select an agent from the available pool."""
        pass
    
    def update_performance(self, 
                         agent: AgentProfile,
                         task_result: Dict[str, Any]) -> None:
        """Update agent performance based on task results."""
        # Update agent's performance metrics
        if 'success' in task_result:
            success = task_result['success']
            agent.total_tasks_completed += 1
            
            # Update success rate
            total_attempts = len(agent.recent_performance_scores) + 1
            current_successes = sum(agent.recent_performance_scores) + (1.0 if success else 0.0)
            agent.success_rate = current_successes / total_attempts
            
            # Add to recent performance
            agent.recent_performance_scores.append(1.0 if success else 0.0)
        
        if 'execution_time' in task_result:
            execution_time = task_result['execution_time']
            agent.total_execution_time += execution_time
            
            # Update average response time
            agent.average_response_time = (
                agent.total_execution_time / agent.total_tasks_completed
                if agent.total_tasks_completed > 0 else execution_time
            )
        
        # Update overall performance score
        agent.overall_performance_score = self._calculate_performance_score(agent)
    
    def _calculate_performance_score(self, agent: AgentProfile) -> float:
        """Calculate overall performance score for an agent."""
        # Weighted combination of success rate and response time
        success_weight = 0.7
        speed_weight = 0.3
        
        success_score = agent.success_rate
        
        # Speed score (higher is better, so invert response time)
        max_response_time = 10.0  # Normalize against max expected response time
        speed_score = max(0.0, 1.0 - (agent.average_response_time / max_response_time))
        
        return success_score * success_weight + speed_score * speed_weight
    
    def get_available_agents(self, agents: List[AgentProfile]) -> List[AgentProfile]:
        """Filter agents that are available for selection."""
        return [agent for agent in agents 
                if agent.status == AgentStatus.AVAILABLE and agent.current_load < 1.0]

class RoundRobinSelectionStrategy(BaseSelectionStrategy):
    """Enhanced round-robin selection with fairness tracking."""
    
    def __init__(self):
        super().__init__("RoundRobin")
        self.current_index = 0
        self.fairness_threshold = 0.2  # Maximum allowed variance in selection distribution
    
    async def select_agent(self, 
                         agents: List[AgentProfile],
                         context: SelectionContext) -> SelectionResult:
        """Select agent using round-robin with fairness consideration."""
        available_agents = self.get_available_agents(agents)
        
        if not available_agents:
            return SelectionResult(
                selected_agent=None,
                selection_score=0.0,
                selection_rationale="No agents available"
            )
        
        # Adjust index if needed
        if self.current_index >= len(available_agents):
            self.current_index = 0
        
        # Check for fairness violations
        if self._check_fairness_violation(available_agents):
            # Select least recently used agent instead
            selected_agent = min(available_agents, 
                               key=lambda a: a.last_selection_time or 0)
            rationale = "Fairness-adjusted round-robin selection"
        else:
            # Normal round-robin
            selected_agent = available_agents[self.current_index]
            self.current_index = (self.current_index + 1) % len(available_agents)
            rationale = f"Round-robin selection (index {self.current_index - 1})"
        
        # Update selection tracking
        selected_agent.last_selection_time = time.time()
        selected_agent.selection_count += 1
        
        return SelectionResult(
            selected_agent=selected_agent,
            selection_score=1.0,  # All agents are equally good in round-robin
            selection_rationale=rationale
        )
    
    def _check_fairness_violation(self, agents: List[AgentProfile]) -> bool:
        """Check if selection distribution violates fairness threshold."""
        if len(agents) < 2:
            return False
        
        selection_counts = [agent.selection_count for agent in agents]
        if max(selection_counts) == 0:
            return False
        
        # Calculate coefficient of variation
        mean_selections = statistics.mean(selection_counts)
        if mean_selections == 0:
            return False
        
        std_selections = statistics.stdev(selection_counts)
        cv = std_selections / mean_selections
        
        return cv > self.fairness_threshold

class PerformanceBasedSelectionStrategy(BaseSelectionStrategy):
    """Selection strategy based on agent performance metrics."""
    
    def __init__(self, performance_weight: float = 0.8):
        super().__init__("PerformanceBased")
        self.performance_weight = performance_weight
        self.recency_weight = 1.0 - performance_weight
    
    async def select_agent(self, 
                         agents: List[AgentProfile],
                         context: SelectionContext) -> SelectionResult:
        """Select agent based on performance scores."""
        available_agents = self.get_available_agents(agents)
        
        if not available_agents:
            return SelectionResult(
                selected_agent=None,
                selection_score=0.0,
                selection_rationale="No agents available"
            )
        
        # Score agents based on performance
        scored_agents = []
        for agent in available_agents:
            score = self._calculate_selection_score(agent, context)
            scored_agents.append((agent, score))
        
        # Sort by score (highest first)
        scored_agents.sort(key=lambda x: x[1], reverse=True)
        
        selected_agent, selection_score = scored_agents[0]
        alternatives = scored_agents[1:5]  # Top 5 alternatives
        
        return SelectionResult(
            selected_agent=selected_agent,
            selection_score=selection_score,
            selection_rationale=f"Performance-based selection (score: {selection_score:.3f})",
            alternative_agents=alternatives
        )
    
    def _calculate_selection_score(self, 
                                 agent: AgentProfile,
                                 context: SelectionContext) -> float:
        """Calculate selection score for an agent."""
        # Base performance score
        performance_score = agent.overall_performance_score
        
        # Recency bonus (prefer agents used recently - they might be "warmed up")
        recency_score = 0.5  # Default neutral score
        if agent.last_selection_time:
            time_since_last = time.time() - agent.last_selection_time
            # Give higher score to recently used agents (up to 1 hour)
            recency_score = max(0.0, 1.0 - (time_since_last / 3600.0))
        
        # Capability match bonus
        capability_score = self._calculate_capability_match(agent, context)
        
        # Load penalty
        load_penalty = agent.current_load
        
        # Combined score
        final_score = (
            performance_score * self.performance_weight +
            recency_score * self.recency_weight +
            capability_score * 0.2 -
            load_penalty * 0.1
        )
        
        return max(0.0, final_score)
    
    def _calculate_capability_match(self, 
                                  agent: AgentProfile,
                                  context: SelectionContext) -> float:
        """Calculate how well agent capabilities match task requirements."""
        if not context.required_capabilities:
            return 0.5  # Neutral score if no specific requirements
        
        matching_capabilities = 0
        total_proficiency = 0.0
        
        for required_cap in context.required_capabilities:
            if required_cap in agent.capabilities:
                matching_capabilities += 1
                total_proficiency += agent.capabilities[required_cap].proficiency_level
        
        if matching_capabilities == 0:
            return 0.0
        
        # Average proficiency of matching capabilities
        average_proficiency = total_proficiency / matching_capabilities
        
        # Coverage score (how many requirements are met)
        coverage_score = matching_capabilities / len(context.required_capabilities)
        
        return (average_proficiency + coverage_score) / 2.0

class AdaptiveLearningSelectionStrategy(BaseSelectionStrategy):
    """Selection strategy that learns and adapts from historical performance."""
    
    def __init__(self, learning_rate: float = 0.1):
        super().__init__("AdaptiveLearning")
        self.learning_rate = learning_rate
        self.agent_performance_models: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.context_patterns: Dict[str, List[float]] = defaultdict(list)
        self.exploration_rate = 0.1  # Epsilon for epsilon-greedy exploration
    
    async def select_agent(self, 
                         agents: List[AgentProfile],
                         context: SelectionContext) -> SelectionResult:
        """Select agent using adaptive learning algorithm."""
        available_agents = self.get_available_agents(agents)
        
        if not available_agents:
            return SelectionResult(
                selected_agent=None,
                selection_score=0.0,
                selection_rationale="No agents available"
            )
        
        # Exploration vs exploitation decision
        if random.random() < self.exploration_rate:
            # Exploration: select agent with least experience in this context
            selected_agent = self._select_for_exploration(available_agents, context)
            rationale = "Exploration-based selection"
        else:
            # Exploitation: select best predicted agent
            selected_agent = self._select_best_predicted(available_agents, context)
            rationale = "Prediction-based selection"
        
        # Calculate confidence score
        confidence = self._calculate_prediction_confidence(selected_agent, context)
        
        return SelectionResult(
            selected_agent=selected_agent,
            selection_score=confidence,
            selection_rationale=rationale,
            metadata={'exploration': random.random() < self.exploration_rate}
        )
    
    def _select_for_exploration(self, 
                              agents: List[AgentProfile],
                              context: SelectionContext) -> AgentProfile:
        """Select agent for exploration (least experience in context)."""
        context_key = self._get_context_key(context)
        
        # Score agents by inexperience (lower experience = higher exploration value)
        exploration_scores = []
        for agent in agents:
            experience = self.agent_performance_models[agent.agent_id].get(context_key, 0.0)
            exploration_score = 1.0 / (1.0 + experience)  # Higher score for less experience
            exploration_scores.append((agent, exploration_score))
        
        # Select agent with highest exploration score
        exploration_scores.sort(key=lambda x: x[1], reverse=True)
        return exploration_scores[0][0]
    
    def _select_best_predicted(self, 
                             agents: List[AgentProfile],
                             context: SelectionContext) -> AgentProfile:
        """Select agent with best predicted performance."""
        context_key = self._get_context_key(context)
        
        # Predict performance for each agent
        predictions = []
        for agent in agents:
            predicted_performance = self._predict_performance(agent, context_key)
            predictions.append((agent, predicted_performance))
        
        # Select agent with highest predicted performance
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[0][0]
    
    def _predict_performance(self, 
                           agent: AgentProfile,
                           context_key: str) -> float:
        """Predict agent performance for given context."""
        agent_model = self.agent_performance_models[agent.agent_id]
        
        if context_key in agent_model:
            # Use learned performance for this context
            return agent_model[context_key]
        else:
            # Use overall performance as baseline
            return agent.overall_performance_score
    
    def _calculate_prediction_confidence(self, 
                                       agent: AgentProfile,
                                       context: SelectionContext) -> float:
        """Calculate confidence in performance prediction."""
        context_key = self._get_context_key(context)
        agent_model = self.agent_performance_models[agent.agent_id]
        
        if context_key in agent_model:
            # High confidence if we have data for this context
            return 0.9
        else:
            # Lower confidence for new contexts
            return 0.5
    
    def _get_context_key(self, context: SelectionContext) -> str:
        """Generate a key for the context."""
        # Simplified context key based on task type and capabilities
        capabilities_str = ",".join(sorted(context.required_capabilities))
        return f"{context.task_type}:{capabilities_str}"
    
    def learn_from_outcome(self, 
                         agent: AgentProfile,
                         context: SelectionContext,
                         performance: float) -> None:
        """Learn from task outcome to improve future predictions."""
        context_key = self._get_context_key(context)
        agent_model = self.agent_performance_models[agent.agent_id]
        
        # Update performance model using exponential moving average
        if context_key in agent_model:
            current_estimate = agent_model[context_key]
            updated_estimate = (
                current_estimate * (1 - self.learning_rate) +
                performance * self.learning_rate
            )
        else:
            updated_estimate = performance
        
        agent_model[context_key] = updated_estimate
        
        # Update context patterns
        self.context_patterns[context_key].append(performance)
        
        # Adapt exploration rate based on learning progress
        self._adapt_exploration_rate()
    
    def _adapt_exploration_rate(self) -> None:
        """Adapt exploration rate based on learning progress."""
        # Decrease exploration rate as we learn more
        total_experiences = sum(len(patterns) for patterns in self.context_patterns.values())
        
        if total_experiences > 100:
            # Gradually reduce exploration as we gain more experience
            decay_factor = 0.99
            self.exploration_rate *= decay_factor
            self.exploration_rate = max(0.05, self.exploration_rate)  # Minimum exploration

class MultiCriteriaSelectionStrategy(BaseSelectionStrategy):
    """Selection strategy using multiple criteria with configurable weights."""
    
    def __init__(self, criteria_weights: Dict[SelectionCriteria, float] = None):
        super().__init__("MultiCriteria")
        self.criteria_weights = criteria_weights or {
            SelectionCriteria.PERFORMANCE: 0.3,
            SelectionCriteria.AVAILABILITY: 0.2,
            SelectionCriteria.CAPABILITY: 0.2,
            SelectionCriteria.RELIABILITY: 0.15,
            SelectionCriteria.RESPONSE_TIME: 0.1,
            SelectionCriteria.COST: 0.05
        }
        
        # Normalize weights
        total_weight = sum(self.criteria_weights.values())
        self.criteria_weights = {k: v/total_weight for k, v in self.criteria_weights.items()}
    
    async def select_agent(self, 
                         agents: List[AgentProfile],
                         context: SelectionContext) -> SelectionResult:
        """Select agent using multi-criteria decision analysis."""
        available_agents = self.get_available_agents(agents)
        
        if not available_agents:
            return SelectionResult(
                selected_agent=None,
                selection_score=0.0,
                selection_rationale="No agents available"
            )
        
        # Calculate scores for each criterion
        criterion_scores = {}
        for criterion in self.criteria_weights:
            criterion_scores[criterion] = self._calculate_criterion_scores(
                available_agents, criterion, context
            )
        
        # Calculate weighted total scores
        agent_scores = []
        for agent in available_agents:
            total_score = 0.0
            score_breakdown = {}
            
            for criterion, weight in self.criteria_weights.items():
                criterion_score = criterion_scores[criterion][agent.agent_id]
                score_breakdown[criterion.value] = criterion_score
                total_score += criterion_score * weight
            
            agent_scores.append((agent, total_score, score_breakdown))
        
        # Sort by total score
        agent_scores.sort(key=lambda x: x[1], reverse=True)
        
        selected_agent, selection_score, score_breakdown = agent_scores[0]
        alternatives = [(agent, score) for agent, score, _ in agent_scores[1:5]]
        
        # Create detailed rationale
        rationale = f"Multi-criteria selection (score: {selection_score:.3f})"
        top_criteria = sorted(score_breakdown.items(), key=lambda x: x[1], reverse=True)[:3]
        rationale += f", top criteria: {', '.join(f'{k}:{v:.2f}' for k, v in top_criteria)}"
        
        return SelectionResult(
            selected_agent=selected_agent,
            selection_score=selection_score,
            selection_rationale=rationale,
            alternative_agents=alternatives,
            metadata={'score_breakdown': score_breakdown}
        )
    
    def _calculate_criterion_scores(self, 
                                  agents: List[AgentProfile],
                                  criterion: SelectionCriteria,
                                  context: SelectionContext) -> Dict[str, float]:
        """Calculate scores for all agents on a specific criterion."""
        scores = {}
        
        if criterion == SelectionCriteria.PERFORMANCE:
            # Normalize performance scores
            performance_scores = [agent.overall_performance_score for agent in agents]
            max_score = max(performance_scores) if performance_scores else 1.0
            for agent in agents:
                scores[agent.agent_id] = agent.overall_performance_score / max_score
        
        elif criterion == SelectionCriteria.AVAILABILITY:
            # Availability based on current load
            for agent in agents:
                scores[agent.agent_id] = 1.0 - agent.current_load
        
        elif criterion == SelectionCriteria.CAPABILITY:
            # Capability match with requirements
            for agent in agents:
                scores[agent.agent_id] = self._calculate_capability_match_score(agent, context)
        
        elif criterion == SelectionCriteria.RELIABILITY:
            # Based on success rate
            for agent in agents:
                scores[agent.agent_id] = agent.success_rate
        
        elif criterion == SelectionCriteria.RESPONSE_TIME:
            # Inverse of response time (normalized)
            response_times = [agent.average_response_time for agent in agents]
            max_time = max(response_times) if response_times else 1.0
            for agent in agents:
                scores[agent.agent_id] = 1.0 - (agent.average_response_time / max_time)
        
        elif criterion == SelectionCriteria.COST:
            # Inverse of cost (normalized)
            costs = [agent.cost_per_task for agent in agents]
            max_cost = max(costs) if costs else 1.0
            for agent in agents:
                scores[agent.agent_id] = 1.0 - (agent.cost_per_task / max_cost)
        
        else:
            # Default neutral score
            for agent in agents:
                scores[agent.agent_id] = 0.5
        
        return scores
    
    def _calculate_capability_match_score(self, 
                                        agent: AgentProfile,
                                        context: SelectionContext) -> float:
        """Calculate capability match score for multi-criteria analysis."""
        if not context.required_capabilities:
            return 1.0  # Perfect match if no specific requirements
        
        total_match_score = 0.0
        for required_cap in context.required_capabilities:
            if required_cap in agent.capabilities:
                capability = agent.capabilities[required_cap]
                # Score based on proficiency and experience
                proficiency_score = capability.proficiency_level
                experience_score = min(1.0, capability.experience_count / 10.0)
                match_score = (proficiency_score + experience_score) / 2.0
            else:
                match_score = 0.0
            
            total_match_score += match_score
        
        return total_match_score / len(context.required_capabilities)

class LoadBalancedSelectionStrategy(BaseSelectionStrategy):
    """Selection strategy that balances load across agents."""
    
    def __init__(self, load_threshold: float = 0.8):
        super().__init__("LoadBalanced")
        self.load_threshold = load_threshold
        self.load_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=20))
    
    async def select_agent(self, 
                         agents: List[AgentProfile],
                         context: SelectionContext) -> SelectionResult:
        """Select agent based on load balancing principles."""
        available_agents = self.get_available_agents(agents)
        
        if not available_agents:
            return SelectionResult(
                selected_agent=None,
                selection_score=0.0,
                selection_rationale="No agents available"
            )
        
        # Filter out overloaded agents
        balanced_agents = [agent for agent in available_agents 
                          if agent.current_load <= self.load_threshold]
        
        if not balanced_agents:
            # All agents are overloaded, select least loaded
            balanced_agents = [min(available_agents, key=lambda a: a.current_load)]
        
        # Calculate load balance scores
        load_scores = []
        for agent in balanced_agents:
            # Base score is inverse of current load
            load_score = 1.0 - agent.current_load
            
            # Historical load balance consideration
            avg_historical_load = self._get_average_historical_load(agent)
            historical_bonus = max(0.0, 0.5 - avg_historical_load)
            
            # Capacity utilization bonus (prefer agents with higher capacity)
            capacity_bonus = agent.max_concurrent_tasks / 10.0  # Normalize
            
            total_score = load_score + historical_bonus + capacity_bonus
            load_scores.append((agent, total_score))
        
        # Select agent with best load balance score
        load_scores.sort(key=lambda x: x[1], reverse=True)
        selected_agent, selection_score = load_scores[0]
        
        # Update load history
        self.load_history[selected_agent.agent_id].append(selected_agent.current_load)
        
        alternatives = load_scores[1:5]
        
        return SelectionResult(
            selected_agent=selected_agent,
            selection_score=selection_score,
            selection_rationale=f"Load-balanced selection (load: {selected_agent.current_load:.2f})",
            alternative_agents=alternatives
        )
    
    def _get_average_historical_load(self, agent: AgentProfile) -> float:
        """Get average historical load for an agent."""
        history = self.load_history[agent.agent_id]
        if not history:
            return 0.0
        return statistics.mean(history)

class IntelligentSequentialSelector:
    """Intelligent sequential selector that combines multiple strategies."""
    
    def __init__(self):
        self.strategies: Dict[SelectionStrategy, BaseSelectionStrategy] = {
            SelectionStrategy.ROUND_ROBIN: RoundRobinSelectionStrategy(),
            SelectionStrategy.PERFORMANCE_BASED: PerformanceBasedSelectionStrategy(),
            SelectionStrategy.ADAPTIVE_LEARNING: AdaptiveLearningSelectionStrategy(),
            SelectionStrategy.MULTI_CRITERIA: MultiCriteriaSelectionStrategy(),
            SelectionStrategy.LOAD_BALANCED: LoadBalancedSelectionStrategy()
        }
        
        self.current_strategy = SelectionStrategy.ADAPTIVE_LEARNING
        self.strategy_performance: Dict[SelectionStrategy, deque] = {
            strategy: deque(maxlen=100) for strategy in self.strategies
        }
        
        self.adaptation_enabled = True
        self.adaptation_threshold = 0.1  # Switch strategies if performance differs by this much
        
    async def select_agent(self, 
                         agents: List[AgentProfile],
                         context: SelectionContext,
                         strategy_override: Optional[SelectionStrategy] = None) -> SelectionResult:
        """Select agent using the current or specified strategy."""
        strategy_to_use = strategy_override or self.current_strategy
        strategy_impl = self.strategies[strategy_to_use]
        
        start_time = time.time()
        result = await strategy_impl.select_agent(agents, context)
        selection_time = time.time() - start_time
        
        # Update metrics
        strategy_impl.metrics.total_selections += 1
        strategy_impl.metrics.average_selection_time = (
            (strategy_impl.metrics.average_selection_time * 
             (strategy_impl.metrics.total_selections - 1) + selection_time) /
            strategy_impl.metrics.total_selections
        )
        
        # Add metadata
        result.metadata['strategy_used'] = strategy_to_use.value
        result.metadata['selection_time'] = selection_time
        
        return result
    
    def update_performance(self, 
                         selection_result: SelectionResult,
                         task_outcome: Dict[str, Any]) -> None:
        """Update performance metrics for the strategy that made the selection."""
        strategy_used = SelectionStrategy(selection_result.metadata.get('strategy_used'))
        strategy_impl = self.strategies[strategy_used]
        
        # Update agent performance
        if selection_result.selected_agent:
            strategy_impl.update_performance(selection_result.selected_agent, task_outcome)
        
        # Update strategy performance
        performance_score = task_outcome.get('performance_score', 0.5)
        self.strategy_performance[strategy_used].append(performance_score)
        
        # Update selection accuracy
        if 'success' in task_outcome:
            if task_outcome['success']:
                strategy_impl.metrics.successful_selections += 1
            else:
                strategy_impl.metrics.failed_selections += 1
            
            strategy_impl.metrics.selection_accuracy = (
                strategy_impl.metrics.successful_selections /
                strategy_impl.metrics.total_selections
            )
        
        # Learn from outcome if using adaptive strategy
        if (strategy_used == SelectionStrategy.ADAPTIVE_LEARNING and 
            isinstance(strategy_impl, AdaptiveLearningSelectionStrategy)):
            context = task_outcome.get('context')
            if context:
                strategy_impl.learn_from_outcome(
                    selection_result.selected_agent,
                    context,
                    performance_score
                )
        
        # Check if strategy adaptation is needed
        if self.adaptation_enabled:
            self._consider_strategy_adaptation()
    
    def _consider_strategy_adaptation(self) -> None:
        """Consider switching to a better performing strategy."""
        if len(self.strategy_performance[self.current_strategy]) < 10:
            return  # Need more data
        
        current_performance = statistics.mean(
            self.strategy_performance[self.current_strategy]
        )
        
        # Find best performing strategy
        best_strategy = self.current_strategy
        best_performance = current_performance
        
        for strategy, performances in self.strategy_performance.items():
            if len(performances) >= 10:
                avg_performance = statistics.mean(performances)
                if avg_performance > best_performance + self.adaptation_threshold:
                    best_strategy = strategy
                    best_performance = avg_performance
        
        # Switch if better strategy found
        if best_strategy != self.current_strategy:
            logger.info(f"Switching selection strategy from {self.current_strategy.value} "
                       f"to {best_strategy.value} (performance improvement: "
                       f"{best_performance - current_performance:.3f})")
            self.current_strategy = best_strategy
            
            # Update adaptation metrics
            for strategy_impl in self.strategies.values():
                strategy_impl.metrics.strategy_adaptations += 1
    
    def get_strategy_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report for all strategies."""
        report = {
            'current_strategy': self.current_strategy.value,
            'strategies': {}
        }
        
        for strategy, strategy_impl in self.strategies.items():
            performances = self.strategy_performance[strategy]
            strategy_report = {
                'name': strategy.value,
                'metrics': {
                    'total_selections': strategy_impl.metrics.total_selections,
                    'successful_selections': strategy_impl.metrics.successful_selections,
                    'failed_selections': strategy_impl.metrics.failed_selections,
                    'selection_accuracy': strategy_impl.metrics.selection_accuracy,
                    'average_selection_time': strategy_impl.metrics.average_selection_time,
                    'strategy_adaptations': strategy_impl.metrics.strategy_adaptations
                }
            }
            
            if performances:
                strategy_report['performance'] = {
                    'average': statistics.mean(performances),
                    'std_dev': statistics.stdev(performances) if len(performances) > 1 else 0.0,
                    'min': min(performances),
                    'max': max(performances),
                    'recent_trend': statistics.mean(list(performances)[-10:]) if len(performances) >= 10 else None
                }
            
            report['strategies'][strategy.value] = strategy_report
        
        return report

# Example usage and demonstration
async def demo_intelligent_sequential_selection():
    """Demonstrate the intelligent sequential selection system."""
    
    # Create sample agents with different profiles
    agents = [
        AgentProfile(
            agent_id="agent_1",
            name="Fast Response Agent",
            capabilities={
                "data_processing": AgentCapability("data_processing", "Data Processing", 0.9, 50),
                "analysis": AgentCapability("analysis", "Analysis", 0.7, 30)
            },
            overall_performance_score=0.85,
            success_rate=0.9,
            average_response_time=0.5,
            max_concurrent_tasks=3,
            cost_per_task=2.0
        ),
        AgentProfile(
            agent_id="agent_2",
            name="High Quality Agent",
            capabilities={
                "data_processing": AgentCapability("data_processing", "Data Processing", 0.95, 100),
                "validation": AgentCapability("validation", "Validation", 0.9, 80)
            },
            overall_performance_score=0.95,
            success_rate=0.98,
            average_response_time=1.2,
            max_concurrent_tasks=2,
            cost_per_task=4.0
        ),
        AgentProfile(
            agent_id="agent_3",
            name="Balanced Agent",
            capabilities={
                "analysis": AgentCapability("analysis", "Analysis", 0.8, 40),
                "reporting": AgentCapability("reporting", "Reporting", 0.85, 60)
            },
            overall_performance_score=0.75,
            success_rate=0.85,
            average_response_time=0.8,
            max_concurrent_tasks=4,
            cost_per_task=3.0
        ),
        AgentProfile(
            agent_id="agent_4",
            name="Cost Effective Agent",
            capabilities={
                "data_processing": AgentCapability("data_processing", "Data Processing", 0.6, 20),
                "analysis": AgentCapability("analysis", "Analysis", 0.65, 25)
            },
            overall_performance_score=0.6,
            success_rate=0.8,
            average_response_time=1.5,
            max_concurrent_tasks=5,
            cost_per_task=1.0
        )
    ]
    
    # Create different selection contexts
    contexts = [
        SelectionContext(
            task_type="data_processing",
            required_capabilities={"data_processing"},
            priority=8,
            performance_requirements={"min_success_rate": 0.9}
        ),
        SelectionContext(
            task_type="analysis",
            required_capabilities={"analysis"},
            priority=6,
            performance_requirements={"max_response_time": 1.0}
        ),
        SelectionContext(
            task_type="validation",
            required_capabilities={"validation"},
            priority=9,
            performance_requirements={"min_success_rate": 0.95}
        ),
        SelectionContext(
            task_type="reporting",
            required_capabilities={"reporting"},
            priority=4,
            resource_constraints={"max_cost": 2.5}
        )
    ]
    
    print("🚀 Starting Intelligent Sequential Selection Demo")
    print("=" * 60)
    
    # Initialize selector
    selector = IntelligentSequentialSelector()
    
    # Test different strategies
    strategies_to_test = [
        SelectionStrategy.ROUND_ROBIN,
        SelectionStrategy.PERFORMANCE_BASED,
        SelectionStrategy.MULTI_CRITERIA,
        SelectionStrategy.LOAD_BALANCED,
        SelectionStrategy.ADAPTIVE_LEARNING
    ]
    
    print("\n📊 Testing Different Selection Strategies")
    print("-" * 50)
    
    for strategy in strategies_to_test:
        print(f"\n🔧 Testing {strategy.value} Strategy:")
        
        # Test strategy with different contexts
        strategy_results = []
        
        for i, context in enumerate(contexts):
            result = await selector.select_agent(agents, context, strategy_override=strategy)
            
            if result.selected_agent:
                print(f"  Task {i+1} ({context.task_type}): "
                      f"{result.selected_agent.name} "
                      f"(score: {result.selection_score:.3f})")
                
                # Simulate task execution and outcome
                task_outcome = {
                    'success': random.random() < result.selected_agent.success_rate,
                    'execution_time': result.selected_agent.average_response_time * random.uniform(0.8, 1.2),
                    'performance_score': result.selected_agent.overall_performance_score * random.uniform(0.9, 1.1),
                    'context': context
                }
                
                # Update performance
                selector.update_performance(result, task_outcome)
                strategy_results.append(task_outcome['performance_score'])
            else:
                print(f"  Task {i+1} ({context.task_type}): No agent available")
        
        # Show strategy performance
        if strategy_results:
            avg_performance = statistics.mean(strategy_results)
            print(f"  Average Performance: {avg_performance:.3f}")
    
    print("\n🧠 Testing Adaptive Learning")
    print("-" * 30)
    
    # Run extended simulation with adaptive learning
    for round_num in range(5):
        print(f"\nRound {round_num + 1}:")
        
        for context in contexts:
            # Use adaptive selector (will choose best strategy)
            result = await selector.select_agent(agents, context)
            
            if result.selected_agent:
                strategy_used = result.metadata.get('strategy_used', 'unknown')
                print(f"  {context.task_type}: {result.selected_agent.name} "
                      f"({strategy_used}, score: {result.selection_score:.3f})")
                
                # Simulate improving performance over time
                improvement_factor = 1.0 + round_num * 0.02  # 2% improvement per round
                task_outcome = {
                    'success': random.random() < (result.selected_agent.success_rate * improvement_factor),
                    'execution_time': result.selected_agent.average_response_time / improvement_factor,
                    'performance_score': result.selected_agent.overall_performance_score * improvement_factor,
                    'context': context
                }
                
                selector.update_performance(result, task_outcome)
    
    print("\n📈 Final Performance Report")
    print("-" * 40)
    
    performance_report = selector.get_strategy_performance_report()
    
    print(f"Current Strategy: {performance_report['current_strategy']}")
    print("\nStrategy Performance Summary:")
    
    for strategy_name, strategy_data in performance_report['strategies'].items():
        metrics = strategy_data['metrics']
        performance = strategy_data.get('performance', {})
        
        print(f"\n{strategy_name}:")
        print(f"  Selections: {metrics['total_selections']}")
        print(f"  Success Rate: {metrics['selection_accuracy']:.1%}")
        print(f"  Avg Selection Time: {metrics['average_selection_time']:.3f}s")
        
        if performance:
            print(f"  Avg Performance: {performance['average']:.3f}")
            if performance['recent_trend']:
                print(f"  Recent Trend: {performance['recent_trend']:.3f}")
    
    print("\n🎯 Intelligent Sequential Selection Demo Complete!")
    return performance_report

if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demo_intelligent_sequential_selection())
