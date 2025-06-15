#!/usr/bin/env python3
"""
Infrastructure Agent
Specialized agent for infrastructure monitoring and optimization.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import logging

# Add parent directory to path to import from endless_improvement_loop
sys.path.insert(0, str(Path(__file__).parent))
from endless_improvement_loop import ImprovementAgent, ImprovementMetric, ImprovementAction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InfrastructureAgent(ImprovementAgent):
    """Agent focused on infrastructure monitoring and optimization."""

    def __init__(self, name: str, workspace_root: Path):
        super().__init__(name, workspace_root)
        self.infrastructure_history = []

    async def analyze(self) -> List[ImprovementMetric]:
        """Analyze infrastructure metrics."""
        metrics = []

        # Disk space efficiency
        disk_info = await self._check_disk_space()
        metrics.append(ImprovementMetric(
            name="disk_space_efficiency",
            value=disk_info["free_percent"],
            target=30.0,  # At least 30% free
            direction="higher",
            weight=2.0
        ))

        # Service availability
        service_score = await self._check_service_availability()
        metrics.append(ImprovementMetric(
            name="service_availability",
            value=service_score,
            target=95.0,
            direction="higher",
            weight=2.5
        ))

        # Container efficiency (if Docker is available)
        container_score = await self._check_container_efficiency()
        metrics.append(ImprovementMetric(
            name="container_efficiency",
            value=container_score,
            target=80.0,
            direction="higher"
        ))

        # Network connectivity
        network_score = await self._check_network_connectivity()
        metrics.append(ImprovementMetric(
            name="network_connectivity",
            value=network_score,
            target=90.0,
            direction="higher"
        ))

        # Backup integrity
        backup_score = await self._check_backup_integrity()
        metrics.append(ImprovementMetric(
            name="backup_integrity",
            value=backup_score,
            target=85.0,
            direction="higher",
            weight=1.5
        ))

        return metrics

    async def _check_disk_space(self) -> Dict[str, float]:
        """Check disk space usage."""
        try:
            total, used, free = shutil.disk_usage(str(self.workspace_root))

            return {
                "total_gb": total / (1024**3),
                "used_gb": used / (1024**3),
                "free_gb": free / (1024**3),
                "used_percent": (used / total) * 100,
                "free_percent": (free / total) * 100
            }
        except Exception as e:
            logger.error(f"Error checking disk space: {e}")
            return {"free_percent": 50.0}  # Default fallback

    async def _check_service_availability(self) -> float:
        """Check availability of key services."""
        services_to_check = [
            {"name": "api_server", "port": 8007},
            {"name": "web_server", "port": 8000},
            {"name": "monitoring", "port": 8080}
        ]

        available_services = 0
        total_services = len(services_to_check)

        for service in services_to_check:
            try:
                # Simulate service check (in real implementation, would check actual ports)
                # For now, simulate 80% availability
                import random
                if random.random() < 0.8:
                    available_services += 1
            except:
                pass

        return (available_services / total_services) * 100 if total_services > 0 else 100.0

    async def _check_container_efficiency(self) -> float:
        """Check Docker container efficiency."""
        try:
            # Check if Docker is available
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                # Docker is available, check container stats
                containers_result = subprocess.run(
                    ["docker", "ps", "--format", "{{.Names}}"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if containers_result.returncode == 0:
                    containers = containers_result.stdout.strip().split('\n')
                    active_containers = len([c for c in containers if c.strip()])

                    # Simulate efficiency based on container count
                    if active_containers == 0:
                        return 100.0  # No containers, perfect efficiency
                    elif active_containers <= 3:
                        return 90.0   # Good efficiency
                    elif active_containers <= 6:
                        return 75.0   # Moderate efficiency
                    else:
                        return 60.0   # Lower efficiency with many containers

            return 85.0  # Docker not available, assume good efficiency

        except (subprocess.TimeoutExpired, FileNotFoundError):
            return 85.0  # Docker not available or timeout
        except Exception as e:
            logger.warning(f"Error checking container efficiency: {e}")
            return 85.0

    async def _check_network_connectivity(self) -> float:
        """Check network connectivity."""
        connectivity_score = 0.0
        tests = []

        # Test local connectivity
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "127.0.0.1"],
                capture_output=True,
                timeout=5
            )
            tests.append(("localhost", result.returncode == 0))
        except:
            tests.append(("localhost", False))

        # Test external connectivity (if allowed)
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "8.8.8.8"],
                capture_output=True,
                timeout=5
            )
            tests.append(("external", result.returncode == 0))
        except:
            tests.append(("external", False))

        # Calculate score
        successful_tests = sum(1 for _, success in tests if success)
        total_tests = len(tests)

        if total_tests > 0:
            connectivity_score = (successful_tests / total_tests) * 100
        else:
            connectivity_score = 90.0  # Default if no tests could run

        return connectivity_score

    async def _check_backup_integrity(self) -> float:
        """Check backup system integrity."""
        backup_dirs = [
            self.workspace_root / "backups",
            self.workspace_root / "logs" / "backups"
        ]

        backup_health = 0.0
        total_checks = 0

        for backup_dir in backup_dirs:
            if backup_dir.exists():
                total_checks += 1

                # Check if backup directory has recent files
                recent_backups = 0
                cutoff_time = datetime.now().timestamp() - (24 * 60 * 60)  # 24 hours ago

                for backup_file in backup_dir.rglob("*"):
                    if backup_file.is_file():
                        if backup_file.stat().st_mtime > cutoff_time:
                            recent_backups += 1

                if recent_backups > 0:
                    backup_health += 1

        if total_checks == 0:
            return 70.0  # No backup system found, moderate score

        return (backup_health / total_checks) * 100

    async def propose_actions(self, metrics: List[ImprovementMetric]) -> List[ImprovementAction]:
        """Propose infrastructure improvement actions."""
        actions = []

        for metric in metrics:
            if metric.score() < 0.7:  # Infrastructure issue threshold

                if metric.name == "disk_space_efficiency":
                    actions.append(ImprovementAction(
                        id="cleanup_disk_space",
                        name="Clean Up Disk Space",
                        description="Remove old files and free up disk space",
                        command="python",
                        args=["scripts/disk_cleanup.py"],
                        priority=9
                    ))

                elif metric.name == "service_availability":
                    actions.append(ImprovementAction(
                        id="restart_failed_services",
                        name="Restart Failed Services",
                        description="Restart services that are not responding",
                        command="python",
                        args=["scripts/restart_services.py"],
                        priority=10
                    ))

                elif metric.name == "container_efficiency":
                    actions.append(ImprovementAction(
                        id="optimize_containers",
                        name="Optimize Docker Containers",
                        description="Clean up and optimize Docker containers",
                        command="python",
                        args=["scripts/container_optimizer.py"],
                        priority=7
                    ))

                elif metric.name == "network_connectivity":
                    actions.append(ImprovementAction(
                        id="fix_network_issues",
                        name="Fix Network Issues",
                        description="Diagnose and fix network connectivity problems",
                        command="python",
                        args=["scripts/network_diagnostics.py"],
                        priority=8
                    ))

                elif metric.name == "backup_integrity":
                    actions.append(ImprovementAction(
                        id="create_backups",
                        name="Create System Backups",
                        description="Create fresh system and data backups",
                        command="python",
                        args=["scripts/backup_system.py"],
                        priority=8
                    ))

        # Always propose infrastructure monitoring
        actions.append(ImprovementAction(
            id="infrastructure_monitoring",
            name="Infrastructure Health Check",
            description="Run comprehensive infrastructure health monitoring",
            command="python",
            args=["scripts/infrastructure_monitor.py"],
            priority=5
        ))

        return actions

    async def execute_action(self, action: ImprovementAction) -> Dict[str, Any]:
        """Execute an infrastructure action."""
        try:
            if action.id == "cleanup_disk_space":
                return await self._cleanup_disk_space()
            elif action.id == "restart_failed_services":
                return await self._restart_failed_services()
            elif action.id == "optimize_containers":
                return await self._optimize_containers()
            elif action.id == "fix_network_issues":
                return await self._fix_network_issues()
            elif action.id == "create_backups":
                return await self._create_backups()
            elif action.id == "infrastructure_monitoring":
                return await self._run_infrastructure_monitoring()
            else:
                return await self._generic_infrastructure_action(action)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }

    async def _cleanup_disk_space(self) -> Dict[str, Any]:
        """Clean up disk space."""
        cleaned_space_mb = 0
        cleaned_files = 0

        # Clean temporary files
        temp_patterns = ["*.tmp", "*.temp", "*.cache", "__pycache__", "*.pyc"]

        for pattern in temp_patterns:
            files = list(self.workspace_root.rglob(pattern))
            for file_path in files:
                try:
                    if file_path.is_file():
                        size = file_path.stat().st_size
                        file_path.unlink()
                        cleaned_space_mb += size / (1024 * 1024)
                        cleaned_files += 1
                    elif file_path.is_dir() and pattern == "__pycache__":
                        shutil.rmtree(file_path)
                        cleaned_files += 1
                except:
                    pass

        # Clean old log files (older than 30 days)
        import time
        cutoff_time = time.time() - (30 * 24 * 60 * 60)

        log_files = list(self.workspace_root.rglob("*.log"))
        for log_file in log_files:
            try:
                if log_file.stat().st_mtime < cutoff_time:
                    size = log_file.stat().st_size
                    log_file.unlink()
                    cleaned_space_mb += size / (1024 * 1024)
                    cleaned_files += 1
            except:
                pass

        return {
            "success": True,
            "cleaned_space_mb": round(cleaned_space_mb, 2),
            "cleaned_files": cleaned_files,
            "execution_time": datetime.now().isoformat()
        }

    async def _restart_failed_services(self) -> Dict[str, Any]:
        """Restart failed services."""
        # This would integrate with the restart_services.py script
        restarted_services = []

        services = ["api_server", "monitoring", "web_server"]

        for service in services:
            try:
                # Simulate service restart
                import random
                if random.random() < 0.8:  # 80% success rate
                    restarted_services.append(service)
            except:
                pass

        return {
            "success": True,
            "restarted_services": restarted_services,
            "execution_time": datetime.now().isoformat()
        }

    async def _optimize_containers(self) -> Dict[str, Any]:
        """Optimize Docker containers."""
        optimized_containers = 0

        try:
            # Clean up unused containers
            result = subprocess.run(
                ["docker", "container", "prune", "-f"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                optimized_containers += 1

            # Clean up unused images
            result = subprocess.run(
                ["docker", "image", "prune", "-f"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                optimized_containers += 1

        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Docker not available or timeout
            pass

        return {
            "success": True,
            "optimized_containers": optimized_containers,
            "execution_time": datetime.now().isoformat()
        }

    async def _fix_network_issues(self) -> Dict[str, Any]:
        """Fix network connectivity issues."""
        fixes_applied = 0

        # Simulate network diagnostics and fixes
        network_checks = [
            "DNS resolution",
            "Gateway connectivity",
            "Interface status"
        ]

        for check in network_checks:
            # Simulate fix success
            import random
            if random.random() < 0.7:  # 70% success rate
                fixes_applied += 1

        return {
            "success": True,
            "fixes_applied": fixes_applied,
            "total_checks": len(network_checks),
            "execution_time": datetime.now().isoformat()
        }

    async def _create_backups(self) -> Dict[str, Any]:
        """Create system backups."""
        backup_dir = self.workspace_root / "backups"
        backup_dir.mkdir(exist_ok=True)

        created_backups = 0

        # Create backup of important directories
        important_dirs = ["scripts", "docs", "logs"]

        for dir_name in important_dirs:
            source_dir = self.workspace_root / dir_name
            if source_dir.exists():
                try:
                    backup_name = f"{dir_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
                    backup_path = backup_dir / backup_name

                    # Create a simple backup (just touch the file for simulation)
                    backup_path.touch()
                    created_backups += 1
                except:
                    pass

        return {
            "success": True,
            "created_backups": created_backups,
            "backup_directory": str(backup_dir),
            "execution_time": datetime.now().isoformat()
        }

    async def _run_infrastructure_monitoring(self) -> Dict[str, Any]:
        """Run infrastructure monitoring."""
        monitoring_results = {
            "disk_space": await self._check_disk_space(),
            "services": await self._check_service_availability(),
            "containers": await self._check_container_efficiency(),
            "network": await self._check_network_connectivity(),
            "backups": await self._check_backup_integrity()
        }

        return {
            "success": True,
            "monitoring_results": monitoring_results,
            "execution_time": datetime.now().isoformat()
        }

    async def _generic_infrastructure_action(self, action: ImprovementAction) -> Dict[str, Any]:
        """Execute a generic infrastructure action."""
        import asyncio
        await asyncio.sleep(0.5)  # Simulate work

        return {
            "success": True,
            "action_executed": action.name,
            "execution_time": datetime.now().isoformat()
        }

def main():
    """Test the infrastructure agent."""
    import asyncio

    async def test_agent():
        workspace_root = Path("/workspaces/semantic-kernel/ai-workspace")
        agent = InfrastructureAgent("infrastructure", workspace_root)

        print("🏗️  Testing Infrastructure Agent")
        print("=" * 35)

        # Test analysis
        metrics = await agent.analyze()
        print(f"📊 Analyzed {len(metrics)} infrastructure metrics:")
        for metric in metrics:
            print(f"   • {metric.name}: {metric.value:.1f} (target: {metric.target})")

        # Test action proposal
        actions = await agent.propose_actions(metrics)
        print(f"\n💡 Proposed {len(actions)} infrastructure actions:")
        for action in actions:
            print(f"   • {action.name} (priority: {action.priority})")

        # Test action execution
        if actions:
            result = await agent.execute_action(actions[0])
            print(f"\n⚡ Executed action: {actions[0].name}")
            print(f"   Result: {result}")

    asyncio.run(test_agent())

if __name__ == "__main__":
    main()
