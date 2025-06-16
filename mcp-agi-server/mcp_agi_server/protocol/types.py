"""
MCP Protocol Types and Data Structures

This module defines the core types and data structures used in the
Model Context Protocol implementation.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union, Literal
from enum import Enum
import json

class ToolParameterType(Enum):
    """Tool parameter types"""
    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"

@dataclass
class ToolParameter:
    """Tool parameter definition"""
    name: str
    type: ToolParameterType
    description: str
    required: bool = True
    default: Any = None
    enum: Optional[List[Any]] = None
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[Union[int, float]] = None
    pattern: Optional[str] = None

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            "name": self.name,
            "type": self.type.value,
            "description": self.description,
            "required": self.required
        }

        if self.default is not None:
            result["default"] = self.default
        if self.enum is not None:
            result["enum"] = self.enum
        if self.minimum is not None:
            result["minimum"] = self.minimum
        if self.maximum is not None:
            result["maximum"] = self.maximum
        if self.pattern is not None:
            result["pattern"] = self.pattern

        return result

@dataclass
class Tool:
    """Tool definition for MCP"""
    name: str
    description: str
    parameters: List[ToolParameter] = field(default_factory=list)
    category: str = "general"
    version: str = "1.0.0"
    author: str = "AGI Server"
    tags: List[str] = field(default_factory=list)
    examples: List[Dict[str, Any]] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    resource_requirements: Dict[str, Any] = field(default_factory=dict)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [param.dict() for param in self.parameters],
            "category": self.category,
            "version": self.version,
            "author": self.author,
            "tags": self.tags,
            "examples": self.examples,
            "permissions": self.permissions,
            "resource_requirements": self.resource_requirements
        }

@dataclass
class ToolCall:
    """Tool call request"""
    name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    call_id: Optional[str] = None
    timeout: Optional[int] = None
    resource_limits: Dict[str, Any] = field(default_factory=dict)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            "name": self.name,
            "arguments": self.arguments
        }

        if self.call_id:
            result["call_id"] = self.call_id
        if self.timeout:
            result["timeout"] = self.timeout
        if self.resource_limits:
            result["resource_limits"] = self.resource_limits

        return result

@dataclass
class ToolResult:
    """Tool execution result"""
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result_dict = {
            "success": self.success
        }

        if self.result is not None:
            result_dict["result"] = self.result
        if self.error:
            result_dict["error"] = self.error
        if self.execution_time is not None:
            result_dict["execution_time"] = self.execution_time
        if self.resource_usage:
            result_dict["resource_usage"] = self.resource_usage
        if self.metadata:
            result_dict["metadata"] = self.metadata
        if self.warnings:
            result_dict["warnings"] = self.warnings

        return result_dict

@dataclass
class MCPRequest:
    """MCP request structure"""
    id: str
    method: str
    params: Dict[str, Any] = field(default_factory=dict)
    jsonrpc: str = "2.0"

    @classmethod
    def from_json(cls, json_str: str) -> "MCPRequest":
        """Create request from JSON string"""
        data = json.loads(json_str)
        return cls(
            id=data["id"],
            method=data["method"],
            params=data.get("params", {}),
            jsonrpc=data.get("jsonrpc", "2.0")
        )

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps({
            "id": self.id,
            "method": self.method,
            "params": self.params,
            "jsonrpc": self.jsonrpc
        })

@dataclass
class MCPResponse:
    """MCP response structure"""
    id: str
    result: Any = None
    jsonrpc: str = "2.0"

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps({
            "id": self.id,
            "result": self.result,
            "jsonrpc": self.jsonrpc
        })

@dataclass
class MCPError:
    """MCP error response"""
    id: Optional[str] = None
    code: int = -32603
    message: str = "Internal error"
    data: Any = None
    jsonrpc: str = "2.0"

    def to_json(self) -> str:
        """Convert to JSON string"""
        error_dict = {
            "id": self.id,
            "error": {
                "code": self.code,
                "message": self.message
            },
            "jsonrpc": self.jsonrpc
        }

        if self.data is not None:
            error_dict["error"]["data"] = self.data

        return json.dumps(error_dict)

# Standard MCP error codes
class MCPErrorCode:
    """Standard MCP error codes"""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

    # Custom AGI server errors
    SAFETY_VIOLATION = -40001
    RESOURCE_LIMIT_EXCEEDED = -40002
    SANDBOX_ERROR = -40003
    REASONING_ERROR = -40004
    MEMORY_ERROR = -40005
    LEARNING_ERROR = -40006
    AUTONOMOUS_MODE_ERROR = -40007

@dataclass
class ReasoningRequest:
    """Reasoning request structure"""
    problem: str
    context: Dict[str, Any] = field(default_factory=dict)
    reasoning_mode: str = "mixed"
    max_steps: Optional[int] = None
    confidence_threshold: Optional[float] = None

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            "problem": self.problem,
            "context": self.context,
            "reasoning_mode": self.reasoning_mode
        }

        if self.max_steps is not None:
            result["max_steps"] = self.max_steps
        if self.confidence_threshold is not None:
            result["confidence_threshold"] = self.confidence_threshold

        return result

@dataclass
class ReasoningResult:
    """Reasoning result structure"""
    solution: Any
    confidence: float
    reasoning_steps: List[Dict[str, Any]] = field(default_factory=list)
    execution_time: Optional[float] = None
    reasoning_mode: str = "mixed"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "solution": self.solution,
            "confidence": self.confidence,
            "reasoning_steps": self.reasoning_steps,
            "execution_time": self.execution_time,
            "reasoning_mode": self.reasoning_mode,
            "metadata": self.metadata
        }

@dataclass
class MemoryQuery:
    """Memory query structure"""
    query: str
    query_type: str = "semantic"
    max_results: int = 10
    similarity_threshold: float = 0.8
    filters: Dict[str, Any] = field(default_factory=dict)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "query": self.query,
            "query_type": self.query_type,
            "max_results": self.max_results,
            "similarity_threshold": self.similarity_threshold,
            "filters": self.filters
        }

@dataclass
class MemoryResult:
    """Memory query result"""
    results: List[Dict[str, Any]]
    query_info: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "results": self.results,
            "query_info": self.query_info,
            "metadata": self.metadata
        }

@dataclass
class LearningUpdate:
    """Learning update structure"""
    data: Any
    learning_type: str = "general"
    confidence: float = 1.0
    source: str = "user"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "data": self.data,
            "learning_type": self.learning_type,
            "confidence": self.confidence,
            "source": self.source,
            "metadata": self.metadata
        }

@dataclass
class AgentCapability:
    """Agent capability description"""
    name: str
    description: str
    enabled: bool = True
    confidence_level: float = 1.0
    prerequisites: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "confidence_level": self.confidence_level,
            "prerequisites": self.prerequisites,
            "limitations": self.limitations,
            "examples": self.examples
        }

@dataclass
class SessionInfo:
    """Session information"""
    session_id: str
    user_id: Optional[str] = None
    created_at: float = 0.0
    last_activity: float = 0.0
    capabilities: List[AgentCapability] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "last_activity": self.last_activity,
            "capabilities": [cap.dict() for cap in self.capabilities],
            "context": self.context,
            "preferences": self.preferences
        }
