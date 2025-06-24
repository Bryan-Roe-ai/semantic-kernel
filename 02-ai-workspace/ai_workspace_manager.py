#!/usr/bin/env python3
"""
AI module for ai workspace manager

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class AIWorkspaceManager:
    def __init__(self, workspace_path="/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_path = Path(workspace_path)
        self.root_path = self.workspace_path.parent

    def get_workspace_status(self) -> Dict[str, Any]:
        """Get the current status of the AI workspace."""
        status = {
            "workspace_exists": self.workspace_path.exists(),
            "directories": {},
            "total_files": 0,
            "total_notebooks": 0,
            "environment_files": []
        }

        if not status["workspace_exists"]:
            return status

        for item in self.workspace_path.iterdir():
            if item.is_dir() and item.name.startswith(('01-', '02-', '03-', '04-', '05-', '06-', '07-', '08-', '09-', '10-')):
                dir_info = self._analyze_directory(item)
                status["directories"][item.name] = dir_info
                status["total_files"] += dir_info["file_count"]
                status["total_notebooks"] += dir_info["notebook_count"]

        # Find environment files
        env_patterns = [".env*", "*.config", "appsettings*", "requirements*.txt"]
        for pattern in env_patterns:
            status["environment_files"].extend(list(self.workspace_path.glob(f"**/{pattern}")))

        return status

    def _analyze_directory(self, directory: Path) -> Dict[str, Any]:
        """Analyze a directory and return information about its contents."""
        info = {
            "file_count": 0,
            "notebook_count": 0,
            "subdirectories": [],
            "key_files": []
        }

        try:
            for item in directory.rglob("*"):
                if item.is_file():
                    info["file_count"] += 1
                    if item.suffix == ".ipynb":
                        info["notebook_count"] += 1
                    if item.name in ["README.md", "requirements.txt", "setup.py", "main.py", "app.py"]:
                        info["key_files"].append(str(item.relative_to(directory)))
                elif item.is_dir() and item.parent == directory:
                    info["subdirectories"].append(item.name)
        except PermissionError:
            pass

        return info

    def create_dev_environment(self):
        """Create development environment setup files."""

        # Create main requirements.txt for AI development
        ai_requirements = """# AI Development Requirements
semantic-kernel>=1.0.0
openai>=1.0.0
azure-openai
azure-identity
azure-storage-blob
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
seaborn>=0.11.0
jupyter>=1.0.0
jupyterlab>=3.0.0
ipykernel>=6.0.0
requests>=2.25.0
python-dotenv>=0.19.0
pydantic>=2.0.0
fastapi>=0.68.0
uvicorn>=0.15.0
streamlit>=1.28.0
gradio>=3.0.0
transformers>=4.20.0
torch>=1.12.0
tensorflow>=2.9.0
huggingface-hub>=0.16.0
langchain>=0.1.0
chromadb>=0.4.0
pinecone-client>=2.2.0
redis>=4.3.0
pymongo>=4.0.0
asyncio
aiohttp>=3.8.0
websockets>=10.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
black>=22.0.0
flake8>=5.0.0
mypy>=0.991
pre-commit>=2.20.0"""

        with open(self.workspace_path / "requirements.txt", "w") as f:
            f.write(ai_requirements)

        # Create environment template
        env_template = """# AI Development Environment Variables

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_CHAT_MODEL_ID=gpt-4

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-01

# Hugging Face Configuration
HUGGINGFACE_API_KEY=your_huggingface_token_here

# Database Configuration
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://localhost:27017
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment

