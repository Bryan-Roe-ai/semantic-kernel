#!/usr/bin/env python3
"""
Endless Improvement Loop
A self-evolving system that continuously improves the AI workspace through
automated optimization, learning, and adaptation.
"""

import os
import sys
import time
import json
import asyncio
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import random
import hashlib
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

# Custom JSON encoder for datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ImprovementMetric:
    """Represents a measurable improvement metric."""
    name: str
    value: float
    target: float
    weight: float = 1.0
    direction: str = "higher"  # "higher" or "lower" is better
    
    def score(self) -> float:
        """Calculate improvement score (0-1)."""
        if self.direction == "higher":
            return min(self.value / self.target, 1.0) if self.target > 0 else 0.0
        else:
            return max(1.0 - (self.value / self.target), 0.0) if self.target > 0 else 0.0

@dataclass
class ImprovementAction:
    """Represents an action that can improve the system."""
    id: str
    name: str
    description: str
    command: str
    args: List[str]
    priority: int = 5  # 1-10, 10 being highest
    impact_score: float = 0.0
    success_rate: float = 1.0
    last_executed: Optional[datetime] = None
    execution_count: int = 0
    
    def can_execute(self) -> bool:
        """Check if action can be executed now."""
        if self.last_executed is None:
            return True
        
        # Minimum cooldown based on priority
        cooldown_hours = 24 / max(self.priority, 1)
        return datetime.now() - self.last_executed > timedelta(hours=cooldown_hours)

class ImprovementAgent(ABC):
    """Abstract base class for improvement agents."""
    
    def __init__(self, name: str, workspace_root: Path):
        self.name = name
        self.workspace_root = workspace_root
        self.metrics_history: List[Dict] = []
        
    @abstractmethod
    async def analyze(self) -> List[ImprovementMetric]:
        """Analyze current state and return metrics."""
        pass
    
    @abstractmethod
    async def propose_actions(self, metrics: List[ImprovementMetric]) -> List[ImprovementAction]:
        """Propose actions based on current metrics."""
        pass
    
    @abstractmethod
    async def execute_action(self, action: ImprovementAction) -> Dict[str, Any]:
        """Execute an improvement action."""
        pass

