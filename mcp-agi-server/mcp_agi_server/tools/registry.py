"""
Tool Registry for MCP AGI Server

This module manages the registration, execution, and lifecycle of tools
available to the AGI system.
"""

import asyncio
import importlib
import inspect
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Type
from dataclasses import dataclass

from ..protocol.types import Tool, ToolParameter, ToolParameterType, ToolResult
from ..core.logging_setup import get_logger, performance_logger, security_logger
from ..safety.sandbox import SandboxManager

@dataclass
class ToolExecutionContext:
    """Context for tool execution"""
    tool_name: str
    arguments: Dict[str, Any]
    timeout: Optional[int] = None
    resource_limits: Dict[str, Any] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class BaseTool:
    """Base class for all tools"""

    def __init__(self):
        self.name = self.__class__.__name__.lower()
        self.description = "Base tool"
        self.category = "general"
        self.version = "1.0.0"
        self.parameters: List[ToolParameter] = []
        self.permissions: List[str] = []
        self.resource_requirements = {}

    async def execute(self, context: ToolExecutionContext) -> ToolResult:
        """Execute the tool"""
        raise NotImplementedError("Tool must implement execute method")

    def validate_arguments(self, arguments: Dict[str, Any]) -> bool:
        """Validate tool arguments"""
        # Basic validation - can be overridden
        required_params = [p.name for p in self.parameters if p.required]

        for param in required_params:
            if param not in arguments:
                return False

        return True

    def get_tool_definition(self) -> Tool:
        """Get tool definition for MCP"""
        return Tool(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
            category=self.category,
            version=self.version,
            permissions=self.permissions,
            resource_requirements=self.resource_requirements
        )

