#!/usr/bin/env python3
"""
Organize Files module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import shutil
import json
from pathlib import Path

class AIWorkspaceOrganizer:
    def __init__(self, root_path="/workspaces/semantic-kernel"):
        self.root_path = Path(root_path)
        self.ai_workspace = self.root_path / "ai-workspace"

        # Define organization mapping
        self.organization_map = {
            "01-notebooks": {
                "patterns": ["*.ipynb", "*.ipynb?*"],
                "directories": ["notebooks"],
                "description": "Jupyter notebooks for AI experimentation and development"
            },
            "02-agents": {
                "patterns": ["*agent*", "*Agent*"],
                "directories": ["AgentDocs", "aipmakerday"],
                "files": ["ai-chat-launcher.hta"],
                "description": "AI agents, agent frameworks, and collaboration tools"
            },
            "03-models-training": {
                "patterns": ["*train*", "*finetune*", "*gpt*", "*llm*"],
                "files": ["collect_llm_training_data.py", "finetune_gpt2_custom.py", "simple_llm_demo.py"],
                "description": "Model training, fine-tuning, and LLM development"
            },
            "04-plugins": {
                "directories": ["plugins", "prompt_template_samples"],
                "patterns": ["*plugin*", "*Plugin*"],
                "description": "Semantic Kernel plugins and extensions"
            },
            "05-samples-demos": {
                "directories": ["samples"],
                "files": ["express-rate.js", "server.js"],
                "description": "Sample applications and demonstrations"
            },
            "06-backend-services": {
                "directories": ["AzureFunctions"],
                "files": [
                    "backend.py", "backend-starter.py", "backend_starter_server.py",
                    "start_backend.py", "start_chat_unified.py", "app.py"
                ],
                "description": "Backend services, APIs, and cloud functions"
            },
            "07-data-resources": {
                "directories": ["data", "devdata", "resources", "uploads", "results"],
                "patterns": ["*.xml", "*.json", "data*"],
                "files": ["index.xml", "output.xml"],
                "description": "Data files, resources, and training datasets"
            },
            "08-documentation": {
                "directories": ["docs"],
                "patterns": ["*.txt", "*.md", "README*", "Documentation*"],
                "files": ["BR-AI.txt", "Documentation 1.txt", "Documentation 2.txt", "Documentation 3.txt"],
                "description": "Documentation, guides, and reference materials"
            },
            "09-deployment": {
                "patterns": ["Dockerfile*", "docker*", "*.sh", "entrypoint*"],
                "files": ["Dockerfile", "dotnet-install.sh.1", "dotnet-install.sh.2", "entrypoint.sh.template"],
                "directories": ["circleci"],
                "description": "Deployment configurations and containerization"
            },
            "10-config": {
                "directories": ["config", "configs"],
                "patterns": ["*.config", "*.json", "appsettings*", "nuget*"],
                "files": ["nuget.config", "vcpkg-configuration.jsonc", "requirements.txt"],
                "description": "Configuration files and environment settings"
            }
        }

    def create_structure(self):
        """Create the organized directory structure."""
        for folder_name, config in self.organization_map.items():
            folder_path = self.ai_workspace / folder_name
            folder_path.mkdir(exist_ok=True)

            # Create README for each section
            readme_content = f"""# {folder_name.split('-', 1)[1].replace('-', ' ').title()}

{config['description']}

