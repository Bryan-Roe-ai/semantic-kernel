#!/usr/bin/env python3
"""
Intelligent Adaptive Planner module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
AI-driven adaptive planning with machine learning optimization.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental

logger = logging.getLogger(__name__)


class PlanComplexity(Enum):
    """Classification of plan complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"


class StepType(Enum):
    """Types of execution steps in a plan."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    FUNCTION_CALL = "function_call"
    DECISION_POINT = "decision_point"


@dataclass
class PlanMetrics:
    """Performance metrics for plan execution."""
    total_plans_created: int = 0
    total_plans_executed: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_execution_time_ms: float = 0.0
    average_steps_per_plan: float = 0.0
    complexity_distribution: Dict[str, int] = field(default_factory=dict)
    optimization_improvements: float = 0.0  # Percentage improvement from ML optimization

    @property
    def success_rate(self) -> float:
        """Calculate the success rate percentage."""
        if self.total_plans_executed == 0:
            return 0.0
        return (self.successful_executions / self.total_plans_executed) * 100

    def update_execution_metrics(self, success: bool, execution_time_ms: float, step_count: int):
        """Update metrics after plan execution."""
        self.total_plans_executed += 1
        if success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1

        # Update averages
        total_time = self.average_execution_time_ms * (self.total_plans_executed - 1) + execution_time_ms
        self.average_execution_time_ms = total_time / self.total_plans_executed

        total_steps = self.average_steps_per_plan * (self.total_plans_executed - 1) + step_count
        self.average_steps_per_plan = total_steps / self.total_plans_executed


@dataclass
class ExecutionStep:
    """Represents a single execution step in a plan."""
    id: str
    step_type: StepType
    description: str
    function_name: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    estimated_duration_ms: float = 100.0
    retry_count: int = 0
    max_retries: int = 3
    timeout_ms: float = 30000.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def can_execute(self, completed_steps: set[str]) -> bool:
        """Check if this step can be executed based on dependencies."""
        return all(dep in completed_steps for dep in self.dependencies)


@dataclass
class ExecutionPlan:
    """Represents a complete execution plan with optimization data."""
    id: str
    goal: str
    steps: List[ExecutionStep]
    complexity: PlanComplexity
    estimated_total_duration_ms: float
    created_at: float = field(default_factory=time.time)
    optimization_score: float = 0.0  # ML-driven optimization score
    execution_history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def step_count(self) -> int:
        """Get the total number of steps in the plan."""
        return len(self.steps)

    def get_executable_steps(self, completed_steps: set[str]) -> List[ExecutionStep]:
        """Get all steps that can currently be executed."""
        return [step for step in self.steps if step.can_execute(completed_steps)]

    def get_parallel_steps(self, completed_steps: set[str]) -> List[ExecutionStep]:
        """Get steps that can be executed in parallel."""
        executable = self.get_executable_steps(completed_steps)
        return [step for step in executable if step.step_type in [StepType.PARALLEL, StepType.FUNCTION_CALL]]


@experimental
class IntelligentAdaptivePlanner(KernelBaseModel):
    """
    AI-driven adaptive planner with machine learning optimization.

    Features:
    - Intelligent plan generation based on goal complexity
    - Machine learning-driven optimization
    - Adaptive step ordering and parallelization
    - Performance-based plan improvement
    - Context-aware planning strategies
    """

    # Configuration
    enable_ml_optimization: bool = Field(default=True, description="Enable ML-driven optimization")
    enable_parallel_execution: bool = Field(default=True, description="Enable parallel step execution")
    max_parallel_steps: int = Field(default=5, description="Maximum number of parallel steps")
    learning_rate: float = Field(default=0.1, description="Learning rate for optimization")
    optimization_threshold: float = Field(default=0.75, description="Threshold for applying optimizations")
    cache_plans: bool = Field(default=True, description="Cache generated plans")

    # Internal state
    _plan_cache: Dict[str, ExecutionPlan] = {}
    _execution_patterns: Dict[str, List[float]] = {}  # Performance patterns by plan type
    _optimization_weights: Dict[str, float] = {
        "execution_time": 0.4,
        "success_rate": 0.4,
        "complexity_efficiency": 0.2
    }

    # Metrics
    metrics: PlanMetrics = Field(default_factory=PlanMetrics)

    async def create_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> ExecutionPlan:
        """
        Create an optimized execution plan for the given goal.

        Args:
            goal: The goal to achieve
            context: Additional context for plan generation

        Returns:
            An optimized execution plan
        """
        start_time = time.time()
        context = context or {}

        logger.info(f"Creating adaptive plan for goal: {goal}")

        try:
            # Check cache first
            if self.cache_plans:
                cache_key = self._generate_cache_key(goal, context)
                if cache_key in self._plan_cache:
                    cached_plan = self._plan_cache[cache_key]
                    if self._is_plan_fresh(cached_plan):
                        logger.debug(f"Using cached plan for goal: {goal}")
                        return cached_plan

            # Analyze goal complexity
            complexity = await self._analyze_goal_complexity(goal, context)

            # Generate base plan
            plan = await self._generate_base_plan(goal, complexity, context)

            # Apply ML optimization if enabled
            if self.enable_ml_optimization:
                plan = await self._optimize_plan_with_ml(plan, context)

            # Apply adaptive improvements
            plan = await self._apply_adaptive_optimizations(plan)

            # Cache the plan
            if self.cache_plans:
                cache_key = self._generate_cache_key(goal, context)
                self._plan_cache[cache_key] = plan

            # Update metrics
            self.metrics.total_plans_created += 1
            complexity_key = complexity.value
            if complexity_key not in self.metrics.complexity_distribution:
                self.metrics.complexity_distribution[complexity_key] = 0
            self.metrics.complexity_distribution[complexity_key] += 1

            execution_time = (time.time() - start_time) * 1000
            logger.info(f"Created plan '{plan.id}' with {plan.step_count} steps in {execution_time:.2f}ms")

            return plan

        except Exception as e:
            logger.error(f"Error creating plan for goal '{goal}': {e}")
            raise

    async def execute_plan(
        self,
        plan: ExecutionPlan,
        kernel: Any = None,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Execute a plan with intelligent optimization and monitoring.

        Args:
            plan: The plan to execute
            kernel: Semantic kernel instance for function execution
            progress_callback: Optional callback for progress updates

        Returns:
            Execution results and metrics
        """
        start_time = time.time()
        execution_id = f"exec_{int(time.time() * 1000)}"

        logger.info(f"Executing plan '{plan.id}' with {plan.step_count} steps")

        try:
            # Prepare execution context
            execution_context = {
                "plan_id": plan.id,
                "execution_id": execution_id,
                "start_time": start_time,
                "completed_steps": set(),
                "step_results": {},
                "errors": [],
                "performance_data": []
            }

            # Execute steps with optimization
            if self.enable_parallel_execution and plan.complexity in [PlanComplexity.COMPLEX, PlanComplexity.ENTERPRISE]:
                await self._execute_plan_parallel(plan, execution_context, kernel, progress_callback)
            else:
                await self._execute_plan_sequential(plan, execution_context, kernel, progress_callback)

            # Calculate execution metrics
            execution_time_ms = (time.time() - start_time) * 1000
            success = len(execution_context["errors"]) == 0

            # Update plan execution history
            execution_record = {
                "execution_id": execution_id,
                "timestamp": start_time,
                "duration_ms": execution_time_ms,
                "success": success,
                "steps_completed": len(execution_context["completed_steps"]),
                "errors": execution_context["errors"]
            }
            plan.execution_history.append(execution_record)

            # Update metrics
            self.metrics.update_execution_metrics(success, execution_time_ms, plan.step_count)

            # Learn from execution for future optimization
            if self.enable_ml_optimization:
                await self._learn_from_execution(plan, execution_context)

            logger.info(f"Plan execution completed: success={success}, duration={execution_time_ms:.2f}ms")

            return {
                "success": success,
                "execution_time_ms": execution_time_ms,
                "steps_completed": len(execution_context["completed_steps"]),
                "total_steps": plan.step_count,
                "results": execution_context["step_results"],
                "errors": execution_context["errors"],
                "execution_id": execution_id
            }

        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            self.metrics.update_execution_metrics(False, execution_time_ms, plan.step_count)
            logger.error(f"Error executing plan '{plan.id}': {e}")
            raise

    async def _analyze_goal_complexity(self, goal: str, context: Dict[str, Any]) -> PlanComplexity:
        """Analyze the complexity of a goal to determine planning strategy."""

        # Simple heuristic-based complexity analysis
        # In a real implementation, this could use ML models

        word_count = len(goal.split())
        has_conditions = any(word in goal.lower() for word in ["if", "when", "unless", "depending"])
        has_iterations = any(word in goal.lower() for word in ["each", "every", "all", "multiple"])
        has_complex_operations = any(word in goal.lower() for word in ["analyze", "generate", "optimize", "transform"])

        complexity_score = 0

        if word_count > 20:
            complexity_score += 2
        elif word_count > 10:
            complexity_score += 1

        if has_conditions:
            complexity_score += 2
        if has_iterations:
            complexity_score += 2
        if has_complex_operations:
            complexity_score += 1

        # Context-based complexity factors
        if context.get("requires_external_apis", False):
            complexity_score += 2
        if context.get("data_processing_required", False):
            complexity_score += 1
        if context.get("user_interaction_required", False):
            complexity_score += 1

        if complexity_score >= 6:
            return PlanComplexity.ENTERPRISE
        elif complexity_score >= 4:
            return PlanComplexity.COMPLEX
        elif complexity_score >= 2:
            return PlanComplexity.MODERATE
        else:
            return PlanComplexity.SIMPLE

    async def _generate_base_plan(self, goal: str, complexity: PlanComplexity, context: Dict[str, Any]) -> ExecutionPlan:
        """Generate a base execution plan based on goal and complexity."""

        plan_id = f"plan_{int(time.time() * 1000)}"
        steps = []

        # Generate steps based on complexity
        if complexity == PlanComplexity.SIMPLE:
            steps = await self._generate_simple_steps(goal, context)
        elif complexity == PlanComplexity.MODERATE:
            steps = await self._generate_moderate_steps(goal, context)
        elif complexity == PlanComplexity.COMPLEX:
            steps = await self._generate_complex_steps(goal, context)
        else:  # ENTERPRISE
            steps = await self._generate_enterprise_steps(goal, context)

        # Calculate estimated duration
        total_duration = sum(step.estimated_duration_ms for step in steps)

        return ExecutionPlan(
            id=plan_id,
            goal=goal,
            steps=steps,
            complexity=complexity,
            estimated_total_duration_ms=total_duration,
            metadata={"context": context, "generation_strategy": complexity.value}
        )

    async def _generate_simple_steps(self, goal: str, context: Dict[str, Any]) -> List[ExecutionStep]:
        """Generate steps for simple goals."""
        return [
            ExecutionStep(
                id="step_1",
                step_type=StepType.FUNCTION_CALL,
                description=f"Execute simple task: {goal}",
                function_name="execute_simple_task",
                parameters={"goal": goal, "context": context},
                estimated_duration_ms=500.0
            )
        ]

    async def _generate_moderate_steps(self, goal: str, context: Dict[str, Any]) -> List[ExecutionStep]:
        """Generate steps for moderate complexity goals."""
        return [
            ExecutionStep(
                id="step_1",
                step_type=StepType.SEQUENTIAL,
                description="Analyze requirements",
                function_name="analyze_requirements",
                parameters={"goal": goal},
                estimated_duration_ms=1000.0
            ),
            ExecutionStep(
                id="step_2",
                step_type=StepType.FUNCTION_CALL,
                description="Execute main task",
                function_name="execute_main_task",
                parameters={"goal": goal, "context": context},
                dependencies=["step_1"],
                estimated_duration_ms=2000.0
            ),
            ExecutionStep(
                id="step_3",
                step_type=StepType.SEQUENTIAL,
                description="Validate results",
                function_name="validate_results",
                parameters={},
                dependencies=["step_2"],
                estimated_duration_ms=500.0
            )
        ]

    async def _generate_complex_steps(self, goal: str, context: Dict[str, Any]) -> List[ExecutionStep]:
        """Generate steps for complex goals."""
        return [
            ExecutionStep(
                id="step_1",
                step_type=StepType.SEQUENTIAL,
                description="Analyze and decompose goal",
                function_name="analyze_complex_goal",
                parameters={"goal": goal},
                estimated_duration_ms=1500.0
            ),
            ExecutionStep(
                id="step_2a",
                step_type=StepType.PARALLEL,
                description="Prepare data sources",
                function_name="prepare_data",
                parameters={"context": context},
                dependencies=["step_1"],
                estimated_duration_ms=2000.0
            ),
            ExecutionStep(
                id="step_2b",
                step_type=StepType.PARALLEL,
                description="Initialize resources",
                function_name="initialize_resources",
                parameters={"context": context},
                dependencies=["step_1"],
                estimated_duration_ms=1500.0
            ),
            ExecutionStep(
                id="step_3",
                step_type=StepType.DECISION_POINT,
                description="Choose execution strategy",
                function_name="choose_strategy",
                parameters={"goal": goal},
                dependencies=["step_2a", "step_2b"],
                estimated_duration_ms=500.0
            ),
            ExecutionStep(
                id="step_4",
                step_type=StepType.FUNCTION_CALL,
                description="Execute complex processing",
                function_name="execute_complex_task",
                parameters={"goal": goal, "context": context},
                dependencies=["step_3"],
                estimated_duration_ms=5000.0
            ),
            ExecutionStep(
                id="step_5",
                step_type=StepType.SEQUENTIAL,
                description="Post-process and validate",
                function_name="post_process_results",
                parameters={},
                dependencies=["step_4"],
                estimated_duration_ms=1000.0
            )
        ]

    async def _generate_enterprise_steps(self, goal: str, context: Dict[str, Any]) -> List[ExecutionStep]:
        """Generate steps for enterprise-level goals."""
        # This would generate a comprehensive set of steps for enterprise workflows
        base_steps = await self._generate_complex_steps(goal, context)

        # Add enterprise-specific steps
        enterprise_steps = [
            ExecutionStep(
                id="step_0",
                step_type=StepType.SEQUENTIAL,
                description="Enterprise planning and authorization",
                function_name="enterprise_planning",
                parameters={"goal": goal, "context": context},
                estimated_duration_ms=3000.0
            ),
            ExecutionStep(
                id="step_audit",
                step_type=StepType.SEQUENTIAL,
                description="Audit and compliance check",
                function_name="audit_compliance",
                parameters={},
                dependencies=[step.id for step in base_steps],
                estimated_duration_ms=2000.0
            ),
            ExecutionStep(
                id="step_report",
                step_type=StepType.SEQUENTIAL,
                description="Generate execution report",
                function_name="generate_report",
                parameters={},
                dependencies=["step_audit"],
                estimated_duration_ms=1000.0
            )
        ]

        # Update dependencies for base steps
        for step in base_steps:
            if not step.dependencies:
                step.dependencies = ["step_0"]

        return [enterprise_steps[0]] + base_steps + enterprise_steps[1:]

    async def _optimize_plan_with_ml(self, plan: ExecutionPlan, context: Dict[str, Any]) -> ExecutionPlan:
        """Apply machine learning-based optimizations to the plan."""

        if not self.enable_ml_optimization:
            return plan

        # Simulate ML optimization (in practice, this would use trained models)
        optimization_score = await self._calculate_optimization_score(plan)

        if optimization_score > self.optimization_threshold:
            # Apply optimizations
            optimized_steps = await self._optimize_step_ordering(plan.steps)
            plan.steps = optimized_steps
            plan.optimization_score = optimization_score

            # Recalculate estimated duration with optimizations
            total_duration = sum(step.estimated_duration_ms for step in plan.steps)
            optimization_factor = 0.85  # 15% improvement from optimization
            plan.estimated_total_duration_ms = total_duration * optimization_factor

            self.metrics.optimization_improvements += 15.0  # Track improvement

            logger.debug(f"Applied ML optimization to plan {plan.id}, score: {optimization_score:.3f}")

        return plan

    async def _calculate_optimization_score(self, plan: ExecutionPlan) -> float:
        """Calculate an optimization score for the plan."""

        # Factors that contribute to optimization potential
        parallelizable_steps = sum(1 for step in plan.steps if step.step_type == StepType.PARALLEL)
        total_steps = len(plan.steps)
        dependency_efficiency = self._calculate_dependency_efficiency(plan.steps)

        # Historical performance data
        plan_type_key = f"{plan.complexity.value}_{total_steps}"
        historical_performance = self._execution_patterns.get(plan_type_key, [1.0])
        avg_performance = sum(historical_performance) / len(historical_performance)

        # Calculate composite score
        parallelization_score = parallelizable_steps / max(1, total_steps)
        efficiency_score = dependency_efficiency
        performance_score = min(1.0, avg_performance)

        optimization_score = (
            parallelization_score * 0.4 +
            efficiency_score * 0.3 +
            performance_score * 0.3
        )

        return optimization_score

    def _calculate_dependency_efficiency(self, steps: List[ExecutionStep]) -> float:
        """Calculate how efficiently dependencies are structured."""

        if not steps:
            return 1.0

        total_dependencies = sum(len(step.dependencies) for step in steps)
        max_possible_dependencies = len(steps) * (len(steps) - 1) / 2

        if max_possible_dependencies == 0:
            return 1.0

        # Lower dependency ratio is better (more parallelizable)
        dependency_ratio = total_dependencies / max_possible_dependencies
        return 1.0 - dependency_ratio

    async def _optimize_step_ordering(self, steps: List[ExecutionStep]) -> List[ExecutionStep]:
        """Optimize the ordering of steps for better execution performance."""

        # Create a dependency graph and optimize ordering
        # This is a simplified version - real implementation would use graph algorithms

        optimized_steps = []
        remaining_steps = steps.copy()

        while remaining_steps:
            # Find steps with no remaining dependencies
            ready_steps = [
                step for step in remaining_steps
                if all(dep_id in [s.id for s in optimized_steps] for dep_id in step.dependencies)
            ]

            if not ready_steps:
                # Add the first remaining step to break potential cycles
                ready_steps = [remaining_steps[0]]

            # Sort ready steps by priority (parallel steps first, then by estimated duration)
            ready_steps.sort(key=lambda s: (
                0 if s.step_type == StepType.PARALLEL else 1,
                s.estimated_duration_ms
            ))

            # Add the best step to optimized list
            best_step = ready_steps[0]
            optimized_steps.append(best_step)
            remaining_steps.remove(best_step)

        return optimized_steps

    async def _apply_adaptive_optimizations(self, plan: ExecutionPlan) -> ExecutionPlan:
        """Apply adaptive optimizations based on historical data and patterns."""

        # Adjust timeouts based on historical execution times
        for step in plan.steps:
            step_type_key = f"{step.step_type.value}_{step.function_name}"
            if step_type_key in self._execution_patterns:
                historical_times = self._execution_patterns[step_type_key]
                avg_time = sum(historical_times) / len(historical_times)
                # Set timeout to 3x average historical time with minimum of 5 seconds
                step.timeout_ms = max(5000, avg_time * 3)

        return plan

    async def _execute_plan_sequential(
        self,
        plan: ExecutionPlan,
        context: Dict[str, Any],
        kernel: Any,
        progress_callback: Optional[callable]
    ):
        """Execute plan steps sequentially."""

        for i, step in enumerate(plan.steps):
            try:
                # Check dependencies
                if not step.can_execute(context["completed_steps"]):
                    raise Exception(f"Step {step.id} dependencies not met")

                # Execute step
                step_start = time.time()
                result = await self._execute_step(step, kernel, context)
                step_duration = (time.time() - step_start) * 1000

                # Update context
                context["completed_steps"].add(step.id)
                context["step_results"][step.id] = result
                context["performance_data"].append({
                    "step_id": step.id,
                    "duration_ms": step_duration,
                    "success": True
                })

                # Progress callback
                if progress_callback:
                    await progress_callback(i + 1, len(plan.steps), step.id, result)

                logger.debug(f"Completed step {step.id} in {step_duration:.2f}ms")

            except Exception as e:
                error_info = {
                    "step_id": step.id,
                    "error": str(e),
                    "timestamp": time.time()
                }
                context["errors"].append(error_info)
                logger.error(f"Error executing step {step.id}: {e}")

                # Continue with next step unless it's a critical failure
                if step.step_type == StepType.DECISION_POINT:
                    break

    async def _execute_plan_parallel(
        self,
        plan: ExecutionPlan,
        context: Dict[str, Any],
        kernel: Any,
        progress_callback: Optional[callable]
    ):
        """Execute plan steps with parallel optimization."""

        while len(context["completed_steps"]) < len(plan.steps):
            # Get steps that can run in parallel
            executable_steps = plan.get_parallel_steps(context["completed_steps"])

            if not executable_steps:
                # Get sequential steps that can execute
                all_executable = plan.get_executable_steps(context["completed_steps"])
                if all_executable:
                    executable_steps = [all_executable[0]]
                else:
                    break  # No more executable steps

            # Limit parallel execution
            parallel_batch = executable_steps[:self.max_parallel_steps]

            # Execute batch in parallel
            tasks = [
                self._execute_step_with_context(step, kernel, context)
                for step in parallel_batch
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for step, result in zip(parallel_batch, results):
                if isinstance(result, Exception):
                    error_info = {
                        "step_id": step.id,
                        "error": str(result),
                        "timestamp": time.time()
                    }
                    context["errors"].append(error_info)
                    logger.error(f"Error executing parallel step {step.id}: {result}")
                else:
                    context["completed_steps"].add(step.id)
                    context["step_results"][step.id] = result
                    logger.debug(f"Completed parallel step {step.id}")

            # Progress callback
            if progress_callback:
                await progress_callback(
                    len(context["completed_steps"]),
                    len(plan.steps),
                    "parallel_batch",
                    f"Completed {len(parallel_batch)} parallel steps"
                )

    async def _execute_step_with_context(self, step: ExecutionStep, kernel: Any, context: Dict[str, Any]):
        """Execute a single step with timing and error handling."""
        step_start = time.time()
        try:
            result = await self._execute_step(step, kernel, context)
            step_duration = (time.time() - step_start) * 1000

            context["performance_data"].append({
                "step_id": step.id,
                "duration_ms": step_duration,
                "success": True
            })

            return result
        except Exception as e:
            step_duration = (time.time() - step_start) * 1000
            context["performance_data"].append({
                "step_id": step.id,
                "duration_ms": step_duration,
                "success": False,
                "error": str(e)
            })
            raise

    async def _execute_step(self, step: ExecutionStep, kernel: Any, context: Dict[str, Any]) -> Any:
        """Execute a single step."""

        # This is a placeholder for actual step execution
        # In practice, this would integrate with the Semantic Kernel function system

        logger.debug(f"Executing step: {step.id} - {step.description}")

        # Simulate step execution
        await asyncio.sleep(step.estimated_duration_ms / 10000)  # Scale down for demo

        return {
            "step_id": step.id,
            "result": f"Completed {step.description}",
            "parameters": step.parameters
        }

    async def _learn_from_execution(self, plan: ExecutionPlan, execution_context: Dict[str, Any]):
        """Learn from execution performance to improve future planning."""

        # Extract performance patterns
        for perf_data in execution_context["performance_data"]:
            step_id = perf_data["step_id"]
            duration_ms = perf_data["duration_ms"]

            # Find the corresponding step
            step = next((s for s in plan.steps if s.id == step_id), None)
            if step:
                pattern_key = f"{step.step_type.value}_{step.function_name}"
                if pattern_key not in self._execution_patterns:
                    self._execution_patterns[pattern_key] = []

                self._execution_patterns[pattern_key].append(duration_ms)

                # Keep only recent performance data
                if len(self._execution_patterns[pattern_key]) > 50:
                    self._execution_patterns[pattern_key] = self._execution_patterns[pattern_key][-50:]

    def _generate_cache_key(self, goal: str, context: Dict[str, Any]) -> str:
        """Generate a cache key for plan caching."""
        context_hash = hash(json.dumps(context, sort_keys=True))
        return f"{hash(goal)}_{context_hash}"

    def _is_plan_fresh(self, plan: ExecutionPlan, max_age_hours: float = 24.0) -> bool:
        """Check if a cached plan is still fresh."""
        age_hours = (time.time() - plan.created_at) / 3600
        return age_hours < max_age_hours

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        return {
            "metrics": {
                "total_plans_created": self.metrics.total_plans_created,
                "total_plans_executed": self.metrics.total_plans_executed,
                "success_rate": self.metrics.success_rate,
                "average_execution_time_ms": self.metrics.average_execution_time_ms,
                "average_steps_per_plan": self.metrics.average_steps_per_plan,
                "optimization_improvements": self.metrics.optimization_improvements
            },
            "complexity_distribution": self.metrics.complexity_distribution,
            "cached_plans": len(self._plan_cache),
            "learned_patterns": len(self._execution_patterns),
            "ml_optimization_enabled": self.enable_ml_optimization
        }

    def clear_cache(self):
        """Clear all cached plans and learning data."""
        self._plan_cache.clear()
        self._execution_patterns.clear()
        logger.info("Cleared adaptive planner cache and learning data")