class PerformanceAgent(ImprovementAgent):
    """Agent focused on system performance improvements."""
    
    async def analyze(self) -> List[ImprovementMetric]:
        """Analyze performance metrics."""
        metrics = []
        
        try:
            import psutil
            
            # CPU utilization
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(ImprovementMetric(
                name="cpu_efficiency",
                value=100 - cpu_percent,  # Higher efficiency = lower usage
                target=80.0,
                direction="higher"
            ))
            
            # Memory efficiency
            memory = psutil.virtual_memory()
            metrics.append(ImprovementMetric(
                name="memory_efficiency",
                value=100 - memory.percent,
                target=85.0,
                direction="higher"
            ))
            
            # Disk space
            disk = psutil.disk_usage(str(self.workspace_root))
            disk_free_percent = ((disk.total - disk.used) / disk.total) * 100
            metrics.append(ImprovementMetric(
                name="disk_space",
                value=disk_free_percent,
                target=20.0,  # At least 20% free
                direction="higher"
            ))
            
        except ImportError:
            # Fallback metrics when psutil is not available
            import shutil
            
            # Simulated CPU efficiency (random for demo)
            cpu_efficiency = random.uniform(60, 90)
            metrics.append(ImprovementMetric(
                name="cpu_efficiency",
                value=cpu_efficiency,
                target=80.0,
                direction="higher"
            ))
            
            # Disk space using shutil
            total, used, free = shutil.disk_usage(str(self.workspace_root))
            disk_free_percent = (free / total) * 100
            metrics.append(ImprovementMetric(
                name="disk_space",
                value=disk_free_percent,
                target=20.0,
                direction="higher"
            ))
            
            # Simulated memory efficiency
            memory_efficiency = random.uniform(50, 85)
            metrics.append(ImprovementMetric(
                name="memory_efficiency",
                value=memory_efficiency,
                target=85.0,
                direction="higher"
            ))
        
        return metrics
    
    async def propose_actions(self, metrics: List[ImprovementMetric]) -> List[ImprovementAction]:
        """Propose performance improvement actions."""
        actions = []
        
        # Standard optimization actions
        actions.extend([
            ImprovementAction(
                id="cleanup_temp",
                name="Cleanup Temporary Files",
                description="Remove temporary and cache files to free disk space",
                command="python",
                args=["scripts/ai_workspace_optimizer.py", "--quick"],
                priority=7
            ),
            ImprovementAction(
                id="optimize_cache",
                name="Optimize Cache",
                description="Optimize cache directories and remove old entries",
                command="python",
                args=["scripts/ai_workspace_optimizer.py", "--cache-only"],
                priority=6
            ),
            ImprovementAction(
                id="compress_logs",
                name="Compress Old Logs",
                description="Compress log files older than 7 days",
                command="find",
                args=["logs/", "-name", "*.log", "-mtime", "+7", "-exec", "gzip", "{}", ";"],
                priority=4
            )
        ])
        
        # Dynamic actions based on metrics
        for metric in metrics:
            if metric.score() < 0.7:  # Performance is below threshold
                if metric.name == "disk_space":
                    actions.append(ImprovementAction(
                        id="deep_cleanup",
                        name="Deep Disk Cleanup",
                        description="Perform comprehensive disk cleanup",
                        command="python",
                        args=["scripts/ai_workspace_optimizer.py", "--deep-clean"],
                        priority=9
                    ))
                elif metric.name == "memory_efficiency":
                    actions.append(ImprovementAction(
                        id="restart_services",
                        name="Restart Memory-Heavy Services",
                        description="Restart services to free memory",
                        command="python",
                        args=["scripts/restart_services.py"],
                        priority=8
                    ))
        
        return actions
    
    async def execute_action(self, action: ImprovementAction) -> Dict[str, Any]:
        """Execute a performance action."""
        try:
            result = subprocess.run(
                [action.command] + action.args,
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Action timed out after 5 minutes",
                "execution_time": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }

