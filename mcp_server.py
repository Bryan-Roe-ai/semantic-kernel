#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server for Advanced AI Tool Coordination
Provides structured tool interactions and context sharing for AI agents.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]
    required: List[str]
    handler: callable

class ToolRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

class ToolResponse(BaseModel):
    success: bool
    result: Any
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MCPServer:
    def __init__(self):
        self.app = FastAPI(title="MCP Server", version="1.0.0")
        self.tools: Dict[str, Tool] = {}
        self.active_sessions: Dict[str, WebSocket] = {}
        self.context_store: Dict[str, Any] = {}
        self.setup_routes()
        self.register_default_tools()

    def setup_routes(self):
        """Setup FastAPI routes"""

        @self.app.get("/")
        async def root():
            return {"message": "MCP Server is running", "tools": list(self.tools.keys())}

        @self.app.get("/tools")
        async def list_tools():
            return {
                "tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                        "required": tool.required
                    }
                    for tool in self.tools.values()
                ]
            }

        @self.app.post("/execute", response_model=ToolResponse)
        async def execute_tool(request: ToolRequest):
            try:
                if request.tool_name not in self.tools:
                    raise HTTPException(status_code=404, detail=f"Tool '{request.tool_name}' not found")

                tool = self.tools[request.tool_name]

                # Validate required parameters
                missing_params = set(tool.required) - set(request.parameters.keys())
                if missing_params:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Missing required parameters: {missing_params}"
                    )

                # Execute tool with context
                result = await tool.handler(request.parameters, request.context)

                return ToolResponse(
                    success=True,
                    result=result,
                    metadata={"tool_name": request.tool_name}
                )

            except Exception as e:
                logger.error(f"Error executing tool {request.tool_name}: {e}")
                return ToolResponse(
                    success=False,
                    result=None,
                    error=str(e)
                )

        @self.app.websocket("/ws/{session_id}")
        async def websocket_endpoint(websocket: WebSocket, session_id: str):
            await websocket.accept()
            self.active_sessions[session_id] = websocket

            try:
                while True:
                    data = await websocket.receive_text()
                    message = json.loads(data)

                    if message.get("type") == "tool_request":
                        request = ToolRequest(**message["data"])
                        response = await execute_tool(request)
                        await websocket.send_text(json.dumps({
                            "type": "tool_response",
                            "data": response.dict()
                        }))
                    elif message.get("type") == "context_update":
                        self.context_store[session_id] = message["data"]
                        await websocket.send_text(json.dumps({
                            "type": "context_ack",
                            "data": {"status": "updated"}
                        }))

            except WebSocketDisconnect:
                del self.active_sessions[session_id]
                if session_id in self.context_store:
                    del self.context_store[session_id]

    def register_tool(self, tool: Tool):
        """Register a new tool"""
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def register_default_tools(self):
        """Register default tools for AI coordination"""

        # File operations
        self.register_tool(Tool(
            name="read_file",
            description="Read contents of a file",
            parameters={
                "file_path": {"type": "string", "description": "Path to the file"}
            },
            required=["file_path"],
            handler=self._read_file
        ))

        self.register_tool(Tool(
            name="write_file",
            description="Write content to a file",
            parameters={
                "file_path": {"type": "string", "description": "Path to the file"},
                "content": {"type": "string", "description": "Content to write"}
            },
            required=["file_path", "content"],
            handler=self._write_file
        ))

        # Code analysis
        self.register_tool(Tool(
            name="analyze_code",
            description="Analyze code structure and quality",
            parameters={
                "file_path": {"type": "string", "description": "Path to code file"},
                "language": {"type": "string", "description": "Programming language"}
            },
            required=["file_path"],
            handler=self._analyze_code
        ))

        # Semantic Kernel integration
        self.register_tool(Tool(
            name="run_sk_function",
            description="Execute a Semantic Kernel function",
            parameters={
                "function_name": {"type": "string", "description": "Name of SK function"},
                "arguments": {"type": "object", "description": "Function arguments"}
            },
            required=["function_name"],
            handler=self._run_sk_function
        ))

        # Context management
        self.register_tool(Tool(
            name="get_context",
            description="Retrieve stored context for a session",
            parameters={
                "session_id": {"type": "string", "description": "Session identifier"}
            },
            required=["session_id"],
            handler=self._get_context
        ))

        # AI model interaction
        self.register_tool(Tool(
            name="query_ai_model",
            description="Query local or remote AI model",
            parameters={
                "prompt": {"type": "string", "description": "Prompt for the AI model"},
                "model": {"type": "string", "description": "Model identifier"},
                "parameters": {"type": "object", "description": "Model parameters"}
            },
            required=["prompt"],
            handler=self._query_ai_model
        ))

    async def _read_file(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None):
        """Read file tool handler"""
        file_path = Path(params["file_path"])

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                "content": content,
                "size": len(content),
                "path": str(file_path),
                "encoding": "utf-8"
            }
        except UnicodeDecodeError:
            # Try binary read for non-text files
            with open(file_path, 'rb') as f:
                content = f.read()

            return {
                "content": content.hex(),
                "size": len(content),
                "path": str(file_path),
                "encoding": "binary"
            }

    async def _write_file(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None):
        """Write file tool handler"""
        file_path = Path(params["file_path"])
        content = params["content"]

        # Create directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "path": str(file_path),
            "size": len(content),
            "status": "written"
        }

    async def _analyze_code(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None):
        """Code analysis tool handler"""
        file_path = Path(params["file_path"])
        language = params.get("language", "auto")

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # Basic analysis
        lines = code.split('\n')
        analysis = {
            "file_path": str(file_path),
            "language": language,
            "metrics": {
                "lines_total": len(lines),
                "lines_code": len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
                "lines_comments": len([line for line in lines if line.strip().startswith('#')]),
                "lines_blank": len([line for line in lines if not line.strip()])
            },
            "functions": [],
            "classes": [],
            "imports": []
        }

        # Language-specific analysis
        if language == "python" or file_path.suffix == ".py":
            import ast
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        analysis["functions"].append({
                            "name": node.name,
                            "line": node.lineno,
                            "args": len(node.args.args)
                        })
                    elif isinstance(node, ast.ClassDef):
                        analysis["classes"].append({
                            "name": node.name,
                            "line": node.lineno
                        })
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            analysis["imports"].append(node.module)
            except SyntaxError as e:
                analysis["syntax_error"] = str(e)

        return analysis

    async def _run_sk_function(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None):
        """Semantic Kernel function execution handler"""
        function_name = params["function_name"]
        arguments = params.get("arguments", {})

        # Placeholder for Semantic Kernel integration
        return {
            "function_name": function_name,
            "arguments": arguments,
            "result": f"Executed {function_name} with args {arguments}",
            "status": "success"
        }

    async def _get_context(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None):
        """Get context tool handler"""
        session_id = params["session_id"]

        return {
            "session_id": session_id,
            "context": self.context_store.get(session_id, {}),
            "available_sessions": list(self.context_store.keys())
        }

    async def _query_ai_model(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None):
        """AI model query handler"""
        prompt = params["prompt"]
        model = params.get("model", "default")
        model_params = params.get("parameters", {})

        # Placeholder for AI model integration
        return {
            "prompt": prompt,
            "model": model,
            "parameters": model_params,
            "response": f"AI response to: {prompt[:50]}...",
            "status": "success"
        }

    async def broadcast_to_sessions(self, message: Dict[str, Any]):
        """Broadcast message to all active sessions"""
        disconnected = []
        for session_id, websocket in self.active_sessions.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception:
                disconnected.append(session_id)

        # Clean up disconnected sessions
        for session_id in disconnected:
            del self.active_sessions[session_id]

def main():
    """Start the MCP server"""
    server = MCPServer()

    # Configuration
    host = "127.0.0.1"
    port = 8000

    logger.info(f"Starting MCP Server on {host}:{port}")
    logger.info(f"Available tools: {list(server.tools.keys())}")

    uvicorn.run(
        server.app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()
