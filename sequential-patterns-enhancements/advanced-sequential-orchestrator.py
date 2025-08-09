#!/usr/bin/env python3
"""
Advanced Sequential Orchestrator with Enhanced Coordination Patterns

This module provides advanced sequential orchestration capabilities that enhance
the existing Semantic Kernel sequential patterns with improved coordination,
error handling, and adaptive selection strategies.

Features:
- Adaptive sequential execution with dynamic flow control
- Advanced error recovery and retry mechanisms
- Context-aware agent selection with learning capabilities
- Performance monitoring and optimization
- Multi-tier sequential coordination patterns
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from collections import deque, defaultdict
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

class ExecutionStatus(Enum):
    """Execution status for sequential operations."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"

class CoordinationPattern(Enum):
    """Advanced coordination patterns for sequential execution."""
    LINEAR_SEQUENTIAL = "linear_sequential"  # Traditional sequential execution
    ADAPTIVE_SEQUENTIAL = "adaptive_sequential"  # Adapts based on performance
    CONDITIONAL_SEQUENTIAL = "conditional_sequential"  # Conditional branching
    PARALLEL_SEQUENTIAL = "parallel_sequential"  # Sequential groups in parallel
    HIERARCHICAL_SEQUENTIAL = "hierarchical_sequential"  # Nested sequential flows
    FEEDBACK_SEQUENTIAL = "feedback_sequential"  # Incorporates feedback loops

@dataclass
class ExecutionMetrics:
    """Metrics for monitoring sequential execution performance."""
    step_count: int = 0
    success_rate: float = 0.0
    average_duration: float = 0.0
    error_count: int = 0
    retry_count: int = 0
    throughput: float = 0.0
    coordination_efficiency: float = 0.0
    adaptation_score: float = 0.0
    
    def update_from_step(self, step_result: 'StepExecutionResult') -> None:
        """Update metrics from a step execution result."""
        self.step_count += 1
        if step_result.status == ExecutionStatus.SUCCESS:
            success_count = int(self.success_rate * (self.step_count - 1)) + 1
            self.success_rate = success_count / self.step_count
        
        # Update average duration
        if step_result.duration:
            total_duration = self.average_duration * (self.step_count - 1) + step_result.duration
            self.average_duration = total_duration / self.step_count
        
        if step_result.status == ExecutionStatus.FAILED:
            self.error_count += 1
        elif step_result.status == ExecutionStatus.RETRYING:
            self.retry_count += 1

@dataclass
class StepExecutionResult:
    """Result of executing a sequential step."""
    step_id: str
    status: ExecutionStatus
    result: Any = None
    error: Optional[Exception] = None
    duration: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    context_updates: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SequentialStep:
    """Enhanced sequential step with advanced coordination features."""
    step_id: str
    executor: Callable
    dependencies: List[str] = field(default_factory=list)
    conditions: List[Callable] = field(default_factory=list)
    retry_policy: Optional['RetryPolicy'] = None
    timeout: Optional[float] = None
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Advanced coordination features
    adaptive_config: Dict[str, Any] = field(default_factory=dict)
    performance_threshold: Optional[float] = None
    fallback_executor: Optional[Callable] = None

@dataclass
class RetryPolicy:
    """Retry policy for failed sequential steps."""
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_backoff: bool = True
    jitter: bool = True
    retry_conditions: List[Callable[[Exception], bool]] = field(default_factory=list)

class SequentialContext:
    """Enhanced context for sequential execution with learning capabilities."""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.step_history: List[StepExecutionResult] = []
        self.performance_history: deque = deque(maxlen=100)
        self.adaptation_data: Dict[str, Any] = {}
        self.coordination_patterns: Dict[str, float] = defaultdict(float)
        
    def set(self, key: str, value: Any) -> None:
        """Set a context value."""
        self.data[key] = value
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get a context value."""
        return self.data.get(key, default)
        
    def update(self, updates: Dict[str, Any]) -> None:
        """Update context with multiple values."""
        self.data.update(updates)
        
    def add_step_result(self, result: StepExecutionResult) -> None:
        """Add a step execution result to history."""
        self.step_history.append(result)
        
        # Update performance tracking
        if result.duration:
            self.performance_history.append({
                'step_id': result.step_id,
                'duration': result.duration,
                'status': result.status,
                'timestamp': time.time()
            })
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics from history."""
        if not self.performance_history:
            return {}
            
        durations = [p['duration'] for p in self.performance_history if p['status'] == ExecutionStatus.SUCCESS]
        if not durations:
            return {}
            
        return {
            'mean_duration': statistics.mean(durations),
            'median_duration': statistics.median(durations),
            'std_deviation': statistics.stdev(durations) if len(durations) > 1 else 0.0,
            'success_rate': len(durations) / len(self.performance_history)
        }