class CodeQualityAgent(ImprovementAgent):
    """Agent focused on code quality improvements."""
    
    async def analyze(self) -> List[ImprovementMetric]:
        """Analyze code quality metrics."""
        metrics = []
        
        # Test coverage (mock for now)
        test_coverage = await self._calculate_test_coverage()
        metrics.append(ImprovementMetric(
            name="test_coverage",
            value=test_coverage,
            target=80.0,
            direction="higher",
            weight=2.0
        ))
        
        # Code complexity
        complexity_score = await self._calculate_complexity()
        metrics.append(ImprovementMetric(
            name="code_complexity",
            value=complexity_score,
            target=5.0,  # Lower is better
            direction="lower"
        ))
        
        # Documentation coverage
        doc_coverage = await self._calculate_doc_coverage()
        metrics.append(ImprovementMetric(
            name="documentation_coverage",
            value=doc_coverage,
            target=70.0,
            direction="higher"
        ))
        
        return metrics
    
    async def _calculate_test_coverage(self) -> float:
        """Calculate test coverage percentage."""
        # Mock implementation - in real scenario, run coverage tools
        python_files = list(self.workspace_root.rglob("*.py"))
        test_files = list(self.workspace_root.rglob("test_*.py")) + list(self.workspace_root.rglob("*_test.py"))
        
        if not python_files:
            return 0.0
        
        # Simplified calculation
        coverage = min((len(test_files) / len(python_files)) * 100, 100.0)
        return coverage
    
    async def _calculate_complexity(self) -> float:
        """Calculate average code complexity."""
        # Mock implementation - in real scenario, use tools like radon
        python_files = list(self.workspace_root.rglob("*.py"))
        total_complexity = 0
        
        for file_path in python_files[:10]:  # Sample first 10 files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple complexity based on control flow keywords
                    complexity = content.count('if ') + content.count('for ') + content.count('while ') + content.count('try:')
                    total_complexity += complexity
            except:
                continue
        
        return total_complexity / max(len(python_files[:10]), 1)
    
    async def _calculate_doc_coverage(self) -> float:
        """Calculate documentation coverage."""
        python_files = list(self.workspace_root.rglob("*.py"))
        documented_functions = 0
        total_functions = 0
        
        for file_path in python_files[:10]:  # Sample first 10 files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for i, line in enumerate(lines):
                        if line.strip().startswith('def '):
                            total_functions += 1
                            # Check if next few lines contain docstring
                            for j in range(i+1, min(i+5, len(lines))):
                                if '"""' in lines[j] or "'''" in lines[j]:
                                    documented_functions += 1
                                    break
            except:
                continue
        
        return (documented_functions / max(total_functions, 1)) * 100
    
    async def propose_actions(self, metrics: List[ImprovementMetric]) -> List[ImprovementAction]:
        """Propose code quality improvement actions."""
        actions = []
        
        for metric in metrics:
            if metric.score() < 0.6:
                if metric.name == "test_coverage":
                    actions.append(ImprovementAction(
                        id="generate_tests",
                        name="Generate Missing Tests",
                        description="Generate unit tests for uncovered code",
                        command="python",
                        args=["scripts/generate_tests.py"],
                        priority=8
                    ))
                elif metric.name == "documentation_coverage":
                    actions.append(ImprovementAction(
                        id="add_docstrings",
                        name="Add Missing Docstrings",
                        description="Add docstrings to undocumented functions",
                        command="python",
                        args=["scripts/add_docstrings.py"],
                        priority=6
                    ))
                elif metric.name == "code_complexity":
                    actions.append(ImprovementAction(
                        id="refactor_complex_code",
                        name="Refactor Complex Code",
                        description="Identify and refactor overly complex functions",
                        command="python",
                        args=["scripts/refactor_assistant.py"],
                        priority=7
                    ))
        
        return actions
    
    async def execute_action(self, action: ImprovementAction) -> Dict[str, Any]:
        """Execute a code quality action."""
        # For now, simulate execution
        await asyncio.sleep(1)  # Simulate work
        
        return {
            "success": True,
            "message": f"Executed {action.name}",
            "execution_time": datetime.now().isoformat(),
            "simulated": True
        }

