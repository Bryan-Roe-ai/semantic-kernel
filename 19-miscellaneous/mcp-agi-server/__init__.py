"""
MCP AGI Server Package

An advanced Model Context Protocol server with comprehensive AGI capabilities.
"""

__version__ = "1.0.0"
__author__ = "AI Development Team"
__email__ = "dev@agiserver.com"
__description__ = "Advanced MCP Server for AGI Applications"

from .core.server import MCPAGIServer
from .core.config import AGIConfig, load_config
from .tools.registry import ToolRegistry
from .reasoning.engine import ReasoningEngine
from .memory.knowledge_graph import KnowledgeGraph

__all__ = [
    "MCPAGIServer",
    "AGIConfig",
    "load_config",
    "ToolRegistry",
    "ReasoningEngine",
    "KnowledgeGraph"
]
