#!/usr/bin/env python3
"""
Api Server module

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
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import traceback
import threading
import time

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

# Import our custom components
import sys
sys.path.append('/workspaces/semantic-kernel/ai-workspace/03-models-training')
from advanced_llm_trainer import AdvancedLLMTrainer, ModelConfig, DataConfig

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
    lora_r: int = 16
    lora_alpha: int = 32
    max_length: int = 512

class ModelInfo(BaseModel):
    name: str
    type: str
    size: str
    status: str
    created: str
    last_used: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

class TrainingStatus(BaseModel):
    job_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: float
    current_epoch: int
    total_epochs: int
    loss: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None
    logs: List[str] = []
    start_time: Optional[str] = None
    end_time: Optional[str] = None

# Global state management
app = FastAPI(title="Custom LLM Studio API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving
static_dir = Path("/workspaces/semantic-kernel/ai-workspace/05-samples-demos")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Global state
training_jobs: Dict[str, TrainingStatus] = {}
active_models: Dict[str, Any] = {}
websocket_connections: List[WebSocket] = []

class ModelManager:
    """Manage loaded models and their lifecycle."""

    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.model_configs = {}

    def load_model(self, model_name: str, model_path: Optional[str] = None) -> bool:
        """Load a model for inference."""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM

            if model_path and Path(model_path).exists():
                tokenizer = AutoTokenizer.from_pretrained(model_path)
                model = AutoModelForCausalLM.from_pretrained(model_path)
            else:
                # Load from Hugging Face Hub
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(model_name)

            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            self.models[model_name] = model
            self.tokenizers[model_name] = tokenizer

            logger.info(f"Model {model_name} loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            return False

    def unload_model(self, model_name: str) -> bool:
        """Unload a model to free memory."""
        try:
            if model_name in self.models:
                del self.models[model_name]
            if model_name in self.tokenizers:
                del self.tokenizers[model_name]
            if model_name in self.model_configs:
                del self.model_configs[model_name]

            # Force garbage collection
            import gc
            gc.collect()
            if hasattr(torch, 'cuda') and torch.cuda.is_available():
                torch.cuda.empty_cache()

            logger.info(f"Model {model_name} unloaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to unload model {model_name}: {str(e)}")
            return False

    def generate_text(self, model_name: str, prompt: str, **kwargs) -> str:
        """Generate text using a loaded model."""
        if model_name not in self.models:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not loaded")

        try:
            import torch

            model = self.models[model_name]
            tokenizer = self.tokenizers[model_name]

            # Tokenize input
            inputs = tokenizer.encode(prompt, return_tensors="pt")

            # Generate
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=kwargs.get('max_tokens', 150) + len(inputs[0]),
                    temperature=kwargs.get('temperature', 0.7),
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    attention_mask=torch.ones_like(inputs)
                )

            # Decode only the new tokens
            generated_text = tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
            return generated_text

        except Exception as e:
            logger.error(f"Generation failed for model {model_name}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

# Initialize model manager
model_manager = ModelManager()

class TrainingManager:
    """Manage training jobs and their lifecycle."""

    def __init__(self):
        self.active_jobs = {}

    async def start_training(self, job_id: str, request: TrainingRequest) -> None:
        """Start a training job in the background."""
        try:
            # Update job status
            training_jobs[job_id].status = "running"
            training_jobs[job_id].start_time = datetime.now().isoformat()

            # Notify WebSocket clients
            await self.broadcast_training_update(job_id)

            # Create model and data configs
            model_config = ModelConfig(
                model_name=request.model_name,
                num_epochs=request.epochs,
                learning_rate=request.learning_rate,
                batch_size=request.batch_size,
                use_lora=request.use_lora,
                lora_r=request.lora_r,
                lora_alpha=request.lora_alpha,
                max_length=request.max_length
            )

            data_config = DataConfig()
            if request.dataset_path:
                data_config.data_path = request.dataset_path

            # Initialize trainer
            trainer = AdvancedLLMTrainer(model_config, data_config)

            # Create training data if provided
            if request.training_data:
                await self.prepare_training_data(request.training_data, data_config.data_path)

            # Start training with progress callback
            def progress_callback(epoch: int, total_epochs: int, loss: float, metrics: Dict):
                training_jobs[job_id].current_epoch = epoch
                training_jobs[job_id].total_epochs = total_epochs
                training_jobs[job_id].loss = loss
                training_jobs[job_id].metrics = metrics
                training_jobs[job_id].progress = (epoch / total_epochs) * 100

                # Create async task to broadcast update
                asyncio.create_task(self.broadcast_training_update(job_id))

            # Train the model
            model_path = trainer.train_model(progress_callback=progress_callback)

            # Update final status
            training_jobs[job_id].status = "completed"
            training_jobs[job_id].end_time = datetime.now().isoformat()
            training_jobs[job_id].progress = 100

            await self.broadcast_training_update(job_id)

            logger.info(f"Training job {job_id} completed successfully")

        except Exception as e:
            logger.error(f"Training job {job_id} failed: {str(e)}")
            training_jobs[job_id].status = "failed"
            training_jobs[job_id].end_time = datetime.now().isoformat()
            training_jobs[job_id].logs.append(f"Error: {str(e)}")

            await self.broadcast_training_update(job_id)

    async def prepare_training_data(self, training_data: List[Dict], data_path: str):
        """Prepare training data from provided samples."""
        import json

        os.makedirs(data_path, exist_ok=True)

        # Split data into train/eval
        train_size = int(0.8 * len(training_data))
        train_data = training_data[:train_size]
        eval_data = training_data[train_size:]

        # Save as JSONL files
        with open(f"{data_path}/train.jsonl", "w") as f:
            for item in train_data:
                f.write(json.dumps(item) + "\n")

        with open(f"{data_path}/eval.jsonl", "w") as f:
            for item in eval_data:
                f.write(json.dumps(item) + "\n")

    async def broadcast_training_update(self, job_id: str):
        """Broadcast training updates to all connected WebSocket clients."""
        if job_id in training_jobs:
            message = {
                "type": "training_update",
                "job_id": job_id,
                "status": training_jobs[job_id].dict()
            }

            # Send to all connected WebSocket clients
            disconnected = []
            for websocket in websocket_connections:
                try:
                    await websocket.send_text(json.dumps(message))
                except:
                    disconnected.append(websocket)

            # Remove disconnected clients
            for ws in disconnected:
                websocket_connections.remove(ws)

# Initialize training manager
training_manager = TrainingManager()

# API Endpoints

@app.get("/")
async def root():
    """Serve the main HTML interface."""
    html_file = static_dir / "custom-llm-studio.html"
    if html_file.exists():
        return FileResponse(html_file)
    return {"message": "Custom LLM Studio API", "status": "running"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_models": list(model_manager.models.keys()),
        "training_jobs": len([j for j in training_jobs.values() if j.status == "running"])
    }

@app.post("/api/chat")
async def chat(request: ChatMessage):
    """Generate text using a loaded model."""
    try:
        # Load model if not already loaded
        if request.model not in model_manager.models:
            success = model_manager.load_model(request.model)
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to load model {request.model}")

        # Generate response
        prompt = request.message
        if request.system:
            prompt = f"System: {request.system}\nUser: {request.message}\nAssistant:"

        response = model_manager.generate_text(
            request.model,
            prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        return {
            "response": response,
            "model": request.model,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/models/load")
async def load_model(model_name: str, model_path: Optional[str] = None):
    """Load a model for inference."""
    try:
        success = model_manager.load_model(model_name, model_path)
        if success:
            return {"status": "success", "message": f"Model {model_name} loaded successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to load model {model_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/models/unload")
async def unload_model(model_name: str):
    """Unload a model to free memory."""
    try:
        success = model_manager.unload_model(model_name)
        if success:
            return {"status": "success", "message": f"Model {model_name} unloaded successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to unload model {model_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models")
async def list_models():
    """List all available models."""
    try:
        models = []

        # Get loaded models
        for name in model_manager.models.keys():
            models.append(ModelInfo(
                name=name,
                type="loaded",
                size="unknown",
                status="active",
                created=datetime.now().isoformat()
            ))

        # Get saved models from filesystem
        models_dir = Path("/workspaces/semantic-kernel/ai-workspace/models")
        if models_dir.exists():
            for model_dir in models_dir.iterdir():
                if model_dir.is_dir():
                    models.append(ModelInfo(
                        name=model_dir.name,
                        type="saved",
                        size="unknown",
                        status="available",
                        created=datetime.fromtimestamp(model_dir.stat().st_ctime).isoformat()
                    ))

        return {"models": models}

    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/train")
async def start_training(request: TrainingRequest, background_tasks: BackgroundTasks):
    """Start a model training job."""
    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())

        # Create training status
        training_jobs[job_id] = TrainingStatus(
            job_id=job_id,
            status="pending",
            progress=0,
            current_epoch=0,
            total_epochs=request.epochs
        )

        # Start training in background
        background_tasks.add_task(training_manager.start_training, job_id, request)

        return {"job_id": job_id, "status": "Training job started"}

    except Exception as e:
        logger.error(f"Error starting training: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/train/{job_id}")
async def get_training_status(job_id: str):
    """Get the status of a training job."""
    if job_id not in training_jobs:
        raise HTTPException(status_code=404, detail="Training job not found")

    return training_jobs[job_id]

@app.get("/api/train")
async def list_training_jobs():
    """List all training jobs."""
    return {"jobs": list(training_jobs.values())}

@app.delete("/api/train/{job_id}")
async def cancel_training(job_id: str):
    """Cancel a training job."""
    if job_id not in training_jobs:
        raise HTTPException(status_code=404, detail="Training job not found")

    # TODO: Implement actual job cancellation
    training_jobs[job_id].status = "cancelled"
    training_jobs[job_id].end_time = datetime.now().isoformat()

    return {"status": "Training job cancelled"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file for training data."""
    try:
        upload_dir = Path("/workspaces/semantic-kernel/ai-workspace/uploads")
        upload_dir.mkdir(exist_ok=True)

        file_path = upload_dir / file.filename

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return {
            "filename": file.filename,
            "path": str(file_path),
            "size": len(content),
            "status": "uploaded"
        }

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time updates
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    websocket_connections.append(websocket)

    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()

            # Echo back for testing
            await websocket.send_text(f"Echo: {data}")

    except WebSocketDisconnect:
        websocket_connections.remove(websocket)

if __name__ == "__main__":
    # Import torch here to avoid issues if not available
    try:
        import torch
        logger.info(f"PyTorch available: {torch.__version__}")
        if torch.cuda.is_available():
            logger.info(f"CUDA available with {torch.cuda.device_count()} device(s)")
    except ImportError:
        logger.warning("PyTorch not available - some features may be limited")

    # Start the server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