class LearningAgent(ImprovementAgent):
    """Agent that learns from past improvements and adapts strategies."""
    
    def __init__(self, name: str, workspace_root: Path):
        super().__init__(name, workspace_root)
        self.learning_history = self._load_learning_history()
        self.strategy_weights = self._initialize_strategy_weights()
    
    def _load_learning_history(self) -> List[Dict]:
        """Load historical learning data."""
        history_file = self.workspace_root / "logs" / "learning_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_learning_history(self):
        """Save learning history to disk."""
        history_file = self.workspace_root / "logs" / "learning_history.json"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(history_file, 'w') as f:
            json.dump(self.learning_history, f, indent=2, cls=DateTimeEncoder)
    
    def _initialize_strategy_weights(self) -> Dict[str, float]:
        """Initialize strategy weights based on historical success."""
        weights = {
            "performance_focus": 1.0,
            "quality_focus": 1.0,
            "aggressive_optimization": 0.5,
            "conservative_approach": 0.8,
            "experimental_features": 0.3
        }
        
        # Adjust weights based on learning history
        for record in self.learning_history[-50:]:  # Last 50 records
            strategy = record.get("strategy", "unknown")
            success = record.get("success", False)
            impact = record.get("impact_score", 0.0)
            
            if strategy in weights:
                if success and impact > 0.5:
                    weights[strategy] = min(weights[strategy] * 1.1, 2.0)
                elif not success:
                    weights[strategy] = max(weights[strategy] * 0.9, 0.1)
        
        return weights
    
    async def analyze(self) -> List[ImprovementMetric]:
        """Analyze learning and adaptation metrics."""
        metrics = []
        
        # Learning efficiency
        recent_successes = sum(1 for record in self.learning_history[-20:] if record.get("success", False))
        learning_efficiency = (recent_successes / 20) * 100 if len(self.learning_history) >= 20 else 50.0
        
        metrics.append(ImprovementMetric(
            name="learning_efficiency",
            value=learning_efficiency,
            target=80.0,
            direction="higher",
            weight=1.5
        ))
        
        # Strategy diversity
        recent_strategies = [record.get("strategy") for record in self.learning_history[-30:]]
        unique_strategies = len(set(filter(None, recent_strategies)))
        strategy_diversity = (unique_strategies / 5) * 100  # Assuming 5 main strategies
        
        metrics.append(ImprovementMetric(
            name="strategy_diversity",
            value=strategy_diversity,
            target=60.0,
            direction="higher"
        ))
        
        return metrics
    
    async def propose_actions(self, metrics: List[ImprovementMetric]) -> List[ImprovementAction]:
        """Propose learning-based improvement actions."""
        actions = []
        
        # Analyze which strategies have been most successful
        successful_actions = [
            record for record in self.learning_history[-100:]
            if record.get("success", False) and record.get("impact_score", 0) > 0.7
        ]
        
        # Propose retrying successful actions with variations
        for action_record in successful_actions[-5:]:  # Top 5 recent successes
            action_id = action_record.get("action_id", "unknown")
            actions.append(ImprovementAction(
                id=f"retry_{action_id}",
                name=f"Retry Successful: {action_record.get('action_name', 'Unknown')}",
                description=f"Retry previously successful action with learned optimizations",
                command="python",
                args=["scripts/adaptive_execution.py", action_id],
                priority=min(9, action_record.get("priority", 5) + 2)
            ))
        
        # Propose experimental actions based on learning
        if self.strategy_weights.get("experimental_features", 0) > 0.5:
            actions.append(ImprovementAction(
                id="experimental_optimization",
                name="Experimental Optimization",
                description="Try new optimization techniques based on recent learnings",
                command="python",
                args=["scripts/experimental_optimizer.py"],
                priority=4
            ))
        
        return actions
    
    async def execute_action(self, action: ImprovementAction) -> Dict[str, Any]:
        """Execute and learn from an action."""
        start_time = datetime.now()
        
        # Simulate execution with learning
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Determine success based on action characteristics and learned patterns
        success_probability = self._calculate_success_probability(action)
        success = random.random() < success_probability
        
        impact_score = random.uniform(0.3, 1.0) if success else random.uniform(0.0, 0.3)
        
        # Record learning
        learning_record = {
            "timestamp": start_time.isoformat(),
            "action_id": action.id,
            "action_name": action.name,
            "strategy": self._determine_strategy(action),
            "success": success,
            "impact_score": impact_score,
            "priority": action.priority,
            "execution_time_seconds": (datetime.now() - start_time).total_seconds()
        }
        
        self.learning_history.append(learning_record)
        self._save_learning_history()
        
        # Update strategy weights based on outcome
        self._update_strategy_weights(learning_record)
        
        return {
            "success": success,
            "impact_score": impact_score,
            "learning_record": learning_record,
            "execution_time": datetime.now().isoformat()
        }
    
    def _calculate_success_probability(self, action: ImprovementAction) -> float:
        """Calculate success probability based on learned patterns."""
        base_probability = action.success_rate
        
        # Adjust based on strategy weights
        strategy = self._determine_strategy(action)
        strategy_weight = self.strategy_weights.get(strategy, 1.0)
        
        # Adjust based on historical performance of similar actions
        similar_actions = [
            record for record in self.learning_history
            if record.get("action_name", "").lower() in action.name.lower()
        ]
        
        if similar_actions:
            historical_success_rate = sum(record.get("success", False) for record in similar_actions) / len(similar_actions)
            base_probability = (base_probability + historical_success_rate) / 2
        
        return min(base_probability * strategy_weight, 1.0)
    
    def _determine_strategy(self, action: ImprovementAction) -> str:
        """Determine which strategy an action belongs to."""
        action_name = action.name.lower()
        
        if "cleanup" in action_name or "optimize" in action_name:
            return "performance_focus"
        elif "test" in action_name or "document" in action_name or "refactor" in action_name:
            return "quality_focus"
        elif "experimental" in action_name:
            return "experimental_features"
        elif action.priority >= 8:
            return "aggressive_optimization"
        else:
            return "conservative_approach"
    
    def _update_strategy_weights(self, learning_record: Dict):
        """Update strategy weights based on learning outcomes."""
        strategy = learning_record.get("strategy")
        success = learning_record.get("success", False)
        impact = learning_record.get("impact_score", 0.0)
        
        if strategy in self.strategy_weights:
            if success and impact > 0.6:
                self.strategy_weights[strategy] = min(self.strategy_weights[strategy] * 1.05, 2.0)
            elif not success:
                self.strategy_weights[strategy] = max(self.strategy_weights[strategy] * 0.95, 0.1)