class AdaptiveSelectionStrategy(ABC):
    """Base class for adaptive selection strategies."""
    
    @abstractmethod
    async def select_next_step(self, 
                             available_steps: List[SequentialStep],
                             context: SequentialContext,
                             metrics: ExecutionMetrics) -> Optional[SequentialStep]:
        """Select the next step to execute."""
        pass
    
    @abstractmethod
    def learn_from_execution(self, 
                           step: SequentialStep, 
                           result: StepExecutionResult, 
                           context: SequentialContext) -> None:
        """Learn from step execution results."""
        pass

class PerformanceBasedSelectionStrategy(AdaptiveSelectionStrategy):
    """Selection strategy that adapts based on performance metrics."""
    
    def __init__(self):
        self.step_performance: Dict[str, List[float]] = defaultdict(list)
        self.step_weights: Dict[str, float] = defaultdict(lambda: 1.0)
        
    async def select_next_step(self, 
                             available_steps: List[SequentialStep],
                             context: SequentialContext,
                             metrics: ExecutionMetrics) -> Optional[SequentialStep]:
        """Select next step based on performance history and priorities."""
        if not available_steps:
            return None
            
        # Score steps based on performance and priority
        scored_steps = []
        for step in available_steps:
            # Check dependencies
            if not self._dependencies_satisfied(step, context):
                continue
                
            # Check conditions
            if not self._conditions_satisfied(step, context):
                continue
                
            # Calculate performance score
            performance_score = self._calculate_performance_score(step)
            priority_score = step.priority / 10.0  # Normalize priority
            
            # Adaptive weight based on recent performance
            adaptive_weight = self.step_weights.get(step.step_id, 1.0)
            
            total_score = (performance_score * 0.4 + 
                          priority_score * 0.3 + 
                          adaptive_weight * 0.3)
            
            scored_steps.append((step, total_score))
        
        if not scored_steps:
            return None
            
        # Select highest scoring step
        scored_steps.sort(key=lambda x: x[1], reverse=True)
        return scored_steps[0][0]
    
    def learn_from_execution(self, 
                           step: SequentialStep, 
                           result: StepExecutionResult, 
                           context: SequentialContext) -> None:
        """Update performance metrics and adaptive weights."""
        if result.duration:
            self.step_performance[step.step_id].append(result.duration)
            
            # Update adaptive weight based on performance
            recent_performances = self.step_performance[step.step_id][-5:]  # Last 5 executions
            if len(recent_performances) >= 3:
                avg_performance = statistics.mean(recent_performances)
                
                # Adjust weight based on performance trend
                if result.status == ExecutionStatus.SUCCESS and result.duration:
                    if result.duration < avg_performance:
                        self.step_weights[step.step_id] *= 1.1  # Increase weight for good performance
                    else:
                        self.step_weights[step.step_id] *= 0.95  # Decrease weight slightly
                elif result.status == ExecutionStatus.FAILED:
                    self.step_weights[step.step_id] *= 0.8  # Decrease weight for failures
                
                # Keep weights in reasonable bounds
                self.step_weights[step.step_id] = max(0.1, min(2.0, self.step_weights[step.step_id]))
    
    def _dependencies_satisfied(self, step: SequentialStep, context: SequentialContext) -> bool:
        """Check if step dependencies are satisfied."""
        for dep_id in step.dependencies:
            # Check if dependency was executed successfully
            dep_found = any(r.step_id == dep_id and r.status == ExecutionStatus.SUCCESS 
                          for r in context.step_history)
            if not dep_found:
                return False
        return True
    
    def _conditions_satisfied(self, step: SequentialStep, context: SequentialContext) -> bool:
        """Check if step conditions are satisfied."""
        for condition in step.conditions:
            if not condition(context):
                return False
        return True
    
    def _calculate_performance_score(self, step: SequentialStep) -> float:
        """Calculate performance score for a step."""
        performances = self.step_performance.get(step.step_id, [])
        if not performances:
            return 0.5  # Neutral score for new steps
            
        # Recent performance trend
        recent = performances[-3:] if len(performances) >= 3 else performances
        avg_performance = statistics.mean(recent)
        
        # Normalize to 0-1 scale (assuming 0-10 second range)
        normalized = max(0, min(1, 1 - (avg_performance / 10.0)))
        return normalized

