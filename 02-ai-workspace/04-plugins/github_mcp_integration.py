#!/usr/bin/env python3
"""
import re
Github Mcp Integration module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Check if Docker is available for GitHub MCP server
def check_docker_available() -> bool:
    """Check if Docker is available for running GitHub MCP server"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

class GitHubMCPIntegration:
    """GitHub MCP integration for AI workspace"""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        self.docker_available = check_docker_available()
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        """Initialize GitHub MCP integration"""
        if not self.github_token:
            self.logger.warning("GITHUB_PERSONAL_ACCESS_TOKEN not set. GitHub features limited.")

        if not self.docker_available:
            self.logger.warning("Docker not available. Using alternative GitHub integration.")

        self.logger.info("GitHub MCP Integration initialized")

    async def create_github_mcp_plugin(self) -> Dict[str, Any]:
        """Create a GitHub MCP plugin configuration"""
        if self.docker_available and self.github_token:
            # Use Docker-based GitHub MCP server
            return {
                "type": "stdio",
                "name": "github",
                "description": "GitHub Repository Integration via MCP",
                "command": "docker",
                "args": [
                    "run", "-i", "--rm",
                    "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
                    "ghcr.io/github/github-mcp-server"
                ],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": self.github_token
                }
            }
        else:
            # Use npm-based GitHub MCP server
            return {
                "type": "stdio",
                "name": "github",
                "description": "GitHub Repository Integration via MCP",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": self.github_token or ""
                }
            }

    async def analyze_workspace_repository(self) -> Dict[str, Any]:
        """Analyze the current workspace as a GitHub repository"""
        try:
            # Check if we're in a git repository (check both workspace and parent)
            git_dir = self.workspace_root / ".git"
            parent_git_dir = self.workspace_root.parent / ".git"

            if not git_dir.exists() and not parent_git_dir.exists():
                return {"error": "Not a git repository", "status": "error"}

            # Use the directory that contains .git
            repo_root = self.workspace_root if git_dir.exists() else self.workspace_root.parent

            # Get repository information
            repo_info = await self._get_git_info(repo_root)

            # Analyze workspace structure
            structure_analysis = await self._analyze_workspace_structure()

            # Check GitHub Actions
            actions_analysis = await self._analyze_github_actions(repo_root)

            return {
                "repository": repo_info,
                "structure": structure_analysis,
                "github_actions": actions_analysis,
                "status": "success"
            }

        except Exception as e:
            return {"error": str(e), "status": "error"}

    async def _get_git_info(self, repo_root: Optional[Path] = None) -> Dict[str, Any]:
        """Get git repository information"""
        if repo_root is None:
            repo_root = self.workspace_root

        try:
            # Get remote URL
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=repo_root,
                capture_output=True,
                text=True
            )

            remote_url = result.stdout.strip() if result.returncode == 0 else "unknown"

            # Get current branch
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo_root,
                capture_output=True,
                text=True
            )

            current_branch = result.stdout.strip() if result.returncode == 0 else "unknown"

            # Get latest commit
            result = subprocess.run(
                ["git", "log", "-1", "--format=%H|%s|%an|%ad"],
                cwd=repo_root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                commit_parts = result.stdout.strip().split("|")
                latest_commit = {
                    "hash": commit_parts[0] if len(commit_parts) > 0 else "",
                    "message": commit_parts[1] if len(commit_parts) > 1 else "",
                    "author": commit_parts[2] if len(commit_parts) > 2 else "",
                    "date": commit_parts[3] if len(commit_parts) > 3 else ""
                }
            else:
                latest_commit = {}

            return {
                "remote_url": remote_url,
                "current_branch": current_branch,
                "latest_commit": latest_commit
            }

        except Exception as e:
            return {"error": str(e)}

    async def _analyze_workspace_structure(self) -> Dict[str, Any]:
        """Analyze the AI workspace structure"""
        structure = {
            "directories": {},
            "key_files": {},
            "total_files": 0,
            "total_size": 0
        }

        # Expected directories
        expected_dirs = [
            "01-notebooks", "02-agents", "03-models-training", "04-plugins",
            "05-samples-demos", "06-backend-services", "07-data-resources",
            "08-documentation", "09-deployment", "10-config", "scripts"
        ]

        for dir_name in expected_dirs:
            dir_path = self.workspace_root / dir_name
            if dir_path.exists():
                file_count = len(list(dir_path.rglob("*")))
                dir_size = sum(f.stat().st_size for f in dir_path.rglob("*") if f.is_file())
                structure["directories"][dir_name] = {
                    "exists": True,
                    "file_count": file_count,
                    "size": dir_size
                }
                structure["total_files"] += file_count
                structure["total_size"] += dir_size
            else:
                structure["directories"][dir_name] = {"exists": False}

        # Key files
        key_files = [
            "README.md", "Dockerfile", "docker-compose.yml",
            "requirements.txt", "requirements-minimal.txt"
        ]

        for file_name in key_files:
            file_path = self.workspace_root / file_name
            structure["key_files"][file_name] = {
                "exists": file_path.exists(),
                "size": file_path.stat().st_size if file_path.exists() else 0
            }

        return structure

    async def _analyze_github_actions(self, repo_root: Optional[Path] = None) -> Dict[str, Any]:
        """Analyze GitHub Actions configuration"""
        if repo_root is None:
            repo_root = self.workspace_root

        actions_dir = repo_root / ".github" / "workflows"

        if not actions_dir.exists():
            return {"configured": False, "workflows": []}

        workflows = []
        for workflow_file in actions_dir.glob("*.yml"):
            try:
                content = workflow_file.read_text()
                workflows.append({
                    "name": workflow_file.name,
                    "size": len(content),
                    "triggers": self._extract_workflow_triggers(content)
                })
            except Exception as e:
                workflows.append({
                    "name": workflow_file.name,
                    "error": str(e)
                })

        return {
            "configured": True,
            "workflow_count": len(workflows),
            "workflows": workflows
        }

    def _extract_workflow_triggers(self, content: str) -> List[str]:
        """Extract workflow triggers from YAML content"""
        triggers = []
        lines = content.split("\n")

        in_on_section = False
        for line in lines:
            line = line.strip()
            if line.startswith("on:"):
                in_on_section = True
                continue
            elif in_on_section:
                if line.startswith("-") or line.startswith("push") or line.startswith("pull_request"):
                    triggers.append(line.lstrip("- ").split(":")[0])
                elif line and not line.startswith(" ") and not line.startswith("-"):
                    break

        return triggers

    async def create_workspace_issue_template(self) -> Dict[str, Any]:
        """Create GitHub issue templates for the AI workspace"""
        templates = {
            "bug_report": {
                "name": "Bug Report",
                "about": "Create a report to help us improve the AI workspace",
                "labels": ["bug", "ai-workspace"],
                "body": """
**Describe the bug**
A clear and concise description of what the bug is.

**Component**
Which AI workspace component is affected?
- [ ] Model Training
- [ ] Backend API
- [ ] Web Interface
- [ ] Docker Setup
- [ ] GitHub Actions
- [ ] Documentation

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment**
- OS: [e.g. Ubuntu 20.04]
- Docker version: [e.g. 20.10.7]
- Python version: [e.g. 3.11]
- Browser [e.g. chrome, safari]

**Additional context**
Add any other context about the problem here.
"""
            },
            "feature_request": {
                "name": "Feature Request",
                "about": "Suggest an idea for the AI workspace",
                "labels": ["enhancement", "ai-workspace"],
                "body": """
**Is your feature request related to a problem?**
A clear and concise description of what the problem is.

**Component**
Which AI workspace component would this enhance?
- [ ] Model Training
- [ ] Backend API
- [ ] Web Interface
- [ ] Docker Setup
- [ ] GitHub Actions
- [ ] Documentation
- [ ] New Component

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
"""
            },
            "model_training": {
                "name": "Model Training Issue",
                "about": "Report issues with model training or request new training features",
                "labels": ["model-training", "ai-workspace"],
                "body": """
**Training Issue Type**
- [ ] Training fails to start
- [ ] Training crashes during execution
- [ ] Poor training results
- [ ] Performance issues
- [ ] Feature request

**Model Details**
- Model type: [e.g. GPT, BERT, Custom]
- Dataset size: [e.g. 1000 samples]
- Training method: [e.g. LoRA, Full fine-tuning]

**Configuration**
```json
{
  "learning_rate": "",
  "batch_size": "",
  "epochs": "",
  "other_params": ""
}
```

**Error Message (if applicable)**
```
Paste error message here
```

**Expected Outcome**
Describe what you expected to happen with the training.

**Additional Context**
Add any other context about the training issue.
"""
            }
        }

        return {
            "templates": templates,
            "status": "success",
            "count": len(templates)
        }

    async def suggest_repository_improvements(self) -> Dict[str, Any]:
        """Suggest improvements for the GitHub repository"""
        analysis = await self.analyze_workspace_repository()

        suggestions = []

        # Check repository basics
        if analysis.get("repository", {}).get("remote_url") == "unknown":
            suggestions.append({
                "category": "repository",
                "priority": "high",
                "suggestion": "Set up GitHub remote repository",
                "description": "Connect this workspace to a GitHub repository for version control and collaboration"
            })

        # Check GitHub Actions
        if not analysis.get("github_actions", {}).get("configured", False):
            suggestions.append({
                "category": "ci_cd",
                "priority": "high",
                "suggestion": "Set up GitHub Actions workflows",
                "description": "Configure automated testing and deployment with GitHub Actions"
            })

        # Check documentation
        structure = analysis.get("structure", {})
        readme_exists = structure.get("key_files", {}).get("README.md", {}).get("exists", False)

        if not readme_exists:
            suggestions.append({
                "category": "documentation",
                "priority": "medium",
                "suggestion": "Add comprehensive README",
                "description": "Create a detailed README.md with setup instructions and usage examples"
            })

        # Check workspace completeness
        directories = structure.get("directories", {})
        missing_dirs = [name for name, info in directories.items() if not info.get("exists", False)]

        if missing_dirs:
            suggestions.append({
                "category": "structure",
                "priority": "medium",
                "suggestion": f"Complete workspace structure",
                "description": f"Add missing directories: {', '.join(missing_dirs)}"
            })

        return {
            "suggestions": suggestions,
            "total_suggestions": len(suggestions),
            "status": "success"
        }


async def main():
    """Main entry point for GitHub MCP integration"""
    workspace_root = Path(__file__).parent.parent

    # Initialize GitHub MCP integration
    github_mcp = GitHubMCPIntegration(workspace_root)
    await github_mcp.initialize()

    # Analyze workspace
    print("🔍 Analyzing AI Workspace GitHub Repository...")
    analysis = await github_mcp.analyze_workspace_repository()
    print(json.dumps(analysis, indent=2))

    print("\n💡 Generating improvement suggestions...")
    suggestions = await github_mcp.suggest_repository_improvements()
    print(json.dumps(suggestions, indent=2))

    print("\n📋 Creating issue templates...")
    templates = await github_mcp.create_workspace_issue_template()
    print(f"Created {templates['count']} issue templates")

    print("\n⚙️ MCP Plugin Configuration:")
    plugin_config = await github_mcp.create_github_mcp_plugin()
    print(json.dumps(plugin_config, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