## Contents
This directory contains:
"""

            if 'directories' in config:
                readme_content += "\n### Directories:\n"
                for dir_name in config['directories']:
                    readme_content += f"- `{dir_name}/`\n"

            if 'files' in config:
                readme_content += "\n### Key Files:\n"
                for file_name in config['files']:
                    readme_content += f"- `{file_name}`\n"

            if 'patterns' in config:
                readme_content += "\n### File Patterns:\n"
                for pattern in config['patterns']:
                    readme_content += f"- `{pattern}`\n"

            with open(folder_path / "README.md", "w") as f:
                f.write(readme_content)

    def organize_files(self):
        """Organize files according to the mapping."""
        print("Starting AI workspace organization...")

        # Create symbolic links instead of moving files to preserve original structure
        for folder_name, config in self.organization_map.items():
            target_dir = self.ai_workspace / folder_name

            # Link directories
            if 'directories' in config:
                for dir_name in config['directories']:
                    source_path = self.root_path / dir_name
                    if source_path.exists():
                        link_path = target_dir / dir_name
                        if not link_path.exists():
                            try:
                                os.symlink(source_path, link_path)
                                print(f"Linked directory: {dir_name} -> {folder_name}")
                            except OSError as e:
                                print(f"Could not link {dir_name}: {e}")

            # Link specific files
            if 'files' in config:
                for file_name in config['files']:
                    source_path = self.root_path / file_name
                    if source_path.exists():
                        link_path = target_dir / file_name
                        if not link_path.exists():
                            try:
                                os.symlink(source_path, link_path)
                                print(f"Linked file: {file_name} -> {folder_name}")
                            except OSError as e:
                                print(f"Could not link {file_name}: {e}")

    def create_master_index(self):
        """Create a master index file for the AI workspace."""
        index_content = """# AI Workspace Index

This organized workspace provides a structured approach to AI development with Semantic Kernel.

## Directory Structure

### 01-notebooks/
Jupyter notebooks for AI experimentation, prototyping, and interactive development.

### 02-agents/
AI agents, agent frameworks, multi-agent systems, and collaboration tools.

### 03-models-training/
Model training scripts, fine-tuning utilities, and LLM development tools.

### 04-plugins/
Semantic Kernel plugins, extensions, and prompt templates.

### 05-samples-demos/
Sample applications, demonstrations, and example implementations.

### 06-backend-services/
Backend services, APIs, Azure Functions, and cloud integrations.

### 07-data-resources/
Datasets, training data, resources, and data processing utilities.

### 08-documentation/
Documentation, guides, tutorials, and reference materials.

### 09-deployment/
Deployment configurations, containerization, and CI/CD setups.

### 10-config/
Configuration files, environment settings, and project configurations.

## Quick Start

1. **Development Environment**: Check `10-config/` for environment setup
2. **Learning**: Start with `01-notebooks/` for interactive examples
3. **Building Agents**: Explore `02-agents/` for agent development
4. **Creating Plugins**: Use `04-plugins/` for extending functionality
5. **Deployment**: Reference `09-deployment/` for production setup

## Key Files

- `organize_files.py`: This organization script
- `ai_workspace_manager.py`: Workspace management utilities
- Various README.md files in each directory for specific guidance

## Usage Patterns

### For AI Research & Development:
1. Start in `01-notebooks/` for experimentation
2. Move to `03-models-training/` for custom model work
3. Use `07-data-resources/` for datasets and resources

### For Production AI Applications:
1. Begin with `05-samples-demos/` for reference implementations
2. Develop in `06-backend-services/` for scalable services
3. Deploy using `09-deployment/` configurations

### For Agent Development:
1. Study examples in `02-agents/`
2. Create plugins in `04-plugins/`
3. Test and iterate in `01-notebooks/`
"""

        with open(self.ai_workspace / "README.md", "w") as f:
            f.write(index_content)

    def run(self):
        """Execute the complete organization process."""
        print("🤖 Starting AI Workspace Organization...")
        print(f"Root path: {self.root_path}")
        print(f"AI workspace: {self.ai_workspace}")

        self.create_structure()
        print("✅ Directory structure created")

        self.organize_files()
        print("✅ Files organized")

        self.create_master_index()
        print("✅ Master index created")

        print("🎉 AI workspace organization complete!")
        print(f"Access your organized workspace at: {self.ai_workspace}")

if __name__ == "__main__":
    organizer = AIWorkspaceOrganizer()
    organizer.run()
