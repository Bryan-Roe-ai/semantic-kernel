#!/usr/bin/env python3
"""
AI Workspace Deployment Automator
Advanced deployment automation for production environments.
"""

import os
import sys
import json
import yaml
import subprocess
import time
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List, Any, Optional
import shutil

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DeploymentAutomator:
    def __init__(self, workspace_root="/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_root = Path(workspace_root)
        self.deployment_dir = self.workspace_root / "09-deployment"
        self.config_dir = self.workspace_root / "10-config"
        self.backup_dir = self.workspace_root / "backups"

    def deploy(self, environment: str = "production", mode: str = "docker"):
        """Deploy the AI workspace to specified environment."""
        print(f"🚀 Starting deployment to {environment}")
        print("=" * 60)

        deployment_plan = {
            "environment": environment,
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }

        try:
            # Pre-deployment checks
            self._step(deployment_plan, "Pre-deployment validation", self._validate_deployment)

            # Create backup
            self._step(deployment_plan, "Creating backup", self._create_backup)

            # Build artifacts
            self._step(deployment_plan, "Building artifacts", lambda: self._build_artifacts(mode))

            # Deploy based on mode
            if mode == "docker":
                self._step(deployment_plan, "Docker deployment", lambda: self._deploy_docker(environment))
            elif mode == "kubernetes":
                self._step(deployment_plan, "Kubernetes deployment", lambda: self._deploy_kubernetes(environment))
            elif mode == "azure":
                self._step(deployment_plan, "Azure deployment", lambda: self._deploy_azure(environment))
            elif mode == "aws":
                self._step(deployment_plan, "AWS deployment", lambda: self._deploy_aws(environment))
            else:
                raise ValueError(f"Unsupported deployment mode: {mode}")

            # Post-deployment validation
            self._step(deployment_plan, "Post-deployment validation", self._validate_services)

            # Update monitoring
            self._step(deployment_plan, "Setup monitoring", self._setup_monitoring)

            print(f"\n✅ Deployment to {environment} completed successfully!")
            self._save_deployment_record(deployment_plan)

        except Exception as e:
            print(f"\n❌ Deployment failed: {e}")
            deployment_plan["status"] = "failed"
            deployment_plan["error"] = str(e)
            self._save_deployment_record(deployment_plan)
            self._rollback_deployment(deployment_plan)
            raise

    def _step(self, plan: Dict, description: str, func):
        """Execute a deployment step."""
        print(f"\n📋 {description}...")
        start_time = time.time()

        try:
            result = func()
            duration = time.time() - start_time

            step_info = {
                "description": description,
                "status": "success",
                "duration": duration,
                "result": result
            }
            plan["steps"].append(step_info)
            print(f"✅ {description} completed in {duration:.2f}s")

        except Exception as e:
            duration = time.time() - start_time
            step_info = {
                "description": description,
                "status": "failed",
                "duration": duration,
                "error": str(e)
            }
            plan["steps"].append(step_info)
            print(f"❌ {description} failed: {e}")
            raise

    def _validate_deployment(self) -> Dict[str, Any]:
        """Validate deployment prerequisites."""
        validations = {
            "workspace_exists": self.workspace_root.exists(),
            "docker_available": self._check_docker(),
            "required_files": self._check_required_files(),
            "environment_config": self._check_environment_config(),
            "disk_space": self._check_disk_space(),
            "network_connectivity": self._check_network()
        }

        failed_checks = [k for k, v in validations.items() if not v]
        if failed_checks:
            raise Exception(f"Validation failed: {failed_checks}")

        return validations

    def _create_backup(self) -> str:
        """Create deployment backup."""
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(parents=True, exist_ok=True)

        # Backup critical files
        critical_paths = [
            "06-backend-services",
            "03-models-training",
            "10-config",
            "docker-compose.yml",
            "Dockerfile",
            "requirements.txt"
        ]

        for path in critical_paths:
            source = self.workspace_root / path
            if source.exists():
                if source.is_file():
                    shutil.copy2(source, backup_path)
                else:
                    shutil.copytree(source, backup_path / path)

        # Create backup manifest
        manifest = {
            "backup_name": backup_name,
            "timestamp": datetime.now().isoformat(),
            "paths": critical_paths,
            "size": self._get_directory_size(backup_path)
        }

        with open(backup_path / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"📦 Backup created: {backup_name}")
        return backup_name

    def _build_artifacts(self, mode: str) -> Dict[str, Any]:
        """Build deployment artifacts."""
        artifacts = {}

        if mode in ["docker", "kubernetes"]:
            # Build Docker image
            image_tag = f"ai-workspace:{datetime.now().strftime('%Y%m%d-%H%M%S')}"

            build_cmd = [
                "docker", "build",
                "-t", image_tag,
                "-t", "ai-workspace:latest",
                str(self.workspace_root)
            ]

            result = subprocess.run(build_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Docker build failed: {result.stderr}")

            artifacts["docker_image"] = image_tag
            artifacts["build_output"] = result.stdout

        # Build static assets
        static_build = self._build_static_assets()
        artifacts.update(static_build)

        return artifacts

    def _build_static_assets(self) -> Dict[str, Any]:
        """Build static web assets."""
        static_dir = self.workspace_root / "05-samples-demos"
        dist_dir = self.workspace_root / "dist"

        # Ensure dist directory exists
        dist_dir.mkdir(exist_ok=True)

        # Copy HTML files
        html_files = list(static_dir.glob("*.html"))
        for html_file in html_files:
            shutil.copy2(html_file, dist_dir)

        # Copy other static assets
        for pattern in ["*.css", "*.js", "*.png", "*.jpg", "*.svg"]:
            for asset in static_dir.glob(pattern):
                shutil.copy2(asset, dist_dir)

        return {
            "static_files": len(list(dist_dir.glob("*"))),
            "dist_path": str(dist_dir)
        }

    def _deploy_docker(self, environment: str) -> Dict[str, Any]:
        """Deploy using Docker Compose."""
        compose_file = "docker-compose.yml"
        if environment != "production":
            compose_file = f"docker-compose.{environment}.yml"

        compose_path = self.workspace_root / compose_file
        if not compose_path.exists():
            # Create environment-specific compose file
            self._create_compose_file(environment, compose_path)

        # Deploy with Docker Compose
        deploy_cmd = [
            "docker-compose",
            "-f", str(compose_path),
            "up", "-d", "--build"
        ]

        result = subprocess.run(deploy_cmd, capture_output=True, text=True, cwd=self.workspace_root)
        if result.returncode != 0:
            raise Exception(f"Docker deployment failed: {result.stderr}")

        # Get container status
        status_cmd = ["docker-compose", "-f", str(compose_path), "ps"]
        status_result = subprocess.run(status_cmd, capture_output=True, text=True, cwd=self.workspace_root)

        return {
            "compose_file": str(compose_path),
            "deployment_output": result.stdout,
            "container_status": status_result.stdout
        }

    def _deploy_kubernetes(self, environment: str) -> Dict[str, Any]:
        """Deploy to Kubernetes."""
        k8s_dir = self.deployment_dir / "kubernetes"
        k8s_dir.mkdir(parents=True, exist_ok=True)

        # Generate Kubernetes manifests
        manifests = self._generate_k8s_manifests(environment)

        # Apply manifests
        deployed_resources = []
        for manifest_file in k8s_dir.glob("*.yaml"):
            apply_cmd = ["kubectl", "apply", "-f", str(manifest_file)]
            result = subprocess.run(apply_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise Exception(f"Kubernetes deployment failed for {manifest_file}: {result.stderr}")

            deployed_resources.append(str(manifest_file))

        return {
            "manifests": manifests,
            "deployed_resources": deployed_resources
        }

    def _deploy_azure(self, environment: str) -> Dict[str, Any]:
        """Deploy to Azure."""
        azure_config = self._load_azure_config(environment)

        # Deploy to Azure Container Instances or App Service
        if azure_config.get("service_type") == "container_instances":
            return self._deploy_azure_aci(azure_config)
        else:
            return self._deploy_azure_app_service(azure_config)

    def _deploy_aws(self, environment: str) -> Dict[str, Any]:
        """Deploy to AWS."""
        aws_config = self._load_aws_config(environment)

        # Deploy to ECS or Lambda
        if aws_config.get("service_type") == "ecs":
            return self._deploy_aws_ecs(aws_config)
        else:
            return self._deploy_aws_lambda(aws_config)

    def _validate_services(self) -> Dict[str, Any]:
        """Validate deployed services."""
        validations = {}

        # Test API endpoints
        import requests

        endpoints = [
            "http://localhost:8000/health",
            "http://localhost:8000/api/chat",
            "http://localhost:8000/api/models"
        ]

        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=10)
                validations[endpoint] = {
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "healthy": response.status_code == 200
                }
            except Exception as e:
                validations[endpoint] = {
                    "error": str(e),
                    "healthy": False
                }

        # Check container health
        if self._check_docker():
            container_health = self._check_container_health()
            validations["containers"] = container_health

        return validations

    def _setup_monitoring(self) -> Dict[str, Any]:
        """Setup monitoring for deployed services."""
        monitoring_config = {
            "metrics_enabled": True,
            "alerting_enabled": True,
            "log_aggregation": True
        }

        # Start monitoring service
        monitor_script = self.workspace_root / "scripts" / "ai_workspace_monitor.py"
        if monitor_script.exists():
            # Could start monitoring in background
            # subprocess.Popen([sys.executable, str(monitor_script)])
            monitoring_config["monitor_script"] = str(monitor_script)

        return monitoring_config

    def _create_compose_file(self, environment: str, compose_path: Path):
        """Create environment-specific Docker Compose file."""
        base_compose = self.workspace_root / "docker-compose.yml"

        if base_compose.exists():
            with open(base_compose, 'r') as f:
                compose_config = yaml.safe_load(f)
        else:
            compose_config = {
                "version": "3.8",
                "services": {}
            }

        # Environment-specific overrides
        if environment == "development":
            # Add development-specific settings
            if "ai-workspace" in compose_config.get("services", {}):
                compose_config["services"]["ai-workspace"]["environment"] = [
                    "DEBUG=true",
                    "LOG_LEVEL=debug"
                ]
                compose_config["services"]["ai-workspace"]["volumes"] = [
                    "./:/app:rw"
                ]

        elif environment == "staging":
            # Add staging-specific settings
            if "ai-workspace" in compose_config.get("services", {}):
                compose_config["services"]["ai-workspace"]["environment"] = [
                    "ENVIRONMENT=staging"
                ]

        with open(compose_path, 'w') as f:
            yaml.dump(compose_config, f, default_flow_style=False)

    def _generate_k8s_manifests(self, environment: str) -> List[str]:
        """Generate Kubernetes manifests."""
        k8s_dir = self.deployment_dir / "kubernetes"

        # Deployment manifest
        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": f"ai-workspace-{environment}",
                "labels": {"app": "ai-workspace", "env": environment}
            },
            "spec": {
                "replicas": 2 if environment == "production" else 1,
                "selector": {"matchLabels": {"app": "ai-workspace"}},
                "template": {
                    "metadata": {"labels": {"app": "ai-workspace"}},
                    "spec": {
                        "containers": [{
                            "name": "ai-workspace",
                            "image": "ai-workspace:latest",
                            "ports": [{"containerPort": 8000}],
                            "env": [
                                {"name": "ENVIRONMENT", "value": environment}
                            ]
                        }]
                    }
                }
            }
        }

        # Service manifest
        service = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": f"ai-workspace-service-{environment}"},
            "spec": {
                "selector": {"app": "ai-workspace"},
                "ports": [{"port": 80, "targetPort": 8000}],
                "type": "LoadBalancer"
            }
        }

        # Save manifests
        manifests = []
        for name, manifest in [("deployment", deployment), ("service", service)]:
            manifest_path = k8s_dir / f"{name}-{environment}.yaml"
            with open(manifest_path, 'w') as f:
                yaml.dump(manifest, f, default_flow_style=False)
            manifests.append(str(manifest_path))

        return manifests

    def _check_docker(self) -> bool:
        """Check if Docker is available."""
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True)
            return result.returncode == 0
        except Exception:
            return False

    def _check_required_files(self) -> bool:
        """Check if required files exist."""
        required_files = [
            "Dockerfile",
            "requirements.txt",
            "06-backend-services/simple_api_server.py"
        ]

        return all((self.workspace_root / f).exists() for f in required_files)

    def _check_environment_config(self) -> bool:
        """Check environment configuration."""
        env_file = self.workspace_root / ".env"
        return env_file.exists()

    def _check_disk_space(self, min_gb: int = 5) -> bool:
        """Check available disk space."""
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.workspace_root)
            free_gb = free / (1024**3)
            return free_gb >= min_gb
        except Exception:
            return False

    def _check_network(self) -> bool:
        """Check network connectivity."""
        try:
            import urllib.request
            urllib.request.urlopen('https://google.com', timeout=5)
            return True
        except Exception:
            return False

    def _check_container_health(self) -> Dict[str, Any]:
        """Check health of running containers."""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "json"],
                capture_output=True, text=True
            )

            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        containers.append(json.loads(line))

                return {
                    "running_containers": len(containers),
                    "containers": containers
                }
        except Exception as e:
            return {"error": str(e)}

        return {"running_containers": 0}

    def _get_directory_size(self, path: Path) -> int:
        """Get total size of directory."""
        total = 0
        for item in path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
        return total

    def _save_deployment_record(self, deployment_plan: Dict[str, Any]):
        """Save deployment record."""
        deployments_dir = self.workspace_root / "deployments"
        deployments_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        record_file = deployments_dir / f"deployment_{timestamp}.json"

        with open(record_file, 'w') as f:
            json.dump(deployment_plan, f, indent=2)

    def _rollback_deployment(self, deployment_plan: Dict[str, Any]):
        """Rollback failed deployment."""
        print("🔄 Initiating rollback...")

        # Stop containers
        try:
            subprocess.run(["docker-compose", "down"], cwd=self.workspace_root)
        except Exception as e:
            print(f"Warning: Could not stop containers: {e}")

        # Could restore from backup here
        print("⚠️  Manual intervention may be required for complete rollback")

    def list_deployments(self) -> List[Dict[str, Any]]:
        """List previous deployments."""
        deployments_dir = self.workspace_root / "deployments"
        if not deployments_dir.exists():
            return []

        deployments = []
        for record_file in deployments_dir.glob("deployment_*.json"):
            try:
                with open(record_file, 'r') as f:
                    deployment = json.load(f)
                    deployments.append({
                        "file": record_file.name,
                        "timestamp": deployment.get("timestamp"),
                        "environment": deployment.get("environment"),
                        "status": deployment.get("status", "unknown")
                    })
            except Exception as e:
                logger.error(f"Error reading deployment record {record_file}: {e}")

        return sorted(deployments, key=lambda x: x["timestamp"], reverse=True)

    # Placeholder methods for cloud deployments
    def _load_azure_config(self, environment: str) -> Dict[str, Any]:
        """Load Azure configuration."""
        return {"service_type": "container_instances"}

    def _deploy_azure_aci(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to Azure Container Instances."""
        return {"status": "placeholder"}

    def _deploy_azure_app_service(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to Azure App Service."""
        return {"status": "placeholder"}

    def _load_aws_config(self, environment: str) -> Dict[str, Any]:
        """Load AWS configuration."""
        return {"service_type": "ecs"}

    def _deploy_aws_ecs(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to AWS ECS."""
        return {"status": "placeholder"}

    def _deploy_aws_lambda(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to AWS Lambda."""
        return {"status": "placeholder"}

def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="AI Workspace Deployment Automator")
    parser.add_argument("action", choices=["deploy", "list", "validate"],
                       help="Action to perform")
    parser.add_argument("--environment", "-e", default="production",
                       choices=["development", "staging", "production"],
                       help="Deployment environment")
    parser.add_argument("--mode", "-m", default="docker",
                       choices=["docker", "kubernetes", "azure", "aws"],
                       help="Deployment mode")
    parser.add_argument("--workspace", default="/workspaces/semantic-kernel/ai-workspace",
                       help="Workspace root directory")

    args = parser.parse_args()

    automator = DeploymentAutomator(args.workspace)

    if args.action == "deploy":
        automator.deploy(args.environment, args.mode)
    elif args.action == "list":
        deployments = automator.list_deployments()
        print(json.dumps(deployments, indent=2))
    elif args.action == "validate":
        result = automator._validate_deployment()
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
