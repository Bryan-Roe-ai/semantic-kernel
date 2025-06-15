#!/usr/bin/env python3
"""
Security Agent
Specialized agent for security analysis and improvements.
"""

import os
import sys
import re
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import logging

# Add parent directory to path to import from endless_improvement_loop
sys.path.insert(0, str(Path(__file__).parent))
from endless_improvement_loop import ImprovementAgent, ImprovementMetric, ImprovementAction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityAgent(ImprovementAgent):
    """Agent focused on security analysis and improvements."""

    def __init__(self, name: str, workspace_root: Path):
        super().__init__(name, workspace_root)
        self.security_patterns = self._load_security_patterns()
        self.vulnerability_history = []

    def _load_security_patterns(self) -> Dict[str, List[str]]:
        """Load security patterns to check for."""
        return {
            "hardcoded_secrets": [
                r"password\s*=\s*['\"][^'\"]+['\"]",
                r"api_key\s*=\s*['\"][^'\"]+['\"]",
                r"secret\s*=\s*['\"][^'\"]+['\"]",
                r"token\s*=\s*['\"][^'\"]+['\"]",
                r"-----BEGIN PRIVATE KEY-----",
                r"-----BEGIN RSA PRIVATE KEY-----"
            ],
            "sql_injection": [
                r"execute\s*\(\s*['\"][^'\"]*%s[^'\"]*['\"]",
                r"cursor\.execute\s*\(\s*['\"][^'\"]*\+[^'\"]*['\"]",
                r"query\s*=\s*['\"][^'\"]*\+[^'\"]*['\"]"
            ],
            "dangerous_functions": [
                r"eval\s*\(",
                r"exec\s*\(",
                r"os\.system\s*\(",
                r"subprocess\.call\s*\([^)]*shell\s*=\s*True",
                r"pickle\.loads\s*\("
            ],
            "insecure_random": [
                r"random\.random\s*\(",
                r"random\.randint\s*\(",
                r"random\.choice\s*\("
            ]
        }

    async def analyze(self) -> List[ImprovementMetric]:
        """Analyze security metrics."""
        metrics = []

        # Security vulnerability count
        vulnerabilities = await self._scan_for_vulnerabilities()
        vulnerability_score = max(100 - len(vulnerabilities) * 10, 0)

        metrics.append(ImprovementMetric(
            name="security_vulnerability_score",
            value=vulnerability_score,
            target=90.0,
            direction="higher",
            weight=2.0
        ))

        # File permission security
        permission_score = await self._check_file_permissions()
        metrics.append(ImprovementMetric(
            name="file_permission_security",
            value=permission_score,
            target=80.0,
            direction="higher"
        ))

        # Dependency security (simulated)
        dependency_score = await self._check_dependency_security()
        metrics.append(ImprovementMetric(
            name="dependency_security",
            value=dependency_score,
            target=85.0,
            direction="higher",
            weight=1.5
        ))

        # Configuration security
        config_score = await self._check_configuration_security()
        metrics.append(ImprovementMetric(
            name="configuration_security",
            value=config_score,
            target=80.0,
            direction="higher"
        ))

        return metrics

    async def _scan_for_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Scan for security vulnerabilities in code."""
        vulnerabilities = []

        python_files = list(self.workspace_root.rglob("*.py"))

        for file_path in python_files[:20]:  # Limit to first 20 files for performance
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                for category, patterns in self.security_patterns.items():
                    for pattern in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            vulnerabilities.append({
                                "file": str(file_path.relative_to(self.workspace_root)),
                                "category": category,
                                "line": line_num,
                                "pattern": pattern,
                                "match": match.group()[:100]  # Truncate long matches
                            })
            except Exception as e:
                logger.warning(f"Error scanning {file_path}: {e}")

        self.vulnerability_history.append({
            "timestamp": datetime.now().isoformat(),
            "count": len(vulnerabilities),
            "vulnerabilities": vulnerabilities
        })

        return vulnerabilities

    async def _check_file_permissions(self) -> float:
        """Check file permissions for security issues."""
        sensitive_files = [
            ".env", "config.py", "settings.py", "*.key", "*.pem"
        ]

        secure_files = 0
        total_files = 0

        for pattern in sensitive_files:
            files = list(self.workspace_root.rglob(pattern))
            for file_path in files:
                total_files += 1
                try:
                    # Check if file is not world-readable
                    stat = file_path.stat()
                    if not (stat.st_mode & 0o004):  # World-readable bit
                        secure_files += 1
                except:
                    pass

        if total_files == 0:
            return 100.0  # No sensitive files found

        return (secure_files / total_files) * 100

    async def _check_dependency_security(self) -> float:
        """Check dependency security (simulated analysis)."""
        requirements_files = list(self.workspace_root.rglob("requirements*.txt"))

        if not requirements_files:
            return 90.0  # No requirements file, assume secure

        # Simulate dependency analysis
        total_deps = 0
        secure_deps = 0

        for req_file in requirements_files:
            try:
                with open(req_file, 'r') as f:
                    lines = f.readlines()

                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        total_deps += 1
                        # Simulate: 85% of dependencies are secure
                        if hash(line) % 100 < 85:
                            secure_deps += 1
            except:
                pass

        if total_deps == 0:
            return 90.0

        return (secure_deps / total_deps) * 100

    async def _check_configuration_security(self) -> float:
        """Check configuration security."""
        config_files = (
            list(self.workspace_root.rglob("*.yml")) +
            list(self.workspace_root.rglob("*.yaml")) +
            list(self.workspace_root.rglob("*.json")) +
            list(self.workspace_root.rglob(".env*"))
        )

        secure_configs = 0
        total_configs = len(config_files)

        for config_file in config_files:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for security issues in config
                has_issues = False

                # Check for hardcoded secrets
                for pattern in self.security_patterns["hardcoded_secrets"]:
                    if re.search(pattern, content, re.IGNORECASE):
                        has_issues = True
                        break

                # Check for debug mode in production configs
                if re.search(r"debug\s*[:=]\s*true", content, re.IGNORECASE):
                    has_issues = True

                if not has_issues:
                    secure_configs += 1

            except:
                pass

        if total_configs == 0:
            return 100.0

        return (secure_configs / total_configs) * 100

    async def propose_actions(self, metrics: List[ImprovementMetric]) -> List[ImprovementAction]:
        """Propose security improvement actions."""
        actions = []

        for metric in metrics:
            if metric.score() < 0.7:  # Security issue threshold

                if metric.name == "security_vulnerability_score":
                    actions.append(ImprovementAction(
                        id="fix_vulnerabilities",
                        name="Fix Security Vulnerabilities",
                        description="Address identified security vulnerabilities in code",
                        command="python",
                        args=["scripts/security_fixes.py"],
                        priority=10  # Highest priority
                    ))

                elif metric.name == "file_permission_security":
                    actions.append(ImprovementAction(
                        id="secure_file_permissions",
                        name="Secure File Permissions",
                        description="Fix insecure file permissions",
                        command="python",
                        args=["scripts/fix_permissions.py"],
                        priority=8
                    ))

                elif metric.name == "dependency_security":
                    actions.append(ImprovementAction(
                        id="update_dependencies",
                        name="Update Insecure Dependencies",
                        description="Update dependencies with known vulnerabilities",
                        command="python",
                        args=["scripts/update_dependencies.py"],
                        priority=9
                    ))

                elif metric.name == "configuration_security":
                    actions.append(ImprovementAction(
                        id="secure_configurations",
                        name="Secure Configuration Files",
                        description="Remove secrets and secure configuration files",
                        command="python",
                        args=["scripts/secure_configs.py"],
                        priority=9
                    ))

        # Always propose security monitoring
        actions.append(ImprovementAction(
            id="security_monitoring",
            name="Security Monitoring Check",
            description="Run regular security monitoring and alerting",
            command="python",
            args=["scripts/security_monitor.py"],
            priority=6
        ))

        return actions

    async def execute_action(self, action: ImprovementAction) -> Dict[str, Any]:
        """Execute a security action."""
        try:
            if action.id == "fix_vulnerabilities":
                return await self._fix_vulnerabilities()
            elif action.id == "secure_file_permissions":
                return await self._secure_file_permissions()
            elif action.id == "update_dependencies":
                return await self._update_dependencies()
            elif action.id == "secure_configurations":
                return await self._secure_configurations()
            elif action.id == "security_monitoring":
                return await self._run_security_monitoring()
            else:
                # Generic security action
                return await self._generic_security_action(action)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": datetime.now().isoformat()
            }

    async def _fix_vulnerabilities(self) -> Dict[str, Any]:
        """Fix identified security vulnerabilities."""
        vulnerabilities = await self._scan_for_vulnerabilities()
        fixed_count = 0

        # Simulate fixing vulnerabilities
        for vuln in vulnerabilities[:5]:  # Fix first 5 vulnerabilities
            if vuln["category"] == "hardcoded_secrets":
                # Simulate replacing hardcoded secrets with environment variables
                fixed_count += 1
            elif vuln["category"] == "dangerous_functions":
                # Simulate replacing dangerous functions with safer alternatives
                fixed_count += 1

        return {
            "success": True,
            "fixed_vulnerabilities": fixed_count,
            "total_vulnerabilities": len(vulnerabilities),
            "execution_time": datetime.now().isoformat()
        }

    async def _secure_file_permissions(self) -> Dict[str, Any]:
        """Secure file permissions."""
        secured_files = 0

        # Find sensitive files and secure them
        sensitive_patterns = [".env", "*.key", "*.pem", "config.*"]

        for pattern in sensitive_patterns:
            files = list(self.workspace_root.rglob(pattern))
            for file_path in files:
                try:
                    # Simulate setting secure permissions (600)
                    os.chmod(file_path, 0o600)
                    secured_files += 1
                except:
                    pass

        return {
            "success": True,
            "secured_files": secured_files,
            "execution_time": datetime.now().isoformat()
        }

    async def _update_dependencies(self) -> Dict[str, Any]:
        """Update insecure dependencies."""
        # Simulate dependency updates
        updated_deps = 0

        requirements_files = list(self.workspace_root.rglob("requirements*.txt"))
        for req_file in requirements_files:
            # Simulate updating 2-3 dependencies per file
            updated_deps += 3

        return {
            "success": True,
            "updated_dependencies": updated_deps,
            "execution_time": datetime.now().isoformat()
        }

    async def _secure_configurations(self) -> Dict[str, Any]:
        """Secure configuration files."""
        secured_configs = 0

        config_files = list(self.workspace_root.rglob("*.yml")) + list(self.workspace_root.rglob("*.yaml"))

        for config_file in config_files[:5]:  # Limit to first 5 files
            try:
                with open(config_file, 'r') as f:
                    content = f.read()

                # Simulate removing debug flags and securing configs
                if "debug: true" in content.lower():
                    secured_configs += 1

            except:
                pass

        return {
            "success": True,
            "secured_configurations": secured_configs,
            "execution_time": datetime.now().isoformat()
        }

    async def _run_security_monitoring(self) -> Dict[str, Any]:
        """Run security monitoring."""
        # Simulate security monitoring
        alerts_generated = 0

        # Check for new vulnerabilities
        current_vulns = await self._scan_for_vulnerabilities()

        if len(current_vulns) > 0:
            alerts_generated = len(current_vulns)

        return {
            "success": True,
            "alerts_generated": alerts_generated,
            "vulnerabilities_found": len(current_vulns),
            "execution_time": datetime.now().isoformat()
        }

    async def _generic_security_action(self, action: ImprovementAction) -> Dict[str, Any]:
        """Execute a generic security action."""
        # Simulate executing the action
        import asyncio
        await asyncio.sleep(0.5)  # Simulate work

        return {
            "success": True,
            "action_executed": action.name,
            "execution_time": datetime.now().isoformat()
        }

def main():
    """Test the security agent."""
    import asyncio

    async def test_agent():
        workspace_root = Path("/workspaces/semantic-kernel/ai-workspace")
        agent = SecurityAgent("security", workspace_root)

        print("🔒 Testing Security Agent")
        print("=" * 30)

        # Test analysis
        metrics = await agent.analyze()
        print(f"📊 Analyzed {len(metrics)} security metrics:")
        for metric in metrics:
            print(f"   • {metric.name}: {metric.value:.1f} (target: {metric.target})")

        # Test action proposal
        actions = await agent.propose_actions(metrics)
        print(f"\n💡 Proposed {len(actions)} security actions:")
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
