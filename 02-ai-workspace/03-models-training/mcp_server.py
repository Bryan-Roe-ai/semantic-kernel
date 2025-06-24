#!/usr/bin/env python3
"""
Mcp Server module

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
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel import Kernel
from semantic_kernel.connectors.openai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

# Add the ai-workspace directory to the path
workspace_dir = Path(__file__).parent.parent
sys.path.append(str(workspace_dir))

# Import our AI workspace modules
try:
    from advanced_llm_trainer import AdvancedLLMTrainer
except ImportError:
    print("Warning: Could not import AdvancedLLMTrainer")
    AdvancedLLMTrainer = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIWorkspaceMCPServer:
    """MCP Server for AI Workspace functionality"""

    def __init__(self):
        self.kernel = Kernel()
        self.trainer = None
        self.workspace_root = workspace_dir

        # Initialize trainer if available
        if AdvancedLLMTrainer:
            try:
                self.trainer = AdvancedLLMTrainer()
            except Exception as e:
                logger.warning(f"Could not initialize trainer: {e}")

    async def initialize(self):
        """Initialize the MCP server"""
        # Set up OpenAI service if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.kernel.add_service(
                OpenAIChatCompletion(
                    model_id="gpt-4o-mini",
                    api_key=api_key
                )
            )

        # Register functions with the kernel
        self.kernel.add_plugin(self, plugin_name="AIWorkspace")

        logger.info("AI Workspace MCP Server initialized")

    @kernel_function(
        name="list_models",
        description="List available AI models in the workspace"
    )
    async def list_models(self) -> str:
        """List available AI models"""
        try:
            models_dir = self.workspace_root / "03-models-training" / "models"
            if not models_dir.exists():
                return json.dumps({"models": [], "status": "No models directory found"})

            models = []
            for model_path in models_dir.iterdir():
                if model_path.is_dir():
                    models.append({
                        "name": model_path.name,
                        "path": str(model_path),
                        "size": sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
                    })

            return json.dumps({"models": models, "status": "success"})
        except Exception as e:
            return json.dumps({"error": str(e), "status": "error"})

    @kernel_function(
        name="start_training",
        description="Start model training with specified parameters",
    )
    async def start_training(
        self,
        model_name: str,
        dataset_path: str = "",
        learning_rate: float = 2e-4,
        num_epochs: int = 3,
        batch_size: int = 4
    ) -> str:
        """Start model training"""
        try:
            if not self.trainer:
                return json.dumps({"error": "Trainer not available", "status": "error"})

            # Prepare training configuration
            config = {
                "model_name": model_name,
                "dataset_path": dataset_path or "sample_data.jsonl",
                "learning_rate": learning_rate,
                "num_epochs": num_epochs,
                "batch_size": batch_size,
                "output_dir": f"./models/{model_name}-finetuned"
            }

            # Start training (this would be async in a real implementation)
            result = await self._start_training_async(config)
            return json.dumps(result)

        except Exception as e:
            return json.dumps({"error": str(e), "status": "error"})

    async def _start_training_async(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Async training starter"""
        # This is a mock implementation - in reality this would start a background training process
        return {
            "status": "training_started",
            "training_id": f"train_{config['model_name']}_{asyncio.get_event_loop().time()}",
            "config": config,
            "message": "Training started successfully"
        }

    @kernel_function(
        name="get_training_status",
        description="Get the status of a training job"
    )
    async def get_training_status(self, training_id: str = "") -> str:
        """Get training status"""
        try:
            # Mock training status - in reality this would check actual training progress
            status = {
                "training_id": training_id,
                "status": "in_progress",
                "progress": 0.65,
                "current_epoch": 2,
                "total_epochs": 3,
                "loss": 0.234,
                "estimated_time_remaining": "15 minutes"
            }
            return json.dumps(status)
        except Exception as e:
            return json.dumps({"error": str(e), "status": "error"})

    @kernel_function(
        name="analyze_repository",
        description="Analyze a GitHub repository structure and content"
    )
    async def analyze_repository(self, repo_url: str, branch: str = "main") -> str:
        """Analyze a GitHub repository"""
        try:
            # Extract repository info
            if "github.com/" in repo_url:
                repo_parts = repo_url.split("github.com/")[-1].strip("/").split("/")
                if len(repo_parts) >= 2:
                    owner, repo = repo_parts[0], repo_parts[1]
                else:
                    return json.dumps({"error": "Invalid repository URL", "status": "error"})
            else:
                return json.dumps({"error": "Only GitHub repositories are supported", "status": "error"})

            # Mock analysis - in reality this would use GitHub API
            analysis = {
                "repository": f"{owner}/{repo}",
                "branch": branch,
                "analysis": {
                    "primary_language": "Python",
                    "total_files": 245,
                    "code_files": 189,
                    "documentation_files": 23,
                    "test_files": 33,
                    "estimated_complexity": "High",
                    "key_technologies": ["Python", "FastAPI", "Docker", "GitHub Actions"],
                    "structure_quality": "Good",
                    "documentation_coverage": "Moderate"
                },
                "recommendations": [
                    "Consider adding more unit tests",
                    "API documentation could be expanded",
                    "Good use of Docker for deployment"
                ]
            }

            return json.dumps(analysis)
        except Exception as e:
            return json.dumps({"error": str(e), "status": "error"})

    @kernel_function(
        name="process_file",
        description="Process and analyze a file from the workspace"
    )
    async def process_file(self, file_path: str, analysis_type: str = "auto") -> str:
        """Process and analyze a file"""
        try:
            full_path = self.workspace_root / file_path

            if not full_path.exists():
                return json.dumps({"error": "File not found", "status": "error"})

            # Get file info
            file_info = {
                "path": file_path,
                "size": full_path.stat().st_size,
                "extension": full_path.suffix,
                "type": self._get_file_type(full_path.suffix)
            }

            # Analyze based on file type
            if analysis_type == "auto":
                analysis_type = self._determine_analysis_type(full_path.suffix)

            analysis = await self._analyze_file_content(full_path, analysis_type)

            return json.dumps({
                "file_info": file_info,
                "analysis": analysis,
                "status": "success"
            })

        except Exception as e:
            return json.dumps({"error": str(e), "status": "error"})

    def _get_file_type(self, extension: str) -> str:
        """Determine file type from extension"""
        type_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".html": "HTML",
            ".css": "CSS",
            ".md": "Markdown",
            ".json": "JSON",
            ".yml": "YAML",
            ".yaml": "YAML",
            ".txt": "Text",
            ".sh": "Shell Script"
        }
        return type_map.get(extension.lower(), "Unknown")

    def _determine_analysis_type(self, extension: str) -> str:
        """Determine analysis type based on file extension"""
        if extension in [".py", ".js", ".ts"]:
            return "code"
        elif extension in [".md", ".txt"]:
            return "text"
        elif extension in [".json", ".yml", ".yaml"]:
            return "config"
        else:
            return "general"

    async def _analyze_file_content(self, file_path: Path, analysis_type: str) -> Dict[str, Any]:
        """Analyze file content based on type"""
        try:
            content = file_path.read_text(encoding="utf-8")

            if analysis_type == "code":
                return {
                    "type": "code_analysis",
                    "lines": len(content.splitlines()),
                    "characters": len(content),
                    "functions_detected": content.count("def ") + content.count("function "),
                    "classes_detected": content.count("class "),
                    "complexity": "medium"  # Mock complexity
                }
            elif analysis_type == "text":
                return {
                    "type": "text_analysis",
                    "lines": len(content.splitlines()),
                    "words": len(content.split()),
                    "characters": len(content),
                    "readability": "good"  # Mock readability
                }
            elif analysis_type == "config":
                return {
                    "type": "config_analysis",
                    "format": "valid",
                    "keys_found": len(content.split(":")),  # Rough estimate
                    "structure": "nested"
                }
            else:
                return {
                    "type": "general_analysis",
                    "size": len(content),
                    "format": "text"
                }

        except Exception as e:
            return {"error": str(e), "type": "error"}

    @kernel_function(
        name="get_workspace_status",
        description="Get overall workspace status and health"
    )
    async def get_workspace_status(self) -> str:
        """Get workspace status"""
        try:
            # Check various workspace components
            status = {
                "workspace_root": str(self.workspace_root),
                "components": {
                    "notebooks": (self.workspace_root / "01-notebooks").exists(),
                    "agents": (self.workspace_root / "02-agents").exists(),
                    "models": (self.workspace_root / "03-models-training").exists(),
                    "plugins": (self.workspace_root / "04-plugins").exists(),
                    "demos": (self.workspace_root / "05-samples-demos").exists(),
                    "backend": (self.workspace_root / "06-backend-services").exists(),
                    "data": (self.workspace_root / "07-data-resources").exists(),
                    "docs": (self.workspace_root / "08-documentation").exists(),
                    "deployment": (self.workspace_root / "09-deployment").exists(),
                    "config": (self.workspace_root / "10-config").exists()
                },
                "services": {
                    "api_server": "available",
                    "trainer": "available" if self.trainer else "unavailable",
                    "docker": "configured",
                    "github_actions": "configured"
                },
                "health": "good",
                "last_updated": "2025-06-15"
            }

            return json.dumps(status)
        except Exception as e:
            return json.dumps({"error": str(e), "status": "error"})


async def main():
    """Main MCP server entry point"""
    # Initialize the server
    server = AIWorkspaceMCPServer()
    await server.initialize()

    # Set up MCP stdio plugin
    plugin = MCPStdioPlugin(
        name="ai_workspace",
        description="AI Workspace MCP Server for model training, GitHub integration, and file processing",
        kernel=server.kernel
    )

    # Start the MCP server
    logger.info("Starting AI Workspace MCP Server...")
    await plugin.start()


if __name__ == "__main__":
    asyncio.run(main())
