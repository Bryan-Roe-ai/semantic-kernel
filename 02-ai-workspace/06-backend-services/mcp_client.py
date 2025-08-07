import sys
#!/usr/bin/env python3
"""
Mcp Client module

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
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPClient:
    """MCP Client for AI Workspace integration"""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.connected_servers = {}
        self.available_tools = {}

    async def initialize(self):
        """Initialize MCP client"""
        logger.info("Initializing MCP Client for AI Workspace")

        # Check for available MCP servers
        await self._discover_mcp_servers()

    async def _discover_mcp_servers(self):
        """Discover available MCP servers"""
        servers_config = {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "")},
                "description": "GitHub repository integration",
                "available": await self._check_npm_available()
            },
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", self.workspace_root],
                "env": {},
                "description": "File system access",
                "available": await self._check_npm_available()
            }
        }

        for server_name, config in servers_config.items():
            if config["available"]:
                logger.info(f"✅ MCP Server available: {server_name}")
                self.available_tools[server_name] = config
            else:
                logger.warning(f"⚠️ MCP Server unavailable: {server_name}")

    async def _check_npm_available(self) -> bool:
        """Check if npm/npx is available"""
        try:
            result = subprocess.run(
                ["npx", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    async def connect_to_github(self) -> Dict[str, Any]:
        """Connect to GitHub MCP server"""
        if "github" not in self.available_tools:
            return {"error": "GitHub MCP server not available", "status": "error"}

        try:
            # Simulate GitHub MCP connection
            # In a real implementation, this would establish actual MCP connection
            github_tools = await self._simulate_github_tools()

            self.connected_servers["github"] = {
                "status": "connected",
                "tools": github_tools,
                "description": "GitHub Repository Integration"
            }

            return {
                "status": "connected",
                "server": "github",
                "tools_count": len(github_tools),
                "tools": list(github_tools.keys())
            }

        except Exception as e:
            logger.error(f"Failed to connect to GitHub MCP: {e}")
            return {"error": str(e), "status": "error"}

    async def _simulate_github_tools(self) -> Dict[str, Any]:
        """Simulate GitHub MCP tools (in real implementation, these would come from actual MCP server)"""
        return {
            "github_search_repositories": {
                "description": "Search for GitHub repositories",
                "parameters": {
                    "query": {"type": "string", "description": "Search query"},
                    "language": {"type": "string", "description": "Programming language filter", "optional": True}
                }
            },
            "github_get_repository": {
                "description": "Get repository information",
                "parameters": {
                    "owner": {"type": "string", "description": "Repository owner"},
                    "repo": {"type": "string", "description": "Repository name"}
                }
            },
            "github_list_issues": {
                "description": "List repository issues",
                "parameters": {
                    "owner": {"type": "string", "description": "Repository owner"},
                    "repo": {"type": "string", "description": "Repository name"},
                    "state": {"type": "string", "description": "Issue state (open/closed)", "optional": True}
                }
            },
            "github_create_issue": {
                "description": "Create a new issue",
                "parameters": {
                    "owner": {"type": "string", "description": "Repository owner"},
                    "repo": {"type": "string", "description": "Repository name"},
                    "title": {"type": "string", "description": "Issue title"},
                    "body": {"type": "string", "description": "Issue body", "optional": True}
                }
            },
            "github_list_commits": {
                "description": "List repository commits",
                "parameters": {
                    "owner": {"type": "string", "description": "Repository owner"},
                    "repo": {"type": "string", "description": "Repository name"},
                    "branch": {"type": "string", "description": "Branch name", "optional": True}
                }
            }
        }

    async def execute_github_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a GitHub MCP tool"""
        if "github" not in self.connected_servers:
            await self.connect_to_github()

        if "github" not in self.connected_servers:
            return {"error": "GitHub MCP not available", "status": "error"}

        available_tools = self.connected_servers["github"]["tools"]

        if tool_name not in available_tools:
            return {"error": f"Tool {tool_name} not available", "status": "error"}

        # Simulate tool execution (in real implementation, this would call actual MCP server)
        try:
            result = await self._simulate_github_tool_execution(tool_name, parameters)
            return {"result": result, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}

    async def _simulate_github_tool_execution(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Simulate GitHub tool execution"""

        if tool_name == "github_get_repository":
            owner = parameters.get("owner", "")
            repo = parameters.get("repo", "")
            return {
                "name": repo,
                "full_name": f"{owner}/{repo}",
                "description": "AI development workspace with model training capabilities",
                "language": "Python",
                "stargazers_count": 42,
                "forks_count": 8,
                "open_issues_count": 3,
                "default_branch": "main",
                "topics": ["ai", "machine-learning", "model-training", "semantic-kernel"]
            }

        elif tool_name == "github_list_issues":
            return [
                {
                    "number": 1,
                    "title": "Improve model training performance",
                    "state": "open",
                    "labels": ["enhancement", "model-training"],
                    "created_at": "2025-06-15T10:00:00Z"
                },
                {
                    "number": 2,
                    "title": "Add support for custom datasets",
                    "state": "open",
                    "labels": ["feature", "data"],
                    "created_at": "2025-06-14T15:30:00Z"
                }
            ]

        elif tool_name == "github_list_commits":
            return [
                {
                    "sha": "be0002114c5dbf1ac871f0cc7ce610f40a2245b0",
                    "commit": {
                        "message": "Refactor GitHub Actions workflow and update deployment validation scripts",
                        "author": {"name": "Bryan", "date": "2025-06-15T17:28:11Z"}
                    }
                },
                {
                    "sha": "abc123def456",
                    "commit": {
                        "message": "Add MCP integration for GitHub",
                        "author": {"name": "Developer", "date": "2025-06-15T16:00:00Z"}
                    }
                }
            ]

        elif tool_name == "github_search_repositories":
            query = parameters.get("query", "")
            return {
                "total_count": 2,
                "items": [
                    {
                        "name": "semantic-kernel",
                        "full_name": "microsoft/semantic-kernel",
                        "description": "Integrate cutting-edge LLM technology quickly and easily into your apps",
                        "language": "C#",
                        "stargazers_count": 21000
                    },
                    {
                        "name": "ai-workspace",
                        "full_name": "example/ai-workspace",
                        "description": "AI development workspace",
                        "language": "Python",
                        "stargazers_count": 150
                    }
                ]
            }

        else:
            return {"message": f"Executed {tool_name} with parameters {parameters}"}

    async def get_available_tools(self) -> Dict[str, Any]:
        """Get all available MCP tools"""
        tools = {}

        for server_name, server_info in self.connected_servers.items():
            tools[server_name] = {
                "description": server_info["description"],
                "status": server_info["status"],
                "tools": list(server_info["tools"].keys())
            }

        return {
            "servers": tools,
            "total_servers": len(self.connected_servers),
            "total_tools": sum(len(info["tools"]) for info in self.connected_servers.values())
        }

    async def health_check(self) -> Dict[str, Any]:
        """Check health of MCP connections"""
        health = {
            "client_status": "healthy",
            "servers": {},
            "issues": []
        }

        for server_name in self.available_tools:
            if server_name in self.connected_servers:
                health["servers"][server_name] = "connected"
            else:
                health["servers"][server_name] = "available"

        # Check for potential issues
        if not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
            health["issues"].append("GITHUB_PERSONAL_ACCESS_TOKEN not set - GitHub functionality limited")

        if not await self._check_npm_available():
            health["issues"].append("npm/npx not available - some MCP servers unavailable")

        return health

    async def create_mcp_config_for_claude(self) -> Dict[str, Any]:
        """Create MCP configuration for Claude Desktop"""
        config = {
            "mcpServers": {}
        }

        # Add available MCP servers
        for server_name, server_config in self.available_tools.items():
            if server_config["available"]:
                config["mcpServers"][f"ai_workspace_{server_name}"] = {
                    "command": server_config["command"],
                    "args": server_config["args"],
                    "env": server_config["env"]
                }

        return {
            "config": config,
            "status": "success",
            "instructions": "Add this configuration to your Claude Desktop config file"
        }


# FastAPI integration functions
async def initialize_mcp_for_api(workspace_root: Path) -> MCPClient:
    """Initialize MCP client for FastAPI backend"""
    client = MCPClient(workspace_root)
    await client.initialize()
    await client.connect_to_github()
    return client

# Main execution for testing
async def main():
    """Main function for testing MCP client"""
    workspace_root = Path(__file__).parent.parent

    print("🔌 Initializing AI Workspace MCP Client...")
    client = MCPClient(workspace_root)
    await client.initialize()

    print("\n🐙 Connecting to GitHub MCP...")
    github_result = await client.connect_to_github()
    print(json.dumps(github_result, indent=2))

    print("\n🛠️ Available Tools:")
    tools = await client.get_available_tools()
    print(json.dumps(tools, indent=2))

    print("\n📊 Testing GitHub tool execution...")
    test_result = await client.execute_github_tool("github_get_repository", {
        "owner": "microsoft",
        "repo": "semantic-kernel"
    })
    print(json.dumps(test_result, indent=2))

    print("\n🏥 Health Check:")
    health = await client.health_check()
    print(json.dumps(health, indent=2))

    print("\n⚙️ Claude Desktop Configuration:")
    claude_config = await client.create_mcp_config_for_claude()
    print(json.dumps(claude_config, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