class CodeExecutionTool(BaseTool):
    """Tool for executing code safely"""

    def __init__(self, sandbox_manager: SandboxManager):
        super().__init__()
        self.name = "execute_code"
        self.description = "Execute code in a secure sandbox environment"
        self.category = "development"
        self.sandbox_manager = sandbox_manager

        self.parameters = [
            ToolParameter(
                name="code",
                type=ToolParameterType.STRING,
                description="Code to execute",
                required=True
            ),
            ToolParameter(
                name="language",
                type=ToolParameterType.STRING,
                description="Programming language",
                required=True,
                enum=["python", "javascript", "bash", "sql"]
            ),
            ToolParameter(
                name="timeout",
                type=ToolParameterType.INTEGER,
                description="Execution timeout in seconds",
                required=False,
                default=30,
                minimum=1,
                maximum=300
            )
        ]

        self.permissions = ["sandbox_execution"]
        self.resource_requirements = {
            "cpu_limit": "1 core",
            "memory_limit": "512MB",
            "disk_limit": "100MB"
        }

    async def execute(self, context: ToolExecutionContext) -> ToolResult:
        """Execute code in sandbox"""
        try:
            code = context.arguments["code"]
            language = context.arguments["language"]
            timeout = context.arguments.get("timeout", 30)

            # Security check
            if not self._is_code_safe(code, language):
                security_logger.log_security_violation(
                    violation_type="unsafe_code",
                    details=f"Potentially unsafe {language} code detected",
                    user_id=context.user_id
                )
                return ToolResult(
                    success=False,
                    error="Code contains potentially unsafe operations"
                )

            # Execute in sandbox
            start_time = time.time()
            result = await self.sandbox_manager.execute_code(
                code=code,
                language=language,
                timeout=timeout,
                user_id=context.user_id
            )
            execution_time = time.time() - start_time

            return ToolResult(
                success=result.get("success", False),
                result=result.get("output"),
                error=result.get("error"),
                execution_time=execution_time,
                resource_usage=result.get("resource_usage", {}),
                metadata={
                    "language": language,
                    "lines_of_code": len(code.split('\n'))
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Code execution failed: {str(e)}"
            )

    def _is_code_safe(self, code: str, language: str) -> bool:
        """Basic code safety check"""
        dangerous_patterns = {
            "python": [
                "import os", "import sys", "import subprocess",
                "eval(", "exec(", "__import__", "open(",
                "file(", "input(", "raw_input("
            ],
            "javascript": [
                "require(", "process.", "fs.", "child_process",
                "eval(", "Function("
            ],
            "bash": [
                "rm ", "sudo ", "su ", "chmod ", "chown ",
                "wget ", "curl ", "nc ", "netcat"
            ]
        }

        patterns = dangerous_patterns.get(language, [])
        return not any(pattern in code for pattern in patterns)

class WebSearchTool(BaseTool):
    """Tool for web search and information retrieval"""

    def __init__(self):
        super().__init__()
        self.name = "web_search"
        self.description = "Search the web for information"
        self.category = "research"

        self.parameters = [
            ToolParameter(
                name="query",
                type=ToolParameterType.STRING,
                description="Search query",
                required=True
            ),
            ToolParameter(
                name="max_results",
                type=ToolParameterType.INTEGER,
                description="Maximum number of results",
                required=False,
                default=10,
                minimum=1,
                maximum=50
            ),
            ToolParameter(
                name="search_type",
                type=ToolParameterType.STRING,
                description="Type of search",
                required=False,
                default="general",
                enum=["general", "academic", "news", "images"]
            )
        ]

        self.permissions = ["web_access"]

    async def execute(self, context: ToolExecutionContext) -> ToolResult:
        """Perform web search"""
        try:
            query = context.arguments["query"]
            max_results = context.arguments.get("max_results", 10)
            search_type = context.arguments.get("search_type", "general")

            # Mock web search - in production, use actual search API
            results = [
                {
                    "title": f"Result {i+1} for '{query}'",
                    "url": f"https://example.com/result{i+1}",
                    "snippet": f"This is a mock search result {i+1} for the query '{query}'",
                    "relevance_score": 0.9 - (i * 0.1)
                }
                for i in range(min(max_results, 5))
            ]

            return ToolResult(
                success=True,
                result={
                    "query": query,
                    "results": results,
                    "total_results": len(results),
                    "search_type": search_type
                },
                metadata={
                    "search_engine": "mock",
                    "response_time": 0.5
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Web search failed: {str(e)}"
            )

class FileOperationTool(BaseTool):
    """Tool for file operations"""

    def __init__(self, sandbox_manager: SandboxManager):
        super().__init__()
        self.name = "file_operations"
        self.description = "Perform file operations in a secure environment"
        self.category = "filesystem"
        self.sandbox_manager = sandbox_manager

        self.parameters = [
            ToolParameter(
                name="operation",
                type=ToolParameterType.STRING,
                description="File operation to perform",
                required=True,
                enum=["read", "write", "list", "create_dir", "delete"]
            ),
            ToolParameter(
                name="path",
                type=ToolParameterType.STRING,
                description="File or directory path",
                required=True
            ),
            ToolParameter(
                name="content",
                type=ToolParameterType.STRING,
                description="Content for write operations",
                required=False
            )
        ]

        self.permissions = ["file_access"]

    async def execute(self, context: ToolExecutionContext) -> ToolResult:
        """Perform file operation"""
        try:
            operation = context.arguments["operation"]
            path = context.arguments["path"]
            content = context.arguments.get("content")

            # Security check
            if not self._is_path_safe(path):
                security_logger.log_security_violation(
                    violation_type="unsafe_path",
                    details=f"Potentially unsafe path: {path}",
                    user_id=context.user_id
                )
                return ToolResult(
                    success=False,
                    error="Path contains potentially unsafe operations"
                )

            # Execute file operation in sandbox
            result = await self.sandbox_manager.file_operation(
                operation=operation,
                path=path,
                content=content,
                user_id=context.user_id
            )

            return ToolResult(
                success=result.get("success", False),
                result=result.get("result"),
                error=result.get("error"),
                metadata={
                    "operation": operation,
                    "path": path
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"File operation failed: {str(e)}"
            )

    def _is_path_safe(self, path: str) -> bool:
        """Check if path is safe"""
        dangerous_patterns = [
            "..", "/etc/", "/root/", "/home/",
            "/usr/", "/var/", "/sys/", "/proc/"
        ]
        return not any(pattern in path for pattern in dangerous_patterns)

class DataAnalysisTool(BaseTool):
    """Tool for data analysis operations"""

    def __init__(self):
        super().__init__()
        self.name = "data_analysis"
        self.description = "Perform data analysis and visualization"
        self.category = "analytics"

        self.parameters = [
            ToolParameter(
                name="data",
                type=ToolParameterType.ARRAY,
                description="Data to analyze",
                required=True
            ),
            ToolParameter(
                name="analysis_type",
                type=ToolParameterType.STRING,
                description="Type of analysis",
                required=True,
                enum=["summary", "correlation", "trend", "distribution"]
            ),
            ToolParameter(
                name="format",
                type=ToolParameterType.STRING,
                description="Output format",
                required=False,
                default="json",
                enum=["json", "csv", "chart"]
            )
        ]

    async def execute(self, context: ToolExecutionContext) -> ToolResult:
        """Perform data analysis"""
        try:
            data = context.arguments["data"]
            analysis_type = context.arguments["analysis_type"]
            output_format = context.arguments.get("format", "json")

            # Mock data analysis
            if analysis_type == "summary":
                result = {
                    "count": len(data),
                    "mean": sum(data) / len(data) if data and all(isinstance(x, (int, float)) for x in data) else None,
                    "min": min(data) if data else None,
                    "max": max(data) if data else None
                }
            elif analysis_type == "correlation":
                result = {"correlation": "Mock correlation analysis"}
            elif analysis_type == "trend":
                result = {"trend": "Mock trend analysis"}
            elif analysis_type == "distribution":
                result = {"distribution": "Mock distribution analysis"}
            else:
                result = {"analysis": f"Mock {analysis_type} analysis"}

            return ToolResult(
                success=True,
                result=result,
                metadata={
                    "analysis_type": analysis_type,
                    "data_points": len(data),
                    "output_format": output_format
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Data analysis failed: {str(e)}"
            )

class SystemInfoTool(BaseTool):
    """Tool for system information"""

    def __init__(self):
        super().__init__()
        self.name = "system_info"
        self.description = "Get system information and metrics"
        self.category = "system"

        self.parameters = [
            ToolParameter(
                name="info_type",
                type=ToolParameterType.STRING,
                description="Type of system information",
                required=True,
                enum=["cpu", "memory", "disk", "network", "processes", "all"]
            )
        ]

    async def execute(self, context: ToolExecutionContext) -> ToolResult:
        """Get system information"""
        try:
            info_type = context.arguments["info_type"]

            # Mock system info - in production, use actual system monitoring
            system_info = {
                "cpu": {"usage": 45.2, "cores": 8},
                "memory": {"usage": 67.8, "total_gb": 16, "available_gb": 5.2},
                "disk": {"usage": 23.4, "total_gb": 500, "free_gb": 383},
                "network": {"bytes_sent": 1024000, "bytes_recv": 2048000},
                "processes": {"total": 156, "running": 12}
            }

            if info_type == "all":
                result = system_info
            else:
                result = system_info.get(info_type, {})

            return ToolResult(
                success=True,
                result=result,
                metadata={
                    "info_type": info_type,
                    "timestamp": time.time()
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"System info retrieval failed: {str(e)}"
            )

class ToolRegistry:
    """Registry for managing tools"""

    def __init__(self, config, sandbox_manager: SandboxManager):
        self.config = config
        self.sandbox_manager = sandbox_manager
        self.logger = get_logger("tools")

        # Tool storage
        self.tools: Dict[str, BaseTool] = {}
        self.tool_categories: Dict[str, List[str]] = {}

        # Execution tracking
        self.execution_stats: Dict[str, Dict[str, Any]] = {}

    async def initialize(self) -> None:
        """Initialize the tool registry"""
        try:
            self.logger.info("Initializing tool registry...")

            # Register built-in tools
            await self._register_builtin_tools()

            # Load external tools
            await self._load_external_tools()

            self.logger.info(f"Tool registry initialized with {len(self.tools)} tools")

        except Exception as e:
            self.logger.error(f"Failed to initialize tool registry: {e}")
            raise

    async def _register_builtin_tools(self) -> None:
        """Register built-in tools"""
        builtin_tools = []

        if self.config.enable_code_execution:
            builtin_tools.append(CodeExecutionTool(self.sandbox_manager))

        if self.config.enable_web_search:
            builtin_tools.append(WebSearchTool())

        if self.config.enable_file_operations:
            builtin_tools.append(FileOperationTool(self.sandbox_manager))

        if self.config.enable_data_analysis:
            builtin_tools.append(DataAnalysisTool())

        if self.config.enable_system_info:
            builtin_tools.append(SystemInfoTool())

        for tool in builtin_tools:
            await self.register_tool(tool)

    async def _load_external_tools(self) -> None:
        """Load external tools from plugins directory"""
        # This would load tools from a plugins directory
        # For now, we'll skip this implementation
        pass

    async def register_tool(self, tool: BaseTool) -> None:
        """Register a tool"""
        try:
            tool_name = tool.name

            if tool_name in self.tools:
                self.logger.warning(f"Tool {tool_name} already registered, replacing")

            self.tools[tool_name] = tool

            # Add to category
            category = tool.category
            if category not in self.tool_categories:
                self.tool_categories[category] = []

            if tool_name not in self.tool_categories[category]:
                self.tool_categories[category].append(tool_name)

            # Initialize stats
            self.execution_stats[tool_name] = {
                "executions": 0,
                "successes": 0,
                "failures": 0,
                "total_execution_time": 0.0,
                "average_execution_time": 0.0
            }

            self.logger.info(f"Registered tool: {tool_name}")

        except Exception as e:
            self.logger.error(f"Failed to register tool {tool.name}: {e}")
            raise

    async def unregister_tool(self, tool_name: str) -> bool:
        """Unregister a tool"""
        try:
            if tool_name not in self.tools:
                return False

            tool = self.tools[tool_name]

            # Remove from tools
            del self.tools[tool_name]

            # Remove from category
            category = tool.category
            if category in self.tool_categories:
                if tool_name in self.tool_categories[category]:
                    self.tool_categories[category].remove(tool_name)

                # Remove category if empty
                if not self.tool_categories[category]:
                    del self.tool_categories[category]

            # Remove stats
            if tool_name in self.execution_stats:
                del self.execution_stats[tool_name]

            self.logger.info(f"Unregistered tool: {tool_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to unregister tool {tool_name}: {e}")
            return False

    async def list_tools(self) -> List[Tool]:
        """List all registered tools"""
        return [tool.get_tool_definition() for tool in self.tools.values()]

    async def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Get a specific tool definition"""
        tool = self.tools.get(tool_name)
        return tool.get_tool_definition() if tool else None

    async def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        timeout: Optional[int] = None,
        resource_limits: Dict[str, Any] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> ToolResult:
        """Execute a tool"""
        start_time = time.time()

        try:
            # Check if tool exists
            if tool_name not in self.tools:
                return ToolResult(
                    success=False,
                    error=f"Tool not found: {tool_name}"
                )

            tool = self.tools[tool_name]

            # Validate arguments
            if not tool.validate_arguments(arguments):
                return ToolResult(
                    success=False,
                    error="Invalid arguments"
                )

            # Create execution context
            context = ToolExecutionContext(
                tool_name=tool_name,
                arguments=arguments,
                timeout=timeout or self.config.max_tool_execution_time,
                resource_limits=resource_limits,
                user_id=user_id,
                session_id=session_id
            )

            # Execute tool
            result = await asyncio.wait_for(
                tool.execute(context),
                timeout=context.timeout
            )

            # Update stats
            execution_time = time.time() - start_time
            self._update_execution_stats(tool_name, execution_time, result.success)

            # Log performance
            performance_logger.log_tool_execution(
                tool_name=tool_name,
                execution_time=execution_time,
                success=result.success,
                resource_usage=result.resource_usage
            )

            return result

        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            self._update_execution_stats(tool_name, execution_time, False)

            return ToolResult(
                success=False,
                error=f"Tool execution timed out after {timeout}s",
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._update_execution_stats(tool_name, execution_time, False)

            self.logger.error(f"Tool execution error ({tool_name}): {e}")

            return ToolResult(
                success=False,
                error=f"Tool execution failed: {str(e)}",
                execution_time=execution_time
            )

    def _update_execution_stats(self, tool_name: str, execution_time: float, success: bool) -> None:
        """Update tool execution statistics"""
        if tool_name not in self.execution_stats:
            return

        stats = self.execution_stats[tool_name]
        stats["executions"] += 1
        stats["total_execution_time"] += execution_time

        if success:
            stats["successes"] += 1
        else:
            stats["failures"] += 1

        # Update average
        stats["average_execution_time"] = stats["total_execution_time"] / stats["executions"]

    def get_tool_stats(self, tool_name: str = None) -> Dict[str, Any]:
        """Get tool execution statistics"""
        if tool_name:
            return self.execution_stats.get(tool_name, {})
        else:
            return self.execution_stats.copy()

    def get_categories(self) -> Dict[str, List[str]]:
        """Get tool categories"""
        return self.tool_categories.copy()

    async def shutdown(self) -> None:
        """Shutdown the tool registry"""
        try:
            self.logger.info("Shutting down tool registry...")

            # Save execution stats if needed
            # Clear tools
            self.tools.clear()
            self.tool_categories.clear()

            self.logger.info("Tool registry shutdown complete")

        except Exception as e:
            self.logger.error(f"Error during tool registry shutdown: {e}")
