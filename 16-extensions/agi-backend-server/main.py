#!/usr/bin/env python3
"""
AGI Backend Server for Semantic Kernel Integration
This server provides RESTful API endpoints for AGI file operations.

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Add semantic kernel path
sys.path.append('/workspaces/semantic-kernel/python')

# Models for API
class FileTask(BaseModel):
    file_path: str
    operation: str
    content: Optional[str] = None
    target_line: Optional[int] = None
    backup: bool = True

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

# Create FastAPI app
app = FastAPI(
    title="AGI Backend Server",
    description="Backend API for AGI file operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("agi_backend.log"),
    ],
)

logger = logging.getLogger("agi_backend")

# Global task storage
tasks = {}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/file/task", response_model=TaskResponse)
async def create_file_task(task: FileTask, background_tasks: BackgroundTasks):
    """Create a new file operation task"""
    import uuid
    
    task_id = str(uuid.uuid4())[:8]
    
    # Store task
    tasks[task_id] = {
        "task": task.dict(),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    # Process task in background
    background_tasks.add_task(process_file_task, task_id, task)
    
    return {
        "task_id": task_id,
        "status": "accepted",
        "message": f"Task {task_id} has been queued"
    }

@app.get("/file/task/{task_id}", response_model=Dict[str, Any])
async def get_task_status(task_id: str):
    """Get status of a specific task"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks[task_id]

@app.get("/file/tasks", response_model=Dict[str, Any])
async def list_tasks():
    """List all tasks"""
    return {
        "tasks": tasks,
        "total": len(tasks),
        "pending": sum(1 for t in tasks.values() if t["status"] == "pending"),
        "completed": sum(1 for t in tasks.values() if t["status"] == "completed"),
        "failed": sum(1 for t in tasks.values() if t["status"] == "failed")
    }

@app.get("/file/analyze", response_model=Dict[str, Any])
async def analyze_file(path: str):
    """Analyze a file"""
    file_path = Path(path)
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        analysis = analyze_file_content(file_path)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def analyze_file_content(file_path: Path) -> Dict[str, Any]:
    """Analyze file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic file analysis
        analysis = {
            "exists": True,
            "size": len(content),
            "lines": len(content.splitlines()),
            "file_type": file_path.suffix,
            "encoding": "utf-8",
            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        }

        return analysis

    except Exception as e:
        logger.error(f"Error analyzing file {file_path}: {e}")
        return {"exists": True, "error": str(e)}

async def process_file_task(task_id: str, task: FileTask):
    """Process a file task in the background"""
    logger.info(f"Processing task {task_id}: {task.operation} on {task.file_path}")
    
    try:
        file_path = Path(task.file_path)
        
        # Perform basic safety checks
        if not is_safe_operation(file_path, task.operation):
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["error"] = "Operation not allowed for safety reasons"
            return
        
        # Execute operation
        if task.operation == "create":
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(task.content or "")
                
        elif task.operation == "update":
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(task.content or "")
                
        elif task.operation == "append":
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(task.content or "")
                
        elif task.operation == "delete":
            if file_path.exists():
                file_path.unlink()
        else:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["error"] = f"Unknown operation: {task.operation}"
            return
            
        # Update task status
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["completed_at"] = datetime.now().isoformat()
        logger.info(f"Task {task_id} completed successfully")
            
    except Exception as e:
        logger.error(f"Task {task_id} failed: {e}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)

def is_safe_operation(file_path: Path, operation: str) -> bool:
    """Check if file operation is safe"""
    # Define safe directories
    safe_directories = [
        "/workspaces/semantic-kernel/python",
        "/workspaces/semantic-kernel/dotnet",
        "/workspaces/semantic-kernel/samples",
        "/workspaces/semantic-kernel/notebooks",
        "/workspaces/semantic-kernel/scripts",
        "/workspaces/semantic-kernel/09-agi-development"
    ]
    
    # Check if file is in safe directories
    file_str = str(file_path.absolute())
    in_safe_dir = any(file_str.startswith(safe_dir) for safe_dir in safe_directories)
    
    if not in_safe_dir:
        return False
        
    # Check for restricted file patterns
    restricted_files = [".git", ".env", "secrets", "credentials", "password"]
    for restricted in restricted_files:
        if restricted.lower() in str(file_path).lower():
            return False
            
    return True

if __name__ == "__main__":
    # Start server
    print("🚀 Starting AGI Backend Server on http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