class AdvancedSequentialOrchestrator:
    """Enhanced sequential orchestrator with advanced coordination patterns."""
    
    def __init__(self, 
                 coordination_pattern: CoordinationPattern = CoordinationPattern.ADAPTIVE_SEQUENTIAL,
                 selection_strategy: Optional[AdaptiveSelectionStrategy] = None,
                 max_concurrent_steps: int = 1,
                 global_timeout: Optional[float] = None):
        self.coordination_pattern = coordination_pattern
        self.selection_strategy = selection_strategy or PerformanceBasedSelectionStrategy()
        self.max_concurrent_steps = max_concurrent_steps
        self.global_timeout = global_timeout
        
        self.steps: Dict[str, SequentialStep] = {}
        self.execution_order: List[str] = []
        self.context = SequentialContext()
        self.metrics = ExecutionMetrics()
        
        # Advanced coordination state
        self.active_executions: Dict[str, asyncio.Task] = {}
        self.execution_semaphore = asyncio.Semaphore(max_concurrent_steps)
        
    def add_step(self, step: SequentialStep) -> None:
        """Add a step to the orchestration."""
        self.steps[step.step_id] = step
        logger.info(f"Added step: {step.step_id} with pattern: {self.coordination_pattern}")
    
    def add_steps(self, steps: List[SequentialStep]) -> None:
        """Add multiple steps to the orchestration."""
        for step in steps:
            self.add_step(step)
    
    async def execute(self, 
                     initial_context: Optional[Dict[str, Any]] = None,
                     progress_callback: Optional[Callable[[StepExecutionResult], None]] = None) -> Dict[str, Any]:
        """Execute the sequential orchestration with advanced coordination."""
        start_time = time.time()
        
        # Initialize context
        if initial_context:
            self.context.update(initial_context)
        
        logger.info(f"Starting sequential orchestration with pattern: {self.coordination_pattern}")
        
        try:
            # Execute based on coordination pattern
            if self.coordination_pattern == CoordinationPattern.LINEAR_SEQUENTIAL:
                await self._execute_linear()
            elif self.coordination_pattern == CoordinationPattern.ADAPTIVE_SEQUENTIAL:
                await self._execute_adaptive()
            elif self.coordination_pattern == CoordinationPattern.CONDITIONAL_SEQUENTIAL:
                await self._execute_conditional()
            elif self.coordination_pattern == CoordinationPattern.PARALLEL_SEQUENTIAL:
                await self._execute_parallel_sequential()
            elif self.coordination_pattern == CoordinationPattern.HIERARCHICAL_SEQUENTIAL:
                await self._execute_hierarchical()
            elif self.coordination_pattern == CoordinationPattern.FEEDBACK_SEQUENTIAL:
                await self._execute_feedback()
            else:
                await self._execute_adaptive()  # Default fallback
                
            # Update final metrics
            total_duration = time.time() - start_time
            self.metrics.throughput = self.metrics.step_count / total_duration if total_duration > 0 else 0
            self.metrics.coordination_efficiency = self._calculate_coordination_efficiency()
            self.metrics.adaptation_score = self._calculate_adaptation_score()
            
            logger.info(f"Sequential orchestration completed. Steps: {self.metrics.step_count}, "
                       f"Success rate: {self.metrics.success_rate:.2%}, "
                       f"Duration: {total_duration:.2f}s")
            
            return {
                'success': True,
                'results': {r.step_id: r.result for r in self.context.step_history 
                           if r.status == ExecutionStatus.SUCCESS},
                'metrics': self.metrics,
                'context': self.context.data,
                'execution_time': total_duration
            }
            
        except Exception as e:
            logger.error(f"Sequential orchestration failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'partial_results': {r.step_id: r.result for r in self.context.step_history 
                                  if r.status == ExecutionStatus.SUCCESS},
                'metrics': self.metrics,
                'context': self.context.data
            }
    
    async def _execute_linear(self) -> None:
        """Execute steps in linear sequential order."""
        remaining_steps = list(self.steps.values())
        
        while remaining_steps:
            # Find next executable step (dependencies satisfied)
            next_step = None
            for step in remaining_steps:
                if self._can_execute_step(step):
                    next_step = step
                    break
            
            if not next_step:
                # Check for circular dependencies or unsatisfiable conditions
                logger.warning("No executable steps found. Checking for issues...")
                break
                
            # Execute step
            result = await self._execute_step(next_step)
            remaining_steps.remove(next_step)
            
            # Stop on failure if no retry policy
            if result.status == ExecutionStatus.FAILED and not next_step.retry_policy:
                break
    
    async def _execute_adaptive(self) -> None:
        """Execute steps using adaptive selection strategy."""
        remaining_steps = list(self.steps.values())
        
        while remaining_steps:
            # Get available steps (dependencies and conditions satisfied)
            available_steps = [step for step in remaining_steps if self._can_execute_step(step)]
            
            if not available_steps:
                logger.warning("No available steps for adaptive execution")
                break
            
            # Use selection strategy to pick next step
            next_step = await self.selection_strategy.select_next_step(
                available_steps, self.context, self.metrics)
            
            if not next_step:
                logger.warning("Selection strategy returned no step")
                break
                
            # Execute step
            result = await self._execute_step(next_step)
            remaining_steps.remove(next_step)
            
            # Let strategy learn from execution
            self.selection_strategy.learn_from_execution(next_step, result, self.context)
            
            # Adaptive behavior: adjust based on performance
            if result.status == ExecutionStatus.SUCCESS and result.duration:
                self.context.coordination_patterns['adaptive_success'] += 1
            elif result.status == ExecutionStatus.FAILED:
                self.context.coordination_patterns['adaptive_failure'] += 1
    
    async def _execute_conditional(self) -> None:
        """Execute steps with conditional branching."""
        remaining_steps = list(self.steps.values())
        
        while remaining_steps:
            executed_any = False
            
            for step in remaining_steps[:]:  # Copy to avoid modification during iteration
                if self._can_execute_step(step):
                    # Check all conditions before execution
                    conditions_met = all(condition(self.context) for condition in step.conditions)
                    
                    if conditions_met:
                        result = await self._execute_step(step)
                        remaining_steps.remove(step)
                        executed_any = True
                        
                        # Conditional branching based on result
                        if result.status == ExecutionStatus.SUCCESS:
                            # Update context for conditional decisions
                            self.context.set(f"{step.step_id}_success", True)
                        else:
                            self.context.set(f"{step.step_id}_failed", True)
                        
                        break  # Re-evaluate conditions after each step
            
            if not executed_any:
                break
    
    async def _execute_parallel_sequential(self) -> None:
        """Execute sequential groups in parallel."""
        # Group steps by dependencies to identify parallel sequences
        step_groups = self._identify_parallel_groups()
        
        for group in step_groups:
            if len(group) == 1:
                # Single step execution
                result = await self._execute_step(group[0])
            else:
                # Execute group in parallel with sequential coordination within each branch
                tasks = []
                for step in group:
                    if self._can_execute_step(step):
                        task = asyncio.create_task(self._execute_step(step))
                        tasks.append(task)
                
                if tasks:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    for result in results:
                        if isinstance(result, Exception):
                            logger.error(f"Parallel execution error: {result}")
    
    async def _execute_hierarchical(self) -> None:
        """Execute with hierarchical sequential coordination."""
        # Organize steps into hierarchy based on dependencies
        hierarchy = self._build_dependency_hierarchy()
        
        # Execute levels sequentially, steps within level in parallel if possible
        for level_steps in hierarchy:
            if self.max_concurrent_steps > 1 and len(level_steps) > 1:
                # Execute level steps concurrently
                tasks = []
                for step in level_steps:
                    if self._can_execute_step(step):
                        task = asyncio.create_task(self._execute_step(step))
                        tasks.append(task)
                
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)
            else:
                # Execute level steps sequentially
                for step in level_steps:
                    if self._can_execute_step(step):
                        await self._execute_step(step)
    
    async def _execute_feedback(self) -> None:
        """Execute with feedback loops for continuous improvement."""
        remaining_steps = list(self.steps.values())
        feedback_threshold = 0.7  # Performance threshold for feedback
        
        while remaining_steps:
            # Select next step adaptively
            available_steps = [step for step in remaining_steps if self._can_execute_step(step)]
            if not available_steps:
                break
                
            next_step = await self.selection_strategy.select_next_step(
                available_steps, self.context, self.metrics)
            if not next_step:
                break
            
            # Execute with feedback monitoring
            result = await self._execute_step(next_step)
            remaining_steps.remove(next_step)
            
            # Feedback analysis
            if result.status == ExecutionStatus.SUCCESS and result.duration:
                performance_score = 1.0 / (1.0 + result.duration)  # Higher score for faster execution
                
                if performance_score < feedback_threshold:
                    # Poor performance - trigger feedback loop
                    logger.info(f"Performance feedback triggered for step {next_step.step_id}")
                    await self._apply_performance_feedback(next_step, result)
            
            # Learn from execution
            self.selection_strategy.learn_from_execution(next_step, result, self.context)
    
    async def _execute_step(self, step: SequentialStep) -> StepExecutionResult:
        """Execute a single step with enhanced error handling and monitoring."""
        step_start_time = time.time()
        
        logger.info(f"Executing step: {step.step_id}")
        
        async with self.execution_semaphore:  # Control concurrency
            try:
                # Check timeout
                timeout = step.timeout or self.global_timeout
                
                if timeout:
                    result = await asyncio.wait_for(
                        self._execute_step_with_retry(step), 
                        timeout=timeout
                    )
                else:
                    result = await self._execute_step_with_retry(step)
                
                # Calculate duration
                duration = time.time() - step_start_time
                result.duration = duration
                
                # Update context and metrics
                self.context.add_step_result(result)
                self.metrics.update_from_step(result)
                
                # Apply context updates from step
                if result.context_updates:
                    self.context.update(result.context_updates)
                
                logger.info(f"Step {step.step_id} completed with status: {result.status}")
                return result
                
            except asyncio.TimeoutError:
                duration = time.time() - step_start_time
                result = StepExecutionResult(
                    step_id=step.step_id,
                    status=ExecutionStatus.FAILED,
                    error=TimeoutError(f"Step {step.step_id} timed out after {timeout}s"),
                    duration=duration
                )
                self.context.add_step_result(result)
                self.metrics.update_from_step(result)
                logger.error(f"Step {step.step_id} timed out")
                return result
            
            except Exception as e:
                duration = time.time() - step_start_time
                result = StepExecutionResult(
                    step_id=step.step_id,
                    status=ExecutionStatus.FAILED,
                    error=e,
                    duration=duration
                )
                self.context.add_step_result(result)
                self.metrics.update_from_step(result)
                logger.error(f"Step {step.step_id} failed: {e}")
                return result
    
    async def _execute_step_with_retry(self, step: SequentialStep) -> StepExecutionResult:
        """Execute step with retry policy."""
        retry_policy = step.retry_policy
        attempt = 0
        last_error = None
        
        while True:
            try:
                # Execute the step
                if asyncio.iscoroutinefunction(step.executor):
                    result_data = await step.executor(self.context)
                else:
                    result_data = step.executor(self.context)
                
                # Success
                return StepExecutionResult(
                    step_id=step.step_id,
                    status=ExecutionStatus.SUCCESS,
                    result=result_data,
                    retry_count=attempt
                )
                
            except Exception as e:
                last_error = e
                attempt += 1
                
                # Check if we should retry
                if not retry_policy or attempt > retry_policy.max_retries:
                    # Check for fallback executor
                    if step.fallback_executor:
                        try:
                            logger.info(f"Using fallback executor for step {step.step_id}")
                            if asyncio.iscoroutinefunction(step.fallback_executor):
                                result_data = await step.fallback_executor(self.context)
                            else:
                                result_data = step.fallback_executor(self.context)
                            
                            return StepExecutionResult(
                                step_id=step.step_id,
                                status=ExecutionStatus.SUCCESS,
                                result=result_data,
                                retry_count=attempt,
                                metadata={'used_fallback': True}
                            )
                        except Exception as fallback_error:
                            logger.error(f"Fallback executor also failed: {fallback_error}")
                    
                    # Final failure
                    return StepExecutionResult(
                        step_id=step.step_id,
                        status=ExecutionStatus.FAILED,
                        error=last_error,
                        retry_count=attempt
                    )
                
                # Check retry conditions
                should_retry = True
                if retry_policy.retry_conditions:
                    should_retry = any(condition(e) for condition in retry_policy.retry_conditions)
                
                if not should_retry:
                    return StepExecutionResult(
                        step_id=step.step_id,
                        status=ExecutionStatus.FAILED,
                        error=last_error,
                        retry_count=attempt
                    )
                
                # Calculate retry delay
                delay = retry_policy.base_delay
                if retry_policy.exponential_backoff:
                    delay = min(retry_policy.base_delay * (2 ** (attempt - 1)), retry_policy.max_delay)
                
                if retry_policy.jitter:
                    import random
                    delay *= (0.5 + random.random() * 0.5)  # 50-100% of calculated delay
                
                logger.info(f"Retrying step {step.step_id} in {delay:.2f}s (attempt {attempt})")
                await asyncio.sleep(delay)
    
    def _can_execute_step(self, step: SequentialStep) -> bool:
        """Check if a step can be executed (dependencies and conditions satisfied)."""
        # Check dependencies
        for dep_id in step.dependencies:
            dep_satisfied = any(r.step_id == dep_id and r.status == ExecutionStatus.SUCCESS 
                              for r in self.context.step_history)
            if not dep_satisfied:
                return False
        
        # Check conditions
        for condition in step.conditions:
            if not condition(self.context):
                return False
                
        return True
    
    def _identify_parallel_groups(self) -> List[List[SequentialStep]]:
        """Identify groups of steps that can be executed in parallel."""
        # Simple implementation - group by dependency level
        groups = []
        remaining_steps = list(self.steps.values())
        
        while remaining_steps:
            current_group = []
            for step in remaining_steps[:]:
                if self._can_execute_step(step):
                    current_group.append(step)
                    remaining_steps.remove(step)
            
            if current_group:
                groups.append(current_group)
            else:
                # Avoid infinite loop if no progress
                break
                
        return groups
    
    def _build_dependency_hierarchy(self) -> List[List[SequentialStep]]:
        """Build dependency hierarchy for hierarchical execution."""
        levels = []
        remaining_steps = list(self.steps.values())
        executed_steps = set()
        
        while remaining_steps:
            current_level = []
            
            for step in remaining_steps[:]:
                # Check if all dependencies are in executed_steps
                deps_satisfied = all(dep_id in executed_steps for dep_id in step.dependencies)
                
                if deps_satisfied:
                    current_level.append(step)
                    remaining_steps.remove(step)
                    executed_steps.add(step.step_id)
            
            if current_level:
                levels.append(current_level)
            else:
                # Circular dependency or unsatisfiable condition
                logger.warning("Circular dependency detected or unsatisfiable conditions")
                break
                
        return levels
    
    async def _apply_performance_feedback(self, step: SequentialStep, result: StepExecutionResult) -> None:
        """Apply performance feedback to improve future executions."""
        # Simple feedback mechanism - adjust step configuration
        if step.adaptive_config:
            # Reduce timeout if performance is poor
            if 'timeout_multiplier' not in step.adaptive_config:
                step.adaptive_config['timeout_multiplier'] = 1.0
            
            if result.duration and step.timeout:
                if result.duration > step.timeout * 0.8:  # Close to timeout
                    step.adaptive_config['timeout_multiplier'] *= 1.2
                    step.timeout *= step.adaptive_config['timeout_multiplier']
                    logger.info(f"Increased timeout for step {step.step_id} to {step.timeout:.2f}s")
    
    def _calculate_coordination_efficiency(self) -> float:
        """Calculate coordination efficiency score."""
        if not self.context.step_history:
            return 0.0
            
        total_steps = len(self.context.step_history)
        successful_steps = sum(1 for r in self.context.step_history if r.status == ExecutionStatus.SUCCESS)
        
        success_ratio = successful_steps / total_steps if total_steps > 0 else 0
        
        # Factor in retry efficiency
        total_retries = sum(r.retry_count for r in self.context.step_history)
        retry_penalty = 1.0 / (1.0 + total_retries * 0.1)
        
        return success_ratio * retry_penalty
    
    def _calculate_adaptation_score(self) -> float:
        """Calculate adaptation score based on learning and improvement."""
        if not hasattr(self.selection_strategy, 'step_weights'):
            return 0.5  # Neutral score for non-adaptive strategies
            
        # Measure how much the strategy has adapted
        weights = self.selection_strategy.step_weights
        if not weights:
            return 0.5
            
        # Calculate variance in weights as adaptation indicator
        weight_values = list(weights.values())
        if len(weight_values) < 2:
            return 0.5
            
        weight_variance = statistics.variance(weight_values)
        # Normalize variance to 0-1 score (higher variance = more adaptation)
        adaptation_score = min(1.0, weight_variance / 0.5)
        
        return adaptation_score

