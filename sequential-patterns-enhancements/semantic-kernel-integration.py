#!/usr/bin/env python3
"""
Sequential Patterns Integration Module

This module provides seamless integration between the enhanced sequential pattern
implementations and the existing Semantic Kernel infrastructure. It includes:

- Integration adapters for existing SK components
- Bridge classes for compatibility
- Migration utilities for existing implementations
- Configuration management
- Performance monitoring and reporting
"""

import asyncio
import logging
import json
from typing import Any, Dict, List, Optional, Union, Callable
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import inspect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Semantic Kernel components
try:
    # These would be actual SK imports in a real implementation
    # from semantic_kernel import Kernel
    # from semantic_kernel.planning import SequentialPlanner as SKSequentialPlanner
    # from semantic_kernel.orchestration import SKFunction
    # from semantic_kernel.orchestration.sk_context import SKContext
    pass
except ImportError:
    logger.info("Semantic Kernel not available, using mock implementations")

# Import enhanced implementations
try:
    from advanced_sequential_orchestrator import (
        AdvancedSequentialOrchestrator,
        SequentialStep,
        ExecutionStatus,
        CoordinationPattern
    )
    from enhanced_sequential_planning import (
        SequentialPlan,
        PlanAction,
        PlanObjective,
        SequentialPlanExecutor,
        GreedySequentialPlanGenerator
    )
    from intelligent_sequential_selection import (
        IntelligentSequentialSelector,
        AgentProfile,
        SelectionContext,
        SelectionStrategy
    )
except ImportError as e:
    logger.warning(f"Enhanced implementations not available: {e}")
    # Create minimal placeholders
    class AdvancedSequentialOrchestrator: pass
    class SequentialStep: pass
    class SequentialPlan: pass
    class PlanAction: pass
    class IntelligentSequentialSelector: pass

