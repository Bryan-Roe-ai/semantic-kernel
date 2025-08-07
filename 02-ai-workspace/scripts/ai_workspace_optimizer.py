#!/usr/bin/env python3
"""
import re
AI module for ai workspace optimizer

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import sys
import json
import time
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIWorkspaceOptimizer:
    def __init__(self, workspace_root="/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_root = Path(workspace_root)
        self.backup_dir = self.workspace_root / "backups"
        self.logs_dir = self.workspace_root / "logs"
        self.cache_dir = self.workspace_root / "cache"

    def optimize_workspace(self):
        """Run comprehensive workspace optimization."""
        print("🚀 AI Workspace Optimizer Starting...")
        print("=" * 60)

        tasks = [
            ("🧹 Cleaning temporary files", self.cleanup_temp_files),
            ("📊 Analyzing disk usage", self.analyze_disk_usage),
            ("🔄 Optimizing cache", self.optimize_cache),
            ("📦 Organizing models", self.organize_models),
            ("📝 Generating reports", self.generate_reports),
            ("🔧 Updating configurations", self.update_configs),
            ("🔍 Running health checks", self.health_check),
        ]

        results = {}
        for task_name, task_func in tasks:
            print(f"\n{task_name}...")
            try:
                result = task_func()
                results[task_name] = {"status": "success", "result": result}
                print(f"✅ {task_name} completed")
            except Exception as e:
                results[task_name] = {"status": "error", "error": str(e)}
                print(f"❌ {task_name} failed: {e}")

        self.save_optimization_report(results)
        print(f"\n🎉 Optimization complete! Report saved to {self.logs_dir}/optimization_report.json")

    def cleanup_temp_files(self):
        """Clean up temporary files and optimize disk space."""
        cleaned_size = 0
        patterns = [
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pyo",
            "**/.pytest_cache",
            "**/node_modules",
            "**/.DS_Store",
            "**/Thumbs.db",
            "**/*.tmp",
            "**/*.temp"
        ]

        for pattern in patterns:
            for path in self.workspace_root.rglob(pattern):
                if path.exists():
                    size = self._get_size(path)
                    if path.is_dir():
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        path.unlink()
                    cleaned_size += size

        return f"Cleaned {cleaned_size / (1024*1024):.2f} MB"

    def analyze_disk_usage(self):
        """Analyze disk usage by directory."""
        usage = {}
        for item in self.workspace_root.iterdir():
            if item.is_dir():
                size = self._get_size(item)
                usage[item.name] = size

        # Sort by size
        sorted_usage = sorted(usage.items(), key=lambda x: x[1], reverse=True)
        return {name: f"{size/(1024*1024):.2f} MB" for name, size in sorted_usage[:10]}

    def optimize_cache(self):
        """Optimize cache directories."""
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True)

        # Clear old cache files (>7 days)
        cutoff = time.time() - (7 * 24 * 60 * 60)
        cleared = 0

        for cache_file in self.cache_dir.rglob("*"):
            if cache_file.is_file() and cache_file.stat().st_mtime < cutoff:
                cache_file.unlink()
                cleared += 1

        return f"Cleared {cleared} old cache files"

    def organize_models(self):
        """Organize model files and create index."""
        models_dir = self.workspace_root / "models"
        if not models_dir.exists():
            models_dir.mkdir(parents=True)

        model_index = {
            "last_updated": datetime.now().isoformat(),
            "models": []
        }

        for model_file in models_dir.rglob("*.bin"):
            model_info = {
                "name": model_file.stem,
                "path": str(model_file.relative_to(self.workspace_root)),
                "size": model_file.stat().st_size,
                "modified": datetime.fromtimestamp(model_file.stat().st_mtime).isoformat()
            }
            model_index["models"].append(model_info)

        # Save model index
        index_file = models_dir / "model_index.json"
        with open(index_file, 'w') as f:
            json.dump(model_index, f, indent=2)

        return f"Indexed {len(model_index['models'])} models"

    def generate_reports(self):
        """Generate workspace reports."""
        reports_dir = self.workspace_root / "08-documentation" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Generate structure report
        structure_report = self._generate_structure_report()
        with open(reports_dir / "workspace_structure.md", 'w') as f:
            f.write(structure_report)

        # Generate metrics report
        metrics = self._collect_metrics()
        with open(reports_dir / "metrics.json", 'w') as f:
            json.dump(metrics, f, indent=2)

        return "Generated structure and metrics reports"

    def update_configs(self):
        """Update configuration files with optimized settings."""
        config_updates = 0

        # Update .env if it exists
        env_file = self.workspace_root / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()

            # Add performance optimizations if not present
            optimizations = [
                "PYTHONDONTWRITEBYTECODE=1",
                "PYTHONUNBUFFERED=1",
                "TOKENIZERS_PARALLELISM=false"
            ]

            for opt in optimizations:
                if opt.split('=')[0] not in content:
                    content += f"\n{opt}"
                    config_updates += 1

            with open(env_file, 'w') as f:
                f.write(content)

        return f"Applied {config_updates} configuration updates"

    def health_check(self):
        """Run comprehensive health check."""
        checks = {
            "python_version": sys.version_info[:2],
            "workspace_readable": os.access(self.workspace_root, os.R_OK),
            "workspace_writable": os.access(self.workspace_root, os.W_OK),
            "required_dirs": [],
            "key_files": []
        }

        # Check required directories
        required_dirs = [
            "01-notebooks", "02-agents", "03-models-training",
            "04-plugins", "05-samples-demos", "06-backend-services"
        ]

        for dir_name in required_dirs:
            exists = (self.workspace_root / dir_name).exists()
            checks["required_dirs"].append({"name": dir_name, "exists": exists})

        # Check key files
        key_files = [
            "docker-compose.yml", "Dockerfile", "requirements.txt",
            "06-backend-services/simple_api_server.py",
            "03-models-training/advanced_llm_trainer.py"
        ]

        for file_path in key_files:
            exists = (self.workspace_root / file_path).exists()
            checks["key_files"].append({"name": file_path, "exists": exists})

        return checks

    def _get_size(self, path):
        """Get size of file or directory in bytes."""
        if path.is_file():
            return path.stat().st_size
        elif path.is_dir():
            return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        return 0

    def _generate_structure_report(self):
        """Generate markdown report of workspace structure."""
        report = ["# AI Workspace Structure Report", ""]
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        def add_tree(path, prefix="", max_depth=3, current_depth=0):
            if current_depth >= max_depth:
                return

            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                report.append(f"{prefix}{current_prefix}{item.name}")

                if item.is_dir() and current_depth < max_depth - 1:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    add_tree(item, next_prefix, max_depth, current_depth + 1)

        report.append("## Directory Structure")
        report.append("```")
        add_tree(self.workspace_root)
        report.append("```")

        return "\n".join(report)

    def _collect_metrics(self):
        """Collect workspace metrics."""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "total_dirs": 0,
            "total_size": 0,
            "file_types": {},
            "language_stats": {}
        }

        for item in self.workspace_root.rglob("*"):
            if item.is_file():
                metrics["total_files"] += 1
                metrics["total_size"] += item.stat().st_size

                # Count file types
                suffix = item.suffix.lower() or "no_extension"
                metrics["file_types"][suffix] = metrics["file_types"].get(suffix, 0) + 1

                # Language statistics
                lang_map = {
                    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
                    ".html": "HTML", ".css": "CSS", ".md": "Markdown",
                    ".json": "JSON", ".yml": "YAML", ".yaml": "YAML"
                }
                if suffix in lang_map:
                    lang = lang_map[suffix]
                    metrics["language_stats"][lang] = metrics["language_stats"].get(lang, 0) + 1

            elif item.is_dir():
                metrics["total_dirs"] += 1

        return metrics

    def save_optimization_report(self, results):
        """Save optimization report."""
        self.logs_dir.mkdir(exist_ok=True)

        report = {
            "timestamp": datetime.now().isoformat(),
            "workspace": str(self.workspace_root),
            "results": results,
            "summary": {
                "total_tasks": len(results),
                "successful": len([r for r in results.values() if r["status"] == "success"]),
                "failed": len([r for r in results.values() if r["status"] == "error"])
            }
        }

        with open(self.logs_dir / "optimization_report.json", 'w') as f:
            json.dump(report, f, indent=2)

def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="AI Workspace Optimizer")
    parser.add_argument("--workspace", default="/workspaces/semantic-kernel/ai-workspace",
                       help="Workspace root directory")
    parser.add_argument("--quick", action="store_true",
                       help="Run quick optimization only")

    args = parser.parse_args()

    optimizer = AIWorkspaceOptimizer(args.workspace)

    if args.quick:
        print("🚀 Running quick optimization...")
        optimizer.cleanup_temp_files()
        optimizer.health_check()
        print("✅ Quick optimization complete!")
    else:
        optimizer.optimize_workspace()

if __name__ == "__main__":
    main()