# Example usage and demonstration
async def demo_advanced_sequential_orchestrator():
    """Demonstrate the advanced sequential orchestrator capabilities."""
    
    # Create orchestrator with adaptive coordination
    orchestrator = AdvancedSequentialOrchestrator(
        coordination_pattern=CoordinationPattern.ADAPTIVE_SEQUENTIAL,
        max_concurrent_steps=2,
        global_timeout=30.0
    )
    
    # Define sample steps with various features
    async def step_1(context):
        await asyncio.sleep(0.1)
        context.set('step_1_result', 'Step 1 completed')
        return {'data': 'result_1', 'processing_time': 0.1}
    
    async def step_2(context):
        await asyncio.sleep(0.2)
        context.set('step_2_result', 'Step 2 completed')
        return {'data': 'result_2', 'dependency': context.get('step_1_result')}
    
    def step_3_condition(context):
        return context.get('step_1_result') is not None
    
    async def step_3(context):
        await asyncio.sleep(0.15)
        return {'data': 'result_3', 'conditional': True}
    
    async def step_4_with_retry(context):
        # Simulate occasional failure for retry demonstration
        import random
        if random.random() < 0.3:  # 30% chance of failure
            raise Exception("Simulated failure for retry demo")
        await asyncio.sleep(0.1)
        return {'data': 'result_4', 'retried': True}
    
    # Create retry policy
    retry_policy = RetryPolicy(
        max_retries=3,
        base_delay=0.5,
        exponential_backoff=True,
        retry_conditions=[lambda e: "Simulated failure" in str(e)]
    )
    
    # Add steps to orchestrator
    orchestrator.add_steps([
        SequentialStep(
            step_id="init",
            executor=step_1,
            priority=10
        ),
        SequentialStep(
            step_id="process",
            executor=step_2,
            dependencies=["init"],
            priority=8
        ),
        SequentialStep(
            step_id="conditional_step",
            executor=step_3,
            conditions=[step_3_condition],
            priority=6
        ),
        SequentialStep(
            step_id="retry_step",
            executor=step_4_with_retry,
            dependencies=["process"],
            retry_policy=retry_policy,
            priority=5
        )
    ])
    
    # Execute orchestration
    print("🚀 Starting Advanced Sequential Orchestration Demo")
    print("=" * 60)
    
    initial_context = {'execution_id': 'demo_001', 'timestamp': time.time()}
    
    result = await orchestrator.execute(
        initial_context=initial_context,
        progress_callback=lambda step_result: print(f"  ✅ {step_result.step_id}: {step_result.status}")
    )
    
    # Display results
    print("\n📊 Execution Results:")
    print(f"  Success: {result['success']}")
    print(f"  Steps Executed: {orchestrator.metrics.step_count}")
    print(f"  Success Rate: {orchestrator.metrics.success_rate:.1%}")
    print(f"  Average Duration: {orchestrator.metrics.average_duration:.3f}s")
    print(f"  Coordination Efficiency: {orchestrator.metrics.coordination_efficiency:.3f}")
    print(f"  Adaptation Score: {orchestrator.metrics.adaptation_score:.3f}")
    
    if result['success']:
        print("\n📝 Step Results:")
        for step_id, step_result in result['results'].items():
            print(f"  {step_id}: {step_result}")
    
    return result

if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demo_advanced_sequential_orchestrator())