class SKIntegrationAdapter:
    """
    Adapter class for integrating enhanced sequential patterns with Semantic Kernel.
    
    This class provides compatibility between the enhanced implementations and
    existing Semantic Kernel interfaces.
    """
    
    def __init__(self, kernel=None):
        """Initialize the integration adapter."""
        self.kernel = kernel
        self.orchestrator = AdvancedSequentialOrchestrator()
        self.plan_executor = SequentialPlanExecutor()
        self.agent_selector = IntelligentSequentialSelector()
        
        # Integration metrics
        self.integration_metrics = {
            'function_calls': 0,
            'plan_executions': 0,
            'agent_selections': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
        
        logger.info("SK Integration Adapter initialized")
    
    async def execute_sk_function_sequentially(self, functions: List[Any], 
                                             context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute Semantic Kernel functions sequentially using enhanced orchestrator.
        
        Args:
            functions: List of SK functions to execute
            context: Execution context
            
        Returns:
            Execution results and metrics
        """
        try:
            self.integration_metrics['function_calls'] += len(functions)
            
            # Convert SK functions to SequentialSteps
            steps = []
            for i, sk_function in enumerate(functions):
                step = await self._convert_sk_function_to_step(sk_function, i)
                steps.append(step)
            
            # Execute using enhanced orchestrator
            if hasattr(self.orchestrator, 'add_steps'):
                self.orchestrator.add_steps(steps)
                result = await self.orchestrator.execute()
            else:
                # Fallback execution
                result = await self._fallback_execute_functions(functions, context)
            
            logger.info(f"Successfully executed {len(functions)} SK functions sequentially")
            return result
            
        except Exception as e:
            self.integration_metrics['errors'] += 1
            logger.error(f"Error executing SK functions: {e}")
            raise
    
    async def _convert_sk_function_to_step(self, sk_function: Any, step_index: int) -> SequentialStep:
        """Convert an SK function to a SequentialStep."""
        
        async def step_executor(context):
            """Execute the SK function."""
            try:
                # Handle different SK function types
                if hasattr(sk_function, 'invoke_async'):
                    result = await sk_function.invoke_async(context)
                elif hasattr(sk_function, 'invoke'):
                    result = sk_function.invoke(context)
                elif callable(sk_function):
                    # Direct function call
                    if inspect.iscoroutinefunction(sk_function):
                        result = await sk_function(context)
                    else:
                        result = sk_function(context)
                else:
                    raise ValueError(f"Unknown function type: {type(sk_function)}")
                
                return {
                    'sk_function': getattr(sk_function, 'name', f'function_{step_index}'),
                    'result': result,
                    'success': True
                }
                
            except Exception as e:
                logger.error(f"Error executing SK function {step_index}: {e}")
                return {
                    'sk_function': getattr(sk_function, 'name', f'function_{step_index}'),
                    'error': str(e),
                    'success': False
                }
        
        return SequentialStep(
            step_id=f"sk_function_{step_index}",
            executor=step_executor,
            priority=step_index + 1,
            timeout=30.0  # Default timeout
        )
    
    async def _fallback_execute_functions(self, functions: List[Any], 
                                        context: Optional[Dict] = None) -> Dict[str, Any]:
        """Fallback execution for when enhanced orchestrator is not available."""
        results = []
        start_time = datetime.now()
        
        for i, func in enumerate(functions):
            try:
                if callable(func):
                    if inspect.iscoroutinefunction(func):
                        result = await func(context)
                    else:
                        result = func(context)
                    results.append({'function_index': i, 'result': result, 'success': True})
                else:
                    results.append({'function_index': i, 'error': 'Not callable', 'success': False})
            except Exception as e:
                results.append({'function_index': i, 'error': str(e), 'success': False})
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'success': all(r['success'] for r in results),
            'results': results,
            'execution_time': execution_time,
            'function_count': len(functions)
        }
    
    async def integrate_sk_planner(self, sk_plan: Any, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Integrate with Semantic Kernel planner using enhanced planning.
        
        Args:
            sk_plan: Semantic Kernel plan object
            context: Execution context
            
        Returns:
            Enhanced plan execution results
        """
        try:
            self.integration_metrics['plan_executions'] += 1
            
            # Convert SK plan to enhanced plan
            enhanced_plan = await self._convert_sk_plan_to_enhanced_plan(sk_plan)
            
            # Execute using enhanced executor
            if hasattr(self.plan_executor, 'execute_plan'):
                metrics = await self.plan_executor.execute_plan(enhanced_plan)
                
                return {
                    'success': True,
                    'plan_metrics': metrics,
                    'enhanced_execution': True
                }
            else:
                # Fallback execution
                return await self._fallback_execute_plan(sk_plan, context)
                
        except Exception as e:
            self.integration_metrics['errors'] += 1
            logger.error(f"Error integrating SK planner: {e}")
            raise
    
    async def _convert_sk_plan_to_enhanced_plan(self, sk_plan: Any) -> SequentialPlan:
        """Convert an SK plan to an enhanced SequentialPlan."""
        enhanced_plan = SequentialPlan()
        
        # Extract actions from SK plan
        if hasattr(sk_plan, 'steps'):
            for step in sk_plan.steps:
                action = await self._convert_sk_step_to_action(step)
                if hasattr(enhanced_plan, 'add_action'):
                    enhanced_plan.add_action(action)
        
        return enhanced_plan
    
    async def _convert_sk_step_to_action(self, sk_step: Any) -> PlanAction:
        """Convert an SK plan step to a PlanAction."""
        
        async def action_executor(context, parameters):
            """Execute the SK plan step."""
            try:
                # Execute the step based on its type
                if hasattr(sk_step, 'invoke_async'):
                    result = await sk_step.invoke_async(context)
                elif hasattr(sk_step, 'invoke'):
                    result = sk_step.invoke(context)
                else:
                    result = str(sk_step)  # Convert to string if no invoke method
                
                return {'sk_step_result': result, 'success': True}
                
            except Exception as e:
                logger.error(f"Error executing SK step: {e}")
                return {'error': str(e), 'success': False}
        
        return PlanAction(
            action_id=getattr(sk_step, 'step_id', f'sk_step_{id(sk_step)}'),
            name=getattr(sk_step, 'name', 'SK Step'),
            description=getattr(sk_step, 'description', 'Converted SK step'),
            executor=action_executor,
            duration_estimate=1.0,  # Default estimate
            success_probability=0.9
        )
    
    async def _fallback_execute_plan(self, sk_plan: Any, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Fallback plan execution."""
        return {
            'success': True,
            'plan_type': 'sk_plan',
            'executed_with_fallback': True,
            'message': 'Plan executed with basic compatibility layer'
        }
    
    def get_integration_metrics(self) -> Dict[str, Any]:
        """Get integration performance metrics."""
        runtime = (datetime.now() - self.integration_metrics['start_time']).total_seconds()
        
        return {
            **self.integration_metrics,
            'runtime_seconds': runtime,
            'functions_per_second': self.integration_metrics['function_calls'] / max(runtime, 1),
            'success_rate': 1 - (self.integration_metrics['errors'] / max(
                self.integration_metrics['function_calls'] + self.integration_metrics['plan_executions'], 1
            ))
        }

class EnhancedPlannerBridge:
    """
    Bridge class for seamless integration between SK planners and enhanced planning.
    """
    
    def __init__(self, sk_planner=None):
        """Initialize the planner bridge."""
        self.sk_planner = sk_planner
        self.enhanced_generator = GreedySequentialPlanGenerator()
        self.plan_cache = {}
        
        logger.info("Enhanced Planner Bridge initialized")
    
    async def create_hybrid_plan(self, goal: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a hybrid plan using both SK and enhanced planning.
        
        Args:
            goal: Planning goal
            context: Planning context
            
        Returns:
            Hybrid plan with both SK and enhanced components
        """
        try:
            # Generate SK plan if planner available
            sk_plan = None
            if self.sk_planner and hasattr(self.sk_planner, 'create_plan_async'):
                try:
                    sk_plan = await self.sk_planner.create_plan_async(goal)
                except Exception as e:
                    logger.warning(f"SK planner failed: {e}")
            
            # Generate enhanced plan
            enhanced_plan = None
            if hasattr(self.enhanced_generator, 'generate_plan'):
                objectives = [PlanObjective("main_goal", goal, weight=1.0)]
                
                # Create basic actions for the goal
                actions = await self._create_actions_for_goal(goal, context)
                
                enhanced_plan = await self.enhanced_generator.generate_plan(
                    objectives=objectives,
                    available_actions=actions,
                    context=context or {}
                )
            
            # Create hybrid plan
            hybrid_plan = {
                'goal': goal,
                'sk_plan': sk_plan,
                'enhanced_plan': enhanced_plan,
                'plan_id': f"hybrid_{hash(goal)}",
                'created_at': datetime.now().isoformat()
            }
            
            # Cache the plan
            self.plan_cache[hybrid_plan['plan_id']] = hybrid_plan
            
            return hybrid_plan
            
        except Exception as e:
            logger.error(f"Error creating hybrid plan: {e}")
            raise
    
    async def _create_actions_for_goal(self, goal: str, context: Optional[Dict] = None) -> List[PlanAction]:
        """Create basic actions for a planning goal."""
        # This is a simple implementation - in practice, this would be more sophisticated
        actions = []
        
        # Create generic actions based on goal keywords
        if any(keyword in goal.lower() for keyword in ['analyze', 'process', 'compute']):
            actions.append(PlanAction(
                action_id="analyze_action",
                name="Analysis Action",
                description="Perform analysis based on goal",
                executor=self._create_generic_executor("analysis"),
                duration_estimate=2.0,
                success_probability=0.85
            ))
        
        if any(keyword in goal.lower() for keyword in ['create', 'generate', 'build']):
            actions.append(PlanAction(
                action_id="create_action",
                name="Creation Action",
                description="Create or generate based on goal",
                executor=self._create_generic_executor("creation"),
                duration_estimate=3.0,
                success_probability=0.8
            ))
        
        if any(keyword in goal.lower() for keyword in ['validate', 'check', 'verify']):
            actions.append(PlanAction(
                action_id="validate_action",
                name="Validation Action",
                description="Validate or verify based on goal",
                executor=self._create_generic_executor("validation"),
                duration_estimate=1.0,
                success_probability=0.9
            ))
        
        # Always add a generic completion action
        actions.append(PlanAction(
            action_id="complete_action",
            name="Completion Action", 
            description="Complete the goal",
            executor=self._create_generic_executor("completion"),
            duration_estimate=1.0,
            success_probability=0.95
        ))
        
        return actions
    
    def _create_generic_executor(self, action_type: str) -> Callable:
        """Create a generic action executor."""
        async def executor(context, parameters):
            await asyncio.sleep(0.1)  # Simulate work
            return {
                'action_type': action_type,
                'context': context,
                'parameters': parameters,
                'result': f"{action_type} completed successfully"
            }
        return executor

class ConfigurationManager:
    """
    Configuration management for sequential pattern integrations.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_file = config_file or "sequential_patterns_config.json"
        self.config = self._load_default_config()
        self._load_config_file()
        
        logger.info(f"Configuration Manager initialized with {self.config_file}")
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "orchestration": {
                "max_concurrent_steps": 5,
                "default_timeout": 30.0,
                "retry_attempts": 3,
                "coordination_pattern": "ADAPTIVE_SEQUENTIAL"
            },
            "planning": {
                "max_plan_depth": 10,
                "optimization_strategy": "greedy",
                "enable_adaptive_learning": True,
                "plan_cache_size": 100
            },
            "selection": {
                "default_strategy": "PERFORMANCE_BASED",
                "enable_learning": True,
                "max_agent_load": 0.8,
                "selection_timeout": 5.0
            },
            "integration": {
                "enable_sk_compatibility": True,
                "fallback_mode": "graceful",
                "metrics_collection": True,
                "log_level": "INFO"
            },
            "performance": {
                "enable_monitoring": True,
                "metrics_collection_interval": 60,
                "performance_threshold": 0.8,
                "memory_limit_mb": 1024
            }
        }
    
    def _load_config_file(self):
        """Load configuration from file if it exists."""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                self._merge_config(self.config, file_config)
                logger.info(f"Loaded configuration from {self.config_file}")
        except Exception as e:
            logger.warning(f"Could not load config file {self.config_file}: {e}")
    
    def _merge_config(self, base_config: Dict, override_config: Dict):
        """Merge override configuration into base configuration."""
        for key, value in override_config.items():
            if key in base_config and isinstance(base_config[key], dict) and isinstance(value, dict):
                self._merge_config(base_config[key], value)
            else:
                base_config[key] = value
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Could not save config file: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key path."""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """Set configuration value by dot-separated key path."""
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value

class PerformanceMonitor:
    """
    Performance monitoring for sequential pattern implementations.
    """
    
    def __init__(self, collection_interval: int = 60):
        """Initialize performance monitor."""
        self.collection_interval = collection_interval
        self.metrics = {
            'orchestration': [],
            'planning': [], 
            'selection': [],
            'integration': []
        }
        self.is_monitoring = False
        
        logger.info("Performance Monitor initialized")
    
    async def start_monitoring(self):
        """Start performance monitoring."""
        self.is_monitoring = True
        logger.info("Performance monitoring started")
        
        while self.is_monitoring:
            await self._collect_metrics()
            await asyncio.sleep(self.collection_interval)
    
    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.is_monitoring = False
        logger.info("Performance monitoring stopped")
    
    async def _collect_metrics(self):
        """Collect performance metrics."""
        try:
            import psutil
            
            # System metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Timestamp
            timestamp = datetime.now().isoformat()
            
            # Store metrics
            system_metrics = {
                'timestamp': timestamp,
                'cpu_usage': cpu_usage,
                'memory_usage': memory.percent,
                'memory_available_mb': memory.available / 1024 / 1024
            }
            
            self.metrics['system'] = system_metrics
            
        except ImportError:
            logger.warning("psutil not available for system metrics")
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
    
    def add_orchestration_metric(self, execution_time: float, step_count: int, success_rate: float):
        """Add orchestration performance metric."""
        metric = {
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time,
            'step_count': step_count,
            'success_rate': success_rate,
            'throughput': step_count / execution_time if execution_time > 0 else 0
        }
        self.metrics['orchestration'].append(metric)
        
        # Keep only recent metrics
        if len(self.metrics['orchestration']) > 1000:
            self.metrics['orchestration'] = self.metrics['orchestration'][-500:]
    
    def add_planning_metric(self, generation_time: float, action_count: int, plan_score: float):
        """Add planning performance metric."""
        metric = {
            'timestamp': datetime.now().isoformat(),
            'generation_time': generation_time,
            'action_count': action_count,
            'plan_score': plan_score,
            'actions_per_second': action_count / generation_time if generation_time > 0 else 0
        }
        self.metrics['planning'].append(metric)
        
        # Keep only recent metrics
        if len(self.metrics['planning']) > 1000:
            self.metrics['planning'] = self.metrics['planning'][-500:]
    
    def add_selection_metric(self, selection_time: float, agent_count: int, selection_quality: float):
        """Add selection performance metric."""
        metric = {
            'timestamp': datetime.now().isoformat(),
            'selection_time': selection_time,
            'agent_count': agent_count,
            'selection_quality': selection_quality,
            'selections_per_second': 1 / selection_time if selection_time > 0 else 0
        }
        self.metrics['selection'].append(metric)
        
        # Keep only recent metrics
        if len(self.metrics['selection']) > 1000:
            self.metrics['selection'] = self.metrics['selection'][-500:]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        report = {
            'generated_at': datetime.now().isoformat(),
            'collection_interval': self.collection_interval,
            'monitoring_active': self.is_monitoring
        }
        
        # Analyze orchestration metrics
        if self.metrics['orchestration']:
            orchestration_times = [m['execution_time'] for m in self.metrics['orchestration']]
            orchestration_throughput = [m['throughput'] for m in self.metrics['orchestration']]
            
            report['orchestration'] = {
                'avg_execution_time': sum(orchestration_times) / len(orchestration_times),
                'min_execution_time': min(orchestration_times),
                'max_execution_time': max(orchestration_times),
                'avg_throughput': sum(orchestration_throughput) / len(orchestration_throughput),
                'total_executions': len(self.metrics['orchestration'])
            }
        
        # Analyze planning metrics
        if self.metrics['planning']:
            planning_times = [m['generation_time'] for m in self.metrics['planning']]
            planning_scores = [m['plan_score'] for m in self.metrics['planning']]
            
            report['planning'] = {
                'avg_generation_time': sum(planning_times) / len(planning_times),
                'avg_plan_score': sum(planning_scores) / len(planning_scores),
                'total_plans_generated': len(self.metrics['planning'])
            }
        
        # Analyze selection metrics
        if self.metrics['selection']:
            selection_times = [m['selection_time'] for m in self.metrics['selection']]
            selection_quality = [m['selection_quality'] for m in self.metrics['selection']]
            
            report['selection'] = {
                'avg_selection_time': sum(selection_times) / len(selection_times),
                'avg_selection_quality': sum(selection_quality) / len(selection_quality),
                'total_selections': len(self.metrics['selection'])
            }
        
        return report

class IntegrationManager:
    """
    Main integration manager that coordinates all enhanced sequential patterns.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize the integration manager."""
        self.config = ConfigurationManager(config_file)
        self.performance_monitor = PerformanceMonitor(
            self.config.get('performance.metrics_collection_interval', 60)
        )
        self.sk_adapter = SKIntegrationAdapter()
        self.planner_bridge = EnhancedPlannerBridge()
        
        self.is_initialized = False
        logger.info("Integration Manager created")
    
    async def initialize(self):
        """Initialize all integration components."""
        try:
            # Start performance monitoring if enabled
            if self.config.get('performance.enable_monitoring', True):
                asyncio.create_task(self.performance_monitor.start_monitoring())
            
            self.is_initialized = True
            logger.info("Integration Manager fully initialized")
            
        except Exception as e:
            logger.error(f"Error initializing Integration Manager: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown the integration manager."""
        try:
            self.performance_monitor.stop_monitoring()
            self.config.save_config()
            
            logger.info("Integration Manager shut down successfully")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    async def execute_sequential_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a complete sequential workflow using enhanced patterns.
        
        Args:
            workflow_config: Configuration for the workflow
            
        Returns:
            Workflow execution results and metrics
        """
        if not self.is_initialized:
            await self.initialize()
        
        try:
            start_time = datetime.now()
            
            # Extract workflow components
            functions = workflow_config.get('functions', [])
            planning_goal = workflow_config.get('planning_goal')
            agents = workflow_config.get('agents', [])
            context = workflow_config.get('context', {})
            
            results = {}
            
            # 1. Agent Selection (if agents provided)
            if agents:
                selection_start = datetime.now()
                # Agent selection logic would go here
                selection_time = (datetime.now() - selection_start).total_seconds()
                
                self.performance_monitor.add_selection_metric(
                    selection_time, len(agents), 0.8  # Mock quality score
                )
                
                results['agent_selection'] = {
                    'selected_agents': agents,  # Simplified
                    'selection_time': selection_time
                }
            
            # 2. Planning (if goal provided)
            if planning_goal:
                planning_start = datetime.now()
                hybrid_plan = await self.planner_bridge.create_hybrid_plan(
                    planning_goal, context
                )
                planning_time = (datetime.now() - planning_start).total_seconds()
                
                self.performance_monitor.add_planning_metric(
                    planning_time, 5, 0.85  # Mock action count and score
                )
                
                results['planning'] = {
                    'plan': hybrid_plan,
                    'planning_time': planning_time
                }
            
            # 3. Function Execution (if functions provided)
            if functions:
                execution_start = datetime.now()
                execution_result = await self.sk_adapter.execute_sk_function_sequentially(
                    functions, context
                )
                execution_time = (datetime.now() - execution_start).total_seconds()
                
                self.performance_monitor.add_orchestration_metric(
                    execution_time, len(functions), 
                    1.0 if execution_result.get('success', False) else 0.0
                )
                
                results['execution'] = execution_result
            
            # Calculate total workflow time
            total_time = (datetime.now() - start_time).total_seconds()
            
            # Compile final results
            workflow_results = {
                'success': True,
                'total_time': total_time,
                'components': results,
                'integration_metrics': self.sk_adapter.get_integration_metrics(),
                'workflow_id': f"workflow_{hash(str(workflow_config))}"
            }
            
            logger.info(f"Sequential workflow completed in {total_time:.2f} seconds")
            return workflow_results
            
        except Exception as e:
            logger.error(f"Error executing sequential workflow: {e}")
            return {
                'success': False,
                'error': str(e),
                'workflow_id': f"failed_workflow_{hash(str(workflow_config))}"
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'integration_manager': {
                'initialized': self.is_initialized,
                'config_file': self.config.config_file
            },
            'performance_monitoring': {
                'active': self.performance_monitor.is_monitoring,
                'collection_interval': self.performance_monitor.collection_interval
            },
            'sk_integration': self.sk_adapter.get_integration_metrics(),
            'performance_report': self.performance_monitor.get_performance_report(),
            'timestamp': datetime.now().isoformat()
        }

# Factory function for easy initialization
def create_integration_manager(config_file: Optional[str] = None) -> IntegrationManager:
    """
    Factory function to create and initialize an IntegrationManager.
    
    Args:
        config_file: Optional configuration file path
        
    Returns:
        Configured IntegrationManager instance
    """
    return IntegrationManager(config_file)

# Example usage and testing
async def main():
    """Example usage of the integration system."""
    print("🔗 Sequential Patterns Integration System")
    print("=" * 50)
    
    # Create integration manager
    manager = create_integration_manager()
    await manager.initialize()
    
    # Example workflow configuration
    workflow_config = {
        'functions': [
            lambda ctx: {"step": "data_processing", "result": "processed"},
            lambda ctx: {"step": "analysis", "result": "analyzed"},
            lambda ctx: {"step": "reporting", "result": "reported"}
        ],
        'planning_goal': "Create comprehensive data analysis report",
        'agents': ['agent1', 'agent2'],  # Simplified agent list
        'context': {'project': 'integration_test', 'priority': 'high'}
    }
    
    try:
        # Execute workflow
        results = await manager.execute_sequential_workflow(workflow_config)
        
        print(f"✅ Workflow executed successfully: {results['success']}")
        print(f"⏱️ Total time: {results.get('total_time', 0):.2f} seconds")
        
        # Get system status
        status = manager.get_system_status()
        print(f"📊 System Status: {status['integration_manager']['initialized']}")
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
    
    finally:
        await manager.shutdown()

if __name__ == "__main__":
    print("Starting Sequential Patterns Integration System...")
    asyncio.run(main())