class EndlessImprovementLoop:
    """Main orchestrator for the endless improvement system."""
    
    def __init__(self, workspace_root: str = "/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_root = Path(workspace_root)
        self.running = False
        self.agents: List[ImprovementAgent] = []
        self.improvement_history: List[Dict] = []
        self.cycle_count = 0
        
        # Initialize agents
        self._initialize_agents()
        
        # Setup directories
        self.logs_dir = self.workspace_root / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
    def _initialize_agents(self):
        """Initialize improvement agents."""
        self.agents = [
            PerformanceAgent("performance", self.workspace_root),
            CodeQualityAgent("code_quality", self.workspace_root),
            LearningAgent("learning", self.workspace_root)
        ]
        
        # Try to import and add additional agents
        try:
            from security_agent import SecurityAgent
            self.agents.append(SecurityAgent("security", self.workspace_root))
        except ImportError:
            logger.info("Security agent not available")
        
        try:
            from infrastructure_agent import InfrastructureAgent
            self.agents.append(InfrastructureAgent("infrastructure", self.workspace_root))
        except ImportError:
            logger.info("Infrastructure agent not available")
    
    async def start_endless_loop(self, cycle_interval: int = 300):  # 5 minutes default
        """Start the endless improvement loop."""
        self.running = True
        
        print("🚀 Starting Endless Improvement Loop")
        print("=" * 60)
        print(f"📁 Workspace: {self.workspace_root}")
        print(f"⏰ Cycle interval: {cycle_interval} seconds")
        print(f"🤖 Active agents: {len(self.agents)}")
        print("🔄 Beginning continuous improvement...\n")
        
        try:
            while self.running:
                await self._run_improvement_cycle()
                
                if self.running:  # Check if still running after cycle
                    print(f"\n⏳ Waiting {cycle_interval} seconds until next cycle...")
                    await asyncio.sleep(cycle_interval)
                    
        except KeyboardInterrupt:
            print("\n🛑 Endless improvement loop stopped by user")
        except Exception as e:
            logger.error(f"Error in improvement loop: {e}")
        finally:
            self.running = False
            await self._save_final_report()
    
    async def _run_improvement_cycle(self):
        """Run a single improvement cycle."""
        self.cycle_count += 1
        cycle_start = datetime.now()
        
        print(f"🔄 === Improvement Cycle #{self.cycle_count} ===")
        print(f"🕒 Started at: {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}")
        
        cycle_results = {
            "cycle_number": self.cycle_count,
            "start_time": cycle_start.isoformat(),
            "agent_results": {},
            "actions_executed": [],
            "overall_improvement_score": 0.0
        }
        
        all_metrics = []
        all_actions = []
        
        # Analyze current state with all agents
        print("\n📊 Phase 1: Analysis")
        for agent in self.agents:
            try:
                print(f"   🔍 {agent.name} agent analyzing...")
                metrics = await agent.analyze()
                all_metrics.extend(metrics)
                
                agent_score = sum(metric.score() * metric.weight for metric in metrics) / sum(metric.weight for metric in metrics)
                print(f"   📈 {agent.name} score: {agent_score:.2f}")
                
                cycle_results["agent_results"][agent.name] = {
                    "metrics": [asdict(metric) for metric in metrics],
                    "score": agent_score
                }
            except Exception as e:
                logger.error(f"Error in {agent.name} analysis: {e}")
                cycle_results["agent_results"][agent.name] = {"error": str(e)}
        
        # Propose improvement actions
        print("\n💡 Phase 2: Action Proposal")
        for agent in self.agents:
            try:
                print(f"   🧠 {agent.name} agent proposing actions...")
                actions = await agent.propose_actions(all_metrics)
                all_actions.extend(actions)
                print(f"   📝 Proposed {len(actions)} actions")
            except Exception as e:
                logger.error(f"Error in {agent.name} action proposal: {e}")
        
        # Prioritize and execute actions
        print("\n⚡ Phase 3: Action Execution")
        executable_actions = [action for action in all_actions if action.can_execute()]
        executable_actions.sort(key=lambda x: x.priority, reverse=True)
        
        # Execute top priority actions (limit to 5 per cycle to avoid overwhelming)
        max_actions = min(5, len(executable_actions))
        executed_actions = []
        
        for i, action in enumerate(executable_actions[:max_actions]):
            print(f"   🎯 Executing ({i+1}/{max_actions}): {action.name}")
            
            try:
                # Find the agent that can execute this action
                executing_agent = None
                for agent in self.agents:
                    if hasattr(agent, 'execute_action'):
                        executing_agent = agent
                        break
                
                if executing_agent:
                    result = await executing_agent.execute_action(action)
                    action.last_executed = datetime.now()
                    action.execution_count += 1
                    
                    if result.get("success", False):
                        action.impact_score = result.get("impact_score", 0.5)
                        print(f"   ✅ Success: {action.name}")
                    else:
                        print(f"   ❌ Failed: {action.name}")
                        action.success_rate *= 0.9  # Reduce success rate
                    
                    executed_actions.append({
                        "action": {
                            "id": action.id,
                            "name": action.name,
                            "description": action.description,
                            "priority": action.priority,
                            "impact_score": action.impact_score,
                            "success_rate": action.success_rate,
                            "last_executed": action.last_executed.isoformat() if action.last_executed else None,
                            "execution_count": action.execution_count
                        },
                        "result": result
                    })
                else:
                    print(f"   ⚠️  No agent available to execute: {action.name}")
                    
            except Exception as e:
                logger.error(f"Error executing {action.name}: {e}")
                executed_actions.append({
                    "action": {
                        "id": action.id,
                        "name": action.name,
                        "description": action.description,
                        "priority": action.priority,
                        "impact_score": action.impact_score,
                        "success_rate": action.success_rate,
                        "last_executed": action.last_executed.isoformat() if action.last_executed else None,
                        "execution_count": action.execution_count
                    },
                    "result": {"success": False, "error": str(e)}
                })
        
        cycle_results["actions_executed"] = executed_actions
        
        # Calculate overall improvement score
        if all_metrics:
            overall_score = sum(metric.score() * metric.weight for metric in all_metrics) / sum(metric.weight for metric in all_metrics)
            cycle_results["overall_improvement_score"] = overall_score
            
            print(f"\n📊 Cycle Results:")
            print(f"   🎯 Overall improvement score: {overall_score:.2f}")
            print(f"   🔧 Actions executed: {len(executed_actions)}")
            print(f"   ✅ Successful actions: {sum(1 for action in executed_actions if action['result'].get('success', False))}")
        
        cycle_results["end_time"] = datetime.now().isoformat()
        cycle_results["duration_seconds"] = (datetime.now() - cycle_start).total_seconds()
        
        # Save cycle results
        self.improvement_history.append(cycle_results)
        await self._save_cycle_report(cycle_results)
        
        print(f"🕒 Cycle completed in {cycle_results['duration_seconds']:.1f} seconds")
    
    async def _save_cycle_report(self, cycle_results: Dict):
        """Save individual cycle report."""
        report_file = self.logs_dir / f"improvement_cycle_{self.cycle_count:04d}.json"
        
        with open(report_file, 'w') as f:
            json.dump(cycle_results, f, indent=2, cls=DateTimeEncoder)
    
    async def _save_final_report(self):
        """Save final improvement report."""
        if not self.improvement_history:
            return
        
        final_report = {
            "summary": {
                "total_cycles": len(self.improvement_history),
                "total_runtime_hours": sum(cycle.get("duration_seconds", 0) for cycle in self.improvement_history) / 3600,
                "total_actions_executed": sum(len(cycle.get("actions_executed", [])) for cycle in self.improvement_history),
                "average_improvement_score": sum(cycle.get("overall_improvement_score", 0) for cycle in self.improvement_history) / len(self.improvement_history),
                "final_timestamp": datetime.now().isoformat()
            },
            "cycles": self.improvement_history[-10:],  # Last 10 cycles
            "trends": self._analyze_trends()
        }
        
        report_file = self.logs_dir / "endless_improvement_final_report.json"
        with open(report_file, 'w') as f:
            json.dump(final_report, f, indent=2, cls=DateTimeEncoder)
        
        print(f"\n📄 Final report saved to: {report_file}")
        print(f"📊 Total cycles: {final_report['summary']['total_cycles']}")
        print(f"⏰ Total runtime: {final_report['summary']['total_runtime_hours']:.1f} hours")
        print(f"🎯 Average improvement score: {final_report['summary']['average_improvement_score']:.2f}")
    
    def _analyze_trends(self) -> Dict[str, Any]:
        """Analyze improvement trends over time."""
        if len(self.improvement_history) < 2:
            return {"insufficient_data": True}
        
        scores = [cycle.get("overall_improvement_score", 0) for cycle in self.improvement_history]
        
        # Calculate trend
        if len(scores) >= 5:
            recent_avg = sum(scores[-5:]) / 5
            early_avg = sum(scores[:5]) / 5
            trend = "improving" if recent_avg > early_avg else "declining" if recent_avg < early_avg else "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "improvement_trend": trend,
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "score_variance": max(scores) - min(scores),
            "recent_average": sum(scores[-5:]) / min(5, len(scores))
        }
    
    def stop(self):
        """Stop the endless improvement loop."""
        self.running = False
        print("🛑 Stopping endless improvement loop...")

def main():
    """Main function to start the endless improvement loop."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Endless Improvement Loop for AI Workspace")
    parser.add_argument("--workspace", type=str, default="/workspaces/semantic-kernel/ai-workspace",
                       help="Path to workspace root")
    parser.add_argument("--interval", type=int, default=300,
                       help="Cycle interval in seconds (default: 300)")
    parser.add_argument("--cycles", type=int, default=0,
                       help="Number of cycles to run (0 = endless)")
    
    args = parser.parse_args()
    
    loop = EndlessImprovementLoop(args.workspace)
    
    async def run_limited_cycles():
        """Run a limited number of cycles."""
        for i in range(args.cycles):
            await loop._run_improvement_cycle()
            if i < args.cycles - 1:  # Don't wait after last cycle
                await asyncio.sleep(args.interval)
        await loop._save_final_report()
    
    try:
        if args.cycles > 0:
            print(f"🔄 Running {args.cycles} improvement cycles...")
            asyncio.run(run_limited_cycles())
        else:
            print("🔄 Starting endless improvement loop...")
            asyncio.run(loop.start_endless_loop(args.interval))
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Improvement loop stopped.")

if __name__ == "__main__":
    main()