# Azure Configuration
AZURE_SUBSCRIPTION_ID=your_azure_subscription_id
AZURE_RESOURCE_GROUP=your_resource_group
AZURE_STORAGE_ACCOUNT=your_storage_account
AZURE_STORAGE_KEY=your_storage_key

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
ENVIRONMENT=development"""

        with open(self.workspace_path / ".env.template", "w") as f:
            f.write(env_template)

        # Create VS Code settings for AI development
        vscode_settings = {
            "python.defaultInterpreterPath": "./venv/bin/python",
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": False,
            "python.linting.flake8Enabled": True,
            "python.formatting.provider": "black",
            "python.testing.pytestEnabled": True,
            "jupyter.askForKernelRestart": False,
            "jupyter.interactiveWindow.creationMode": "perFile",
            "files.associations": {
                "*.ipynb": "jupyter-notebook"
            },
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": True
            }
        }

        vscode_dir = self.workspace_path / ".vscode"
        vscode_dir.mkdir(exist_ok=True)

        with open(vscode_dir / "settings.json", "w") as f:
            json.dump(vscode_settings, f, indent=2)

    def create_quick_start_notebook(self):
        """Create a quick start notebook for the AI workspace."""
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# AI Workspace Quick Start\n",
                        "\n",
                        "Welcome to your organized AI development workspace! This notebook will help you get started.\n",
                        "\n",
                        "## Environment Setup\n",
                        "\n",
                        "First, let's check that everything is properly configured."
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# Check Python environment and key packages\n",
                        "import sys\n",
                        "import os\n",
                        "from pathlib import Path\n",
                        "\n",
                        "print(f\"Python version: {sys.version}\")\n",
                        "print(f\"Current working directory: {os.getcwd()}\")\n",
                        "print(f\"Workspace path: {Path.cwd()}\")\n",
                        "\n",
                        "# Check for required packages\n",
                        "required_packages = ['semantic_kernel', 'openai', 'numpy', 'pandas', 'matplotlib']\n",
                        "for package in required_packages:\n",
                        "    try:\n",
                        "        __import__(package)\n",
                        "        print(f\"✅ {package} is available\")\n",
                        "    except ImportError:\n",
                        "        print(f\"❌ {package} is not installed\")"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Semantic Kernel Setup\n",
                        "\n",
                        "Let's initialize Semantic Kernel and test basic functionality."
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# Initialize Semantic Kernel\n",
                        "try:\n",
                        "    import semantic_kernel as sk\n",
                        "    from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion\n",
                        "    \n",
                        "    # Create kernel\n",
                        "    kernel = sk.Kernel()\n",
                        "    \n",
                        "    print(\"🚀 Semantic Kernel initialized successfully!\")\n",
                        "    print(f\"Kernel services: {len(kernel.services)}\")\n",
                        "    \n",
                        "except Exception as e:\n",
                        "    print(f\"❌ Error initializing Semantic Kernel: {e}\")\n",
                        "    print(\"Please check your installation and API keys.\")"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Workspace Navigation\n",
                        "\n",
                        "Explore the organized directory structure."
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# Display workspace structure\n",
                        "workspace_root = Path('..')\n",
                        "ai_workspace = Path('.')\n",
                        "\n",
                        "print(\"🏗️ AI Workspace Structure:\")\n",
                        "print(\"=\" * 40)\n",
                        "\n",
                        "for item in sorted(ai_workspace.glob('*')):\n",
                        "    if item.is_dir() and item.name.startswith(('01-', '02-', '03-', '04-', '05-', '06-', '07-', '08-', '09-', '10-')):\n",
                        "        print(f\"📁 {item.name}\")\n",
                        "        readme_path = item / 'README.md'\n",
                        "        if readme_path.exists():\n",
                        "            with open(readme_path, 'r') as f:\n",
                        "                lines = f.readlines()\n",
                        "                if len(lines) > 2:\n",
                        "                    description = lines[2].strip()\n",
                        "                    print(f\"   {description}\")\n",
                        "        print()"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Next Steps\n",
                        "\n",
                        "1. **Configure Environment**: Copy `.env.template` to `.env` and add your API keys\n",
                        "2. **Explore Notebooks**: Check out `01-notebooks/` for more examples\n",
                        "3. **Build Agents**: Start with examples in `02-agents/`\n",
                        "4. **Create Plugins**: Develop custom functionality in `04-plugins/`\n",
                        "5. **Deploy Services**: Use `06-backend-services/` for production applications\n",
                        "\n",
                        "Happy AI development! 🤖✨"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.10.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }

        notebook_path = self.workspace_path / "01-notebooks" / "quick-start.ipynb"
        with open(notebook_path, "w") as f:
            json.dump(notebook_content, f, indent=2)

    def setup_workspace(self):
        """Complete workspace setup process."""
        print("🔧 Setting up AI workspace...")

        self.create_dev_environment()
        print("✅ Development environment files created")

        self.create_quick_start_notebook()
        print("✅ Quick start notebook created")

        print("🎉 Workspace setup complete!")

    def status_report(self):
        """Generate and display workspace status report."""
        status = self.get_workspace_status()

        print("📊 AI Workspace Status Report")
        print("=" * 50)
        print(f"Workspace exists: {'✅' if status['workspace_exists'] else '❌'}")
        print(f"Total files: {status['total_files']}")
        print(f"Jupyter notebooks: {status['total_notebooks']}")
        print()

        if status['directories']:
            print("📁 Directory Structure:")
            for dir_name, info in status['directories'].items():
                print(f"  {dir_name}: {info['file_count']} files, {info['notebook_count']} notebooks")

        print()
        print("🔧 Environment files found:")
        for env_file in status['environment_files']:
            print(f"  {env_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Workspace Manager")
    parser.add_argument("--setup", action="store_true", help="Setup the workspace")
    parser.add_argument("--status", action="store_true", help="Show workspace status")

    args = parser.parse_args()

    manager = AIWorkspaceManager()

    if args.setup:
        manager.setup_workspace()
    elif args.status:
        manager.status_report()
    else:
        print("Use --setup to setup workspace or --status for status report")
