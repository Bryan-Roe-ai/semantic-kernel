"""
MCP Protocol Handler

This module implements the Model Context Protocol handler for processing
requests and managing protocol-level operations.
"""

import asyncio
import json
import logging
import time
import uuid
from typing import Dict, Any, Optional, Callable, List
from dataclasses import asdict

from .types import (
    MCPRequest, MCPResponse, MCPError, MCPErrorCode,
    Tool, ToolCall, ToolResult,
    ReasoningRequest, ReasoningResult,
    MemoryQuery, MemoryResult,
    LearningUpdate, SessionInfo, AgentCapability
)
from ..core.logging_setup import get_logger, audit_logger, security_logger

class MCPProtocolHandler:
    """
    MCP Protocol Handler

    Handles the Model Context Protocol communication and request routing.
    """

    def __init__(self, server):
        self.server = server
        self.logger = get_logger("protocol")

        # Protocol state
        self.protocol_version = "1.0.0"
        self.supported_methods = {
            "tools/list",
            "tools/call",
            "tools/describe",
            "reasoning/solve",
            "reasoning/explain",
            "memory/query",
            "memory/store",
            "memory/update",
            "learning/update",
            "learning/status",
            "agi/autonomous",
            "agi/capabilities",
            "agi/status",
            "session/create",
            "session/update",
            "session/info"
        }

        # Request handlers
        self.request_handlers: Dict[str, Callable] = {}
        self.middleware: List[Callable] = []

        # Session management
        self.sessions: Dict[str, SessionInfo] = {}

        # Request tracking
        self.active_requests: Dict[str, Dict[str, Any]] = {}
        self.request_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0
        }

    async def initialize(self) -> None:
        """Initialize the protocol handler"""
        try:
            self.logger.info("Initializing MCP Protocol Handler...")

            # Register request handlers
            self._register_handlers()

            # Setup middleware
            self._setup_middleware()

            self.logger.info(f"Protocol handler initialized (version {self.protocol_version})")

        except Exception as e:
            self.logger.error(f"Failed to initialize protocol handler: {e}")
            raise

    def _register_handlers(self) -> None:
        """Register request handlers"""
        self.request_handlers = {
            "tools/list": self._handle_tools_list,
            "tools/call": self._handle_tools_call,
            "tools/describe": self._handle_tools_describe,
            "reasoning/solve": self._handle_reasoning_solve,
            "reasoning/explain": self._handle_reasoning_explain,
            "memory/query": self._handle_memory_query,
            "memory/store": self._handle_memory_store,
            "memory/update": self._handle_memory_update,
            "learning/update": self._handle_learning_update,
            "learning/status": self._handle_learning_status,
            "agi/autonomous": self._handle_agi_autonomous,
            "agi/capabilities": self._handle_agi_capabilities,
            "agi/status": self._handle_agi_status,
            "session/create": self._handle_session_create,
            "session/update": self._handle_session_update,
            "session/info": self._handle_session_info
        }

    def _setup_middleware(self) -> None:
        """Setup request middleware"""
        self.middleware = [
            self._authentication_middleware,
            self._validation_middleware,
            self._rate_limiting_middleware,
            self._logging_middleware
        ]

    async def handle_request(self, request_data: str, session_id: str = None) -> str:
        """Handle incoming MCP request"""
        start_time = time.time()
        request_id = str(uuid.uuid4())

        try:
            # Parse request
            try:
                request = MCPRequest.from_json(request_data)
            except Exception as e:
                return MCPError(
                    code=MCPErrorCode.PARSE_ERROR,
                    message=f"Parse error: {str(e)}"
                ).to_json()

            # Track request
            self.active_requests[request_id] = {
                "request": request,
                "session_id": session_id,
                "start_time": start_time
            }

            self.request_stats["total_requests"] += 1

            # Process middleware
            for middleware in self.middleware:
                result = await middleware(request, session_id)
                if isinstance(result, MCPError):
                    return result.to_json()

            # Route to handler
            if request.method not in self.supported_methods:
                return MCPError(
                    id=request.id,
                    code=MCPErrorCode.METHOD_NOT_FOUND,
                    message=f"Method not found: {request.method}"
                ).to_json()

            handler = self.request_handlers.get(request.method)
            if not handler:
                return MCPError(
                    id=request.id,
                    code=MCPErrorCode.INTERNAL_ERROR,
                    message=f"No handler for method: {request.method}"
                ).to_json()

            # Execute handler
            response = await handler(request, session_id)

            # Update stats
            execution_time = time.time() - start_time
            self._update_request_stats(execution_time, success=True)

            if isinstance(response, MCPResponse):
                return response.to_json()
            elif isinstance(response, MCPError):
                return response.to_json()
            else:
                return MCPResponse(id=request.id, result=response).to_json()

        except Exception as e:
            execution_time = time.time() - start_time
            self._update_request_stats(execution_time, success=False)

            self.logger.error(f"Error handling request {request_id}: {e}")

            return MCPError(
                id=getattr(request, 'id', None),
                code=MCPErrorCode.INTERNAL_ERROR,
                message=f"Internal error: {str(e)}"
            ).to_json()

        finally:
            # Cleanup
            if request_id in self.active_requests:
                del self.active_requests[request_id]

    async def _authentication_middleware(self, request: MCPRequest, session_id: str) -> Optional[MCPError]:
        """Authentication middleware"""
        # For now, allow all requests
        # In production, implement proper authentication
        return None

    async def _validation_middleware(self, request: MCPRequest, session_id: str) -> Optional[MCPError]:
        """Request validation middleware"""
        try:
            # Validate request structure
            if not request.id:
                return MCPError(
                    code=MCPErrorCode.INVALID_REQUEST,
                    message="Missing request ID"
                )

            if not request.method:
                return MCPError(
                    id=request.id,
                    code=MCPErrorCode.INVALID_REQUEST,
                    message="Missing method"
                )

            # Method-specific validation
            if request.method == "tools/call":
                if "name" not in request.params:
                    return MCPError(
                        id=request.id,
                        code=MCPErrorCode.INVALID_PARAMS,
                        message="Missing tool name"
                    )

            elif request.method == "reasoning/solve":
                if "problem" not in request.params:
                    return MCPError(
                        id=request.id,
                        code=MCPErrorCode.INVALID_PARAMS,
                        message="Missing problem statement"
                    )

            elif request.method == "memory/query":
                if "query" not in request.params:
                    return MCPError(
                        id=request.id,
                        code=MCPErrorCode.INVALID_PARAMS,
                        message="Missing query"
                    )

            return None

        except Exception as e:
            return MCPError(
                id=request.id,
                code=MCPErrorCode.INTERNAL_ERROR,
                message=f"Validation error: {str(e)}"
            )

    async def _rate_limiting_middleware(self, request: MCPRequest, session_id: str) -> Optional[MCPError]:
        """Rate limiting middleware"""
        # Simple rate limiting - implement more sophisticated logic as needed
        max_requests_per_minute = 100

        # For now, just log and allow
        # In production, implement proper rate limiting
        return None

    async def _logging_middleware(self, request: MCPRequest, session_id: str) -> Optional[MCPError]:
        """Logging middleware"""
        audit_logger.log_user_action(
            user_id=session_id or "anonymous",
            action=request.method,
            request_id=request.id
        )

        return None

    # Request Handlers

    async def _handle_tools_list(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle tools list request"""
        tools = await self.server.tool_registry.list_tools()

        return MCPResponse(
            id=request.id,
            result={
                "tools": [tool.dict() for tool in tools],
                "count": len(tools)
            }
        )

    async def _handle_tools_call(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle tool call request"""
        tool_name = request.params["name"]
        arguments = request.params.get("arguments", {})
        timeout = request.params.get("timeout")
        resource_limits = request.params.get("resource_limits", {})

        # Create tool call
        tool_call = ToolCall(
            name=tool_name,
            arguments=arguments,
            call_id=str(uuid.uuid4()),
            timeout=timeout,
            resource_limits=resource_limits
        )

        # Execute tool
        result = await self.server.tool_registry.execute_tool(
            tool_call.name,
            tool_call.arguments,
            timeout=tool_call.timeout,
            resource_limits=tool_call.resource_limits
        )

        return MCPResponse(
            id=request.id,
            result=result.dict()
        )

    async def _handle_tools_describe(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle tool describe request"""
        tool_name = request.params.get("name")

        if tool_name:
            tool = await self.server.tool_registry.get_tool(tool_name)
            if tool:
                return MCPResponse(
                    id=request.id,
                    result=tool.dict()
                )
            else:
                return MCPError(
                    id=request.id,
                    code=MCPErrorCode.METHOD_NOT_FOUND,
                    message=f"Tool not found: {tool_name}"
                )
        else:
            # Return all tools with descriptions
            tools = await self.server.tool_registry.list_tools()
            return MCPResponse(
                id=request.id,
                result={
                    "tools": [tool.dict() for tool in tools]
                }
            )

    async def _handle_reasoning_solve(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle reasoning solve request"""
        problem = request.params["problem"]
        context = request.params.get("context", {})
        reasoning_mode = request.params.get("reasoning_mode", "mixed")
        max_steps = request.params.get("max_steps")
        confidence_threshold = request.params.get("confidence_threshold")

        reasoning_request = ReasoningRequest(
            problem=problem,
            context=context,
            reasoning_mode=reasoning_mode,
            max_steps=max_steps,
            confidence_threshold=confidence_threshold
        )

        result = await self.server.reasoning_engine.solve_problem(
            problem=reasoning_request.problem,
            context=reasoning_request.context,
            reasoning_mode=reasoning_request.reasoning_mode,
            max_steps=reasoning_request.max_steps
        )

        return MCPResponse(
            id=request.id,
            result=result
        )

    async def _handle_reasoning_explain(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle reasoning explain request"""
        solution = request.params.get("solution")
        problem = request.params.get("problem")

        explanation = await self.server.reasoning_engine.explain_reasoning(
            solution=solution,
            problem=problem
        )

        return MCPResponse(
            id=request.id,
            result=explanation
        )

    async def _handle_memory_query(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle memory query request"""
        query = request.params["query"]
        query_type = request.params.get("query_type", "semantic")
        max_results = request.params.get("max_results", 10)
        similarity_threshold = request.params.get("similarity_threshold", 0.8)
        filters = request.params.get("filters", {})

        memory_query = MemoryQuery(
            query=query,
            query_type=query_type,
            max_results=max_results,
            similarity_threshold=similarity_threshold,
            filters=filters
        )

        if query_type == "semantic":
            results = await self.server.knowledge_graph.semantic_search(
                query, max_results, similarity_threshold
            )
        elif query_type == "episodic":
            results = await self.server.knowledge_graph.episodic_search(
                query, max_results
            )
        else:
            results = await self.server.knowledge_graph.general_search(
                query, max_results
            )

        return MCPResponse(
            id=request.id,
            result={
                "results": results,
                "query_info": memory_query.dict(),
                "count": len(results)
            }
        )

    async def _handle_memory_store(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle memory store request"""
        data = request.params.get("data")
        memory_type = request.params.get("type", "semantic")
        metadata = request.params.get("metadata", {})

        result = await self.server.knowledge_graph.store_knowledge(
            data=data,
            memory_type=memory_type,
            metadata=metadata
        )

        return MCPResponse(
            id=request.id,
            result=result
        )

    async def _handle_memory_update(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle memory update request"""
        memory_id = request.params.get("memory_id")
        updates = request.params.get("updates", {})

        result = await self.server.knowledge_graph.update_knowledge(
            memory_id=memory_id,
            updates=updates
        )

        return MCPResponse(
            id=request.id,
            result=result
        )

    async def _handle_learning_update(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle learning update request"""
        data = request.params.get("data")
        learning_type = request.params.get("type", "general")
        confidence = request.params.get("confidence", 1.0)
        source = request.params.get("source", "user")
        metadata = request.params.get("metadata", {})

        learning_update = LearningUpdate(
            data=data,
            learning_type=learning_type,
            confidence=confidence,
            source=source,
            metadata=metadata
        )

        result = await self.server.learning_system.update_from_data(
            data=learning_update.data,
            learning_type=learning_update.learning_type,
            confidence=learning_update.confidence
        )

        return MCPResponse(
            id=request.id,
            result=result
        )

    async def _handle_learning_status(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle learning status request"""
        status = await self.server.learning_system.get_status()

        return MCPResponse(
            id=request.id,
            result=status
        )

    async def _handle_agi_autonomous(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle AGI autonomous request"""
        action = request.params.get("action", "status")

        if action == "status":
            result = {
                "autonomous_mode": self.server.autonomous_mode,
                "active_goals": len(self.server.active_goals),
                "goals": [
                    {
                        "id": goal["id"],
                        "description": goal["description"],
                        "progress": goal.get("progress", 0),
                        "created_at": goal["created_at"]
                    }
                    for goal in self.server.active_goals
                ]
            }
        elif action == "enable":
            self.server.autonomous_mode = True
            await self.server._setup_autonomous_mode()
            result = {"autonomous_mode": True, "message": "Autonomous mode enabled"}
        elif action == "disable":
            self.server.autonomous_mode = False
            self.server.active_goals.clear()
            result = {"autonomous_mode": False, "message": "Autonomous mode disabled"}
        else:
            return MCPError(
                id=request.id,
                code=MCPErrorCode.INVALID_PARAMS,
                message=f"Invalid autonomous action: {action}"
            )

        return MCPResponse(
            id=request.id,
            result=result
        )

    async def _handle_agi_capabilities(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle AGI capabilities request"""
        capabilities = [
            AgentCapability(
                name="autonomous_reasoning",
                description="Autonomous multi-step reasoning and problem solving",
                enabled=self.server.config.agi.enable_autonomous_mode,
                confidence_level=0.9
            ),
            AgentCapability(
                name="adaptive_learning",
                description="Real-time learning and adaptation from interactions",
                enabled=self.server.config.learning.enable_online_learning,
                confidence_level=0.8
            ),
            AgentCapability(
                name="memory_management",
                description="Advanced episodic and semantic memory systems",
                enabled=True,
                confidence_level=0.95
            ),
            AgentCapability(
                name="tool_execution",
                description="Safe execution of various tools and functions",
                enabled=self.server.config.tools.enable_code_execution,
                confidence_level=0.9
            ),
            AgentCapability(
                name="self_reflection",
                description="Meta-cognitive self-reflection and improvement",
                enabled=self.server.config.agi.enable_self_reflection,
                confidence_level=0.7
            )
        ]

        return MCPResponse(
            id=request.id,
            result={
                "capabilities": [cap.dict() for cap in capabilities],
                "count": len(capabilities)
            }
        )

    async def _handle_agi_status(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle AGI status request"""
        status = self.server.get_status()

        return MCPResponse(
            id=request.id,
            result=status
        )

    async def _handle_session_create(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle session create request"""
        user_id = request.params.get("user_id")
        preferences = request.params.get("preferences", {})

        new_session_id = str(uuid.uuid4())
        session_info = SessionInfo(
            session_id=new_session_id,
            user_id=user_id,
            created_at=time.time(),
            last_activity=time.time(),
            preferences=preferences
        )

        self.sessions[new_session_id] = session_info

        return MCPResponse(
            id=request.id,
            result=session_info.dict()
        )

    async def _handle_session_update(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle session update request"""
        target_session_id = request.params.get("session_id", session_id)
        updates = request.params.get("updates", {})

        if target_session_id not in self.sessions:
            return MCPError(
                id=request.id,
                code=MCPErrorCode.INVALID_PARAMS,
                message=f"Session not found: {target_session_id}"
            )

        session = self.sessions[target_session_id]
        session.last_activity = time.time()

        for key, value in updates.items():
            if hasattr(session, key):
                setattr(session, key, value)

        return MCPResponse(
            id=request.id,
            result=session.dict()
        )

    async def _handle_session_info(self, request: MCPRequest, session_id: str) -> MCPResponse:
        """Handle session info request"""
        target_session_id = request.params.get("session_id", session_id)

        if target_session_id not in self.sessions:
            return MCPError(
                id=request.id,
                code=MCPErrorCode.INVALID_PARAMS,
                message=f"Session not found: {target_session_id}"
            )

        session = self.sessions[target_session_id]
        session.last_activity = time.time()

        return MCPResponse(
            id=request.id,
            result=session.dict()
        )

    def _update_request_stats(self, execution_time: float, success: bool) -> None:
        """Update request statistics"""
        if success:
            self.request_stats["successful_requests"] += 1
        else:
            self.request_stats["failed_requests"] += 1

        # Update average response time
        current_avg = self.request_stats["average_response_time"]
        total_requests = self.request_stats["total_requests"]

        new_avg = ((current_avg * (total_requests - 1)) + execution_time) / total_requests
        self.request_stats["average_response_time"] = new_avg

    def get_stats(self) -> Dict[str, Any]:
        """Get protocol handler statistics"""
        return {
            "protocol_version": self.protocol_version,
            "supported_methods": list(self.supported_methods),
            "active_requests": len(self.active_requests),
            "active_sessions": len(self.sessions),
            "request_stats": self.request_stats
        }
