#!/usr/bin/env python3
"""
AI module for ai monitoring integration

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import sys
import inspect
import functools
import asyncio
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
import logging

# Add the scripts directory to Python path
sys.path.append(str(Path(__file__).parent))

from ai_activity_monitor import get_monitor, log_ai_activity, log_ai_thought, log_ai_decision, log_ai_analysis, track_ai_action

logger = logging.getLogger(__name__)

class MonitoredAgent:
    """Wrapper class that adds monitoring to any AI agent"""

    def __init__(self, original_agent, agent_name: str = None):
        self.original_agent = original_agent
        self.agent_name = agent_name or original_agent.__class__.__name__
        self.monitor = get_monitor()

        # Wrap all methods
        self._wrap_methods()

    def _wrap_methods(self):
        """Wrap all methods of the original agent with monitoring"""
        for name, method in inspect.getmembers(self.original_agent, predicate=inspect.ismethod):
            if not name.startswith('_'):  # Don't wrap private methods
                wrapped_method = self._create_wrapped_method(name, method)
                setattr(self, name, wrapped_method)

    def _create_wrapped_method(self, method_name: str, original_method):
        """Create a monitored version of a method"""
        if asyncio.iscoroutinefunction(original_method):
            @functools.wraps(original_method)
            async def async_wrapped(*args, **kwargs):
                async with track_ai_action(self.agent_name, method_name, method_args=args, method_kwargs=kwargs):
                    try:
                        result = await original_method(*args, **kwargs)

                        # Log the result
                        if hasattr(result, '__dict__') or isinstance(result, (list, dict)):
                            log_ai_activity(
                                self.agent_name,
                                "result",
                                f"{method_name} completed successfully",
                                result_type=type(result).__name__,
                                result_size=len(result) if hasattr(result, '__len__') else None
                            )

                        return result
                    except Exception as e:
                        log_ai_activity(
                            self.agent_name,
                            "error",
                            f"{method_name} failed: {str(e)}",
                            error_type=type(e).__name__,
                            error_message=str(e)
                        )
                        raise

            return async_wrapped
        else:
            @functools.wraps(original_method)
            def sync_wrapped(*args, **kwargs):
                log_ai_activity(
                    self.agent_name,
                    "action",
                    f"Executing {method_name}",
                    method_args=str(args)[:200],  # Truncate long args
                    method_kwargs=str(kwargs)[:200]
                )

                try:
                    result = original_method(*args, **kwargs)

                    # Log the result
                    if hasattr(result, '__dict__') or isinstance(result, (list, dict)):
                        log_ai_activity(
                            self.agent_name,
                            "result",
                            f"{method_name} completed successfully",
                            result_type=type(result).__name__,
                            result_size=len(result) if hasattr(result, '__len__') else None
                        )

                    return result
                except Exception as e:
                    log_ai_activity(
                        self.agent_name,
                        "error",
                        f"{method_name} failed: {str(e)}",
                        error_type=type(e).__name__,
                        error_message=str(e)
                    )
                    raise

            return sync_wrapped

    def __getattr__(self, name):
        """Delegate attribute access to original agent"""
        return getattr(self.original_agent, name)

def monitor_agent(agent_class_or_instance, agent_name: str = None):
    """Decorator/wrapper to add monitoring to an agent"""
    if inspect.isclass(agent_class_or_instance):
        # It's a class, create a wrapper class
        class MonitoredAgentClass(agent_class_or_instance):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._monitor = get_monitor()
                self._agent_name = agent_name or self.__class__.__name__
                self._wrap_agent_methods()

            def _wrap_agent_methods(self):
                """Wrap methods with monitoring"""
                for name in dir(self):
                    if not name.startswith('_') and callable(getattr(self, name)):
                        original_method = getattr(self, name)
                        wrapped_method = self._create_monitored_method(name, original_method)
                        setattr(self, name, wrapped_method)

            def _create_monitored_method(self, method_name: str, original_method):
                """Create monitored version of method"""
                @functools.wraps(original_method)
                def wrapped(*args, **kwargs):
                    log_ai_activity(
                        self._agent_name,
                        "action",
                        f"Executing {method_name}",
                        method=method_name
                    )
                    return original_method(*args, **kwargs)
                return wrapped

        return MonitoredAgentClass
    else:
        # It's an instance, wrap it
        return MonitoredAgent(agent_class_or_instance, agent_name)

def patch_existing_agents():
    """Monkey patch existing agents to add monitoring"""
    # This function can be called to patch existing agent modules

    # Try to import and patch common agent modules
    agent_modules = [
        'endless_improvement_loop',
        'cognitive_agent',
        'infrastructure_agent',
        'security_agent',
        'predictive_analytics_agent',
        'autonomous_optimization_agent'
    ]

    for module_name in agent_modules:
        try:
            module = __import__(module_name)
            _patch_module_classes(module, module_name)
            logger.info(f"✅ Patched {module_name} with monitoring")
        except ImportError:
            logger.debug(f"Module {module_name} not found, skipping")
        except Exception as e:
            logger.error(f"Error patching {module_name}: {e}")

def _patch_module_classes(module, module_name: str):
    """Patch all agent classes in a module"""
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if 'Agent' in name and hasattr(obj, 'analyze'):
            # This looks like an agent class
            _add_monitoring_to_class(obj, f"{module_name}.{name}")

def _add_monitoring_to_class(cls, class_name: str):
    """Add monitoring to a specific class"""
    original_init = cls.__init__

    def monitored_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self._monitor = get_monitor()
        self._agent_name = class_name

        # Log agent initialization
        log_ai_activity(
            self._agent_name,
            "initialization",
            f"Agent {class_name} initialized",
            init_args=str(args)[:100],
            init_kwargs=str(kwargs)[:100]
        )

    cls.__init__ = monitored_init

    # Wrap key methods
    for method_name in ['analyze', 'propose_actions', 'execute_action']:
        if hasattr(cls, method_name):
            original_method = getattr(cls, method_name)
            wrapped_method = _create_monitored_method(original_method, class_name, method_name)
            setattr(cls, method_name, wrapped_method)

def _create_monitored_method(original_method, agent_name: str, method_name: str):
    """Create a monitored version of a method"""
    if asyncio.iscoroutinefunction(original_method):
        @functools.wraps(original_method)
        async def async_wrapped(self, *args, **kwargs):
            async with track_ai_action(agent_name, method_name):
                return await original_method(self, *args, **kwargs)
        return async_wrapped
    else:
        @functools.wraps(original_method)
        def sync_wrapped(self, *args, **kwargs):
            log_ai_activity(agent_name, "action", f"Executing {method_name}")
            return original_method(self, *args, **kwargs)
        return sync_wrapped

# Convenience functions for manual logging
class AILogger:
    """Convenient interface for logging AI activities"""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.monitor = get_monitor()

    def thought(self, message: str, **context):
        """Log a thought"""
        log_ai_thought(self.agent_name, message, **context)

    def decision(self, decision: str, reasoning: str, options: List[str] = None):
        """Log a decision"""
        log_ai_decision(self.agent_name, decision, reasoning, options)

    def analysis(self, analysis_type: str, **results):
        """Log analysis results"""
        log_ai_analysis(self.agent_name, analysis_type, **results)

    def action(self, action_name: str, **details):
        """Log an action"""
        log_ai_activity(self.agent_name, "action", action_name, **details)

    def error(self, error_message: str, **details):
        """Log an error"""
        log_ai_activity(self.agent_name, "error", error_message, **details)

    def result(self, result_description: str, **details):
        """Log a result"""
        log_ai_activity(self.agent_name, "result", result_description, **details)

# Global loggers for easy access
_loggers = {}

def get_logger(agent_name: str) -> AILogger:
    """Get or create a logger for an agent"""
    if agent_name not in _loggers:
        _loggers[agent_name] = AILogger(agent_name)
    return _loggers[agent_name]

# Auto-patch on import (can be disabled by setting environment variable)
import os
if os.getenv('DISABLE_AI_MONITORING') != 'true':
    try:
        patch_existing_agents()
    except Exception as e:
        logger.error(f"Error during auto-patching: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Example of how to use the monitoring system

    # Create a logger for testing
    test_logger = get_logger("TestAgent")

    # Log some example activities
    test_logger.thought("Starting test sequence")
    test_logger.decision("Use strategy A", "Strategy A has better performance", ["Strategy A", "Strategy B"])
    test_logger.action("run_test", test_type="integration", duration=5.2)
    test_logger.analysis("performance_test", cpu_usage=45.2, memory_usage=67.8, success_rate=98.5)
    test_logger.result("Test completed successfully", tests_passed=15, tests_failed=0)

    print("✅ Example activities logged")

    # Show recent activities
    monitor = get_monitor()
    recent = monitor.get_recent_activities(5)

    print("\n📊 Recent activities:")
    for activity in recent:
        print(f"  {activity.timestamp} | {activity.agent_name} | {activity.activity_type} | {activity.description}")
