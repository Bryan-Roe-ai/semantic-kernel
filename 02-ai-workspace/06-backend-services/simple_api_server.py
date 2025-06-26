import sys
#!/usr/bin/env python3
"""
Simple Api Server module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import asyncio

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

# Import MCP client
try:
    from mcp_client import MCPClient, initialize_mcp_for_api
except ImportError:
    MCPClient = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data Models
class ChatMessage(BaseModel):
    message: str
    system: Optional[str] = None
    model: Optional[str] = "gpt2"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 150
    stream: Optional[bool] = False

class TrainingRequest(BaseModel):
    model_name: str
    dataset_path: Optional[str] = None
    training_data: Optional[List[Dict[str, Any]]] = None
    epochs: int = 3
    learning_rate: float = 5e-5
    batch_size: int = 4
    use_lora: bool = True

class ModelInfo(BaseModel):
    name: str
    type: str = "causal_lm"
    status: str = "available"
    size: Optional[str] = None
    created: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(
    title="Custom LLM Studio API",
    description="Backend API for custom model training and inference",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
models_db = {}
training_jobs = {}
chat_sessions = {}

# Global MCP client
mcp_client = None

# Mount static files
static_path = Path(__file__).parent.parent / "05-samples-demos"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/")
async def root():
    """Serve the main landing page."""
    index_file = static_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    else:
        return {"message": "Custom LLM Studio API", "status": "running", "web_ui": "/web"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": len(models_db),
        "active_training_jobs": len([j for j in training_jobs.values() if j["status"] == "running"])
    }

@app.post("/api/chat")
async def chat_completion(request: ChatMessage):
    """Basic chat completion endpoint (mock implementation)."""
    try:
        # Mock response for demonstration
        response_text = f"This is a mock response to: '{request.message}'"

        if request.system:
            response_text = f"[System: {request.system}] {response_text}"

        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = {
            "messages": [
                {"role": "user", "content": request.message},
                {"role": "assistant", "content": response_text}
            ],
            "model": request.model,
            "timestamp": datetime.now().isoformat()
        }

        return {
            "response": response_text,
            "session_id": session_id,
            "model": request.model,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models")
async def list_models():
    """List available models."""
    # Add some default models
    default_models = {
        "gpt2": {
            "name": "gpt2",
            "type": "causal_lm",
            "status": "available",
            "size": "124M",
            "created": "2024-01-01T00:00:00"
        },
        "distilgpt2": {
            "name": "distilgpt2",
            "type": "causal_lm",
            "status": "available",
            "size": "82M",
            "created": "2024-01-01T00:00:00"
        }
    }

    all_models = {**default_models, **models_db}
    return {"models": list(all_models.values())}

@app.post("/api/models/train")
async def start_training(request: TrainingRequest, background_tasks: BackgroundTasks):
    """Start model training (mock implementation)."""
    job_id = str(uuid.uuid4())

    training_jobs[job_id] = {
        "id": job_id,
        "model_name": request.model_name,
        "status": "running",
        "progress": 0,
        "created": datetime.now().isoformat(),
        "parameters": request.model_dump()
    }

    # Start mock training process
    background_tasks.add_task(mock_training_process, job_id)

    return {
        "job_id": job_id,
        "status": "started",
        "message": f"Training started for model: {request.model_name}"
    }

async def mock_training_process(job_id: str):
    """Mock training process that simulates progress."""
    try:
        job = training_jobs.get(job_id)
        if not job:
            return

        # Simulate training progress
        for progress in range(0, 101, 10):
            await asyncio.sleep(2)  # Simulate training time
            if job_id in training_jobs:
                training_jobs[job_id]["progress"] = progress
                training_jobs[job_id]["updated"] = datetime.now().isoformat()

        # Complete training
        if job_id in training_jobs:
            training_jobs[job_id]["status"] = "completed"
            training_jobs[job_id]["progress"] = 100

            # Add trained model to models database
            model_name = training_jobs[job_id]["model_name"]
            models_db[model_name] = {
                "name": model_name,
                "type": "causal_lm",
                "status": "available",
                "size": "Custom",
                "created": datetime.now().isoformat()
            }

    except Exception as e:
        logger.error(f"Training process error: {e}")
        if job_id in training_jobs:
            training_jobs[job_id]["status"] = "failed"
            training_jobs[job_id]["error"] = str(e)

@app.get("/api/training/status")
async def get_all_training_status():
    """Get all training job statuses."""
    return await list_training_jobs()

@app.get("/api/training/{job_id}")
async def get_training_status(job_id: str):
    """Get training job status."""
    if job_id not in training_jobs:
        raise HTTPException(status_code=404, detail="Training job not found")

    return training_jobs[job_id]

@app.get("/api/training")
async def list_training_jobs():
    """List all training jobs."""
    return {"jobs": list(training_jobs.values())}

@app.delete("/api/models/{model_name}")
async def delete_model(model_name: str):
    """Delete a model."""
    if model_name in models_db:
        del models_db[model_name]
        return {"message": f"Model {model_name} deleted"}
    else:
        raise HTTPException(status_code=404, detail="Model not found")

@app.get("/api/chat/sessions")
async def list_chat_sessions():
    """List chat sessions."""
    return {"sessions": list(chat_sessions.values())}

@app.get("/api/chat/sessions/{session_id}")
async def get_chat_session(session_id: str):
    """Get specific chat session."""
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return chat_sessions[session_id]

@app.delete("/api/chat/sessions/{session_id}")
async def delete_chat_session(session_id: str):
    """Delete chat session."""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return {"message": f"Session {session_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/web")
async def serve_web_interface():
    """Serve the web interface."""
    web_file = static_path / "custom-llm-studio.html"
    if web_file.exists():
        return FileResponse(web_file)
    else:
        return {"message": "Web interface not found", "expected_path": str(web_file)}

@app.get("/api/health")
async def api_health_check():
    """Health check endpoint for API consistency."""
    return await health_check()

@app.post("/api/generate")
async def generate_text(request: ChatMessage):
    """Generate text endpoint (alias for chat)."""
    return await chat_completion(request)

@app.post("/api/train")
async def start_training_short(request: TrainingRequest, background_tasks: BackgroundTasks):
    """Start model training (short endpoint alias)."""
    return await start_training(request, background_tasks)

@app.post("/api/models/{model_id}/load")
async def load_model(model_id: str):
    """Load a specific model."""
    if model_id in models_db:
        return {
            "status": "loaded",
            "model": models_db[model_id],
            "message": f"Model {model_id} loaded successfully"
        }
    else:
        raise HTTPException(status_code=404, detail="Model not found")

@app.get("/api/models/{model_id}")
async def get_model_info(model_id: str):
    """Get specific model information."""
    if model_id in models_db:
        return models_db[model_id]
    else:
        # Check default models
        default_models = {
            "gpt2": {
                "name": "gpt2",
                "type": "causal_lm",
                "status": "available",
                "size": "124M",
                "created": "2024-01-01T00:00:00"
            },
            "distilgpt2": {
                "name": "distilgpt2",
                "type": "causal_lm",
                "status": "available",
                "size": "82M",
                "created": "2024-01-01T00:00:00"
            }
        }
        if model_id in default_models:
            return default_models[model_id]
        else:
            raise HTTPException(status_code=404, detail="Model not found")

@app.get("/api/status")
async def get_system_status():
    """Get detailed system status."""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "models": len(models_db),
            "training_jobs": len(training_jobs),
            "chat_sessions": len(chat_sessions)
        },
        "endpoints": [
            "/health", "/api/health", "/api/models", "/api/chat",
            "/api/generate", "/api/training", "/docs", "/web"
        ]
    }

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await setup_mcp()
    logger.info("🚀 AI Workspace API Server started successfully")

async def setup_mcp():
    """Setup MCP integration"""
    global mcp_client
    if MCPClient:
        try:
            workspace_root = Path(__file__).parent.parent
            mcp_client = await initialize_mcp_for_api(workspace_root)
            logger.info("MCP client initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize MCP client: {e}")

# Add MCP endpoints
@app.get("/api/mcp/status")
async def get_mcp_status():
    """Get MCP integration status"""
    if not mcp_client:
        return {"status": "unavailable", "message": "MCP client not initialized"}

    try:
        health = await mcp_client.health_check()
        return {"status": "available", "health": health}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/mcp/tools")
async def get_mcp_tools():
    """Get available MCP tools"""
    if not mcp_client:
        return {"tools": {}, "message": "MCP client not available"}

    try:
        tools = await mcp_client.get_available_tools()
        return tools
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.post("/api/mcp/github/execute")
async def execute_github_tool(request: dict):
    """Execute a GitHub MCP tool"""
    if not mcp_client:
        return {"error": "MCP client not available", "status": "error"}

    tool_name = request.get("tool")
    parameters = request.get("parameters", {})

    if not tool_name:
        return {"error": "Tool name required", "status": "error"}

    try:
        result = await mcp_client.execute_github_tool(tool_name, parameters)
        return result
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/api/mcp/claude-config")
async def get_claude_config():
    """Get Claude Desktop MCP configuration"""
    if not mcp_client:
        return {"error": "MCP client not available", "status": "error"}

    try:
        config = await mcp_client.create_mcp_config_for_claude()
        return config
    except Exception as e:
        return {"error": str(e), "status": "error"}

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Custom LLM Studio API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args = parser.parse_args()

    print(f"🚀 Starting Custom LLM Studio API Server")
    print(f"📡 Server: http://{args.host}:{args.port}")
    print(f"🌐 Web UI: http://{args.host}:{args.port}/web")
    print(f"📚 API Docs: http://{args.host}:{args.port}/docs")

    uvicorn.run(
        "simple_api_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )
