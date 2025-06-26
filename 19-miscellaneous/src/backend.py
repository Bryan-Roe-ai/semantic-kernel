#!/usr/bin/env python3
"""
import asyncio
Backend module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Save as backend.py and run with: uvicorn backend:app --reload

from fastapi import FastAPI, Query, File, UploadFile
from typing import Annotated, List, Dict, Any, Optional
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
# removed unused import
from pydantic import BaseModel
import os
import requests
import json
import glob
import importlib.util
import traceback
import sys
import inspect
import shutil
from datetime import datetime

# Try to import PIL for image analysis, but don't fail if not available
try:
    from PIL import Image
    pil_available = True
except ImportError:
    pil_available = False

app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.getcwd()
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

class FileWriteRequest(BaseModel):
    path: str
    content: str

class FileDeleteRequest(BaseModel):
    path: str

class ChatRequest(BaseModel):
    message: str
    system: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

LM_STUDIO_URL = os.environ.get("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")

@app.get("/ping")
def ping() -> Dict[str, str]:
    return {"status": "OK"}

# --- Plugin Loading ---
sys.path.insert(0, PLUGINS_DIR)
python_plugins: Dict[str, Dict[str, Any]] = {}

def load_python_plugins() -> None:
    global python_plugins
    plugin_files = glob.glob(os.path.join(PLUGINS_DIR, "*.py"))
    if not os.path.exists(PLUGINS_DIR):
        try:
            os.makedirs(PLUGINS_DIR, exist_ok=True)
        except Exception as e:
            print(f"Failed to create plugins directory: {str(e)}")
            return
    python_plugins = {}
    for plugin_file in plugin_files:
        module_name = os.path.basename(plugin_file).replace(".py", "")
        try:
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                plugin_found = False
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and name.endswith("Functions"):
                        try:
                            plugin_name = name.replace("Functions", "").lower()
                            instance = obj()
                            python_plugins[plugin_name] = {
                                "instance": instance,
                                "methods": {}
                            }
                            for _, method in inspect.getmembers(instance):
                                if hasattr(method, "__sk_function_name__"):
                                    function_name = getattr(method, "__sk_function_name__")
                                    function_desc = getattr(method, "__sk_function_description__", "")
                                    python_plugins[plugin_name]["methods"][function_name] = {
                                        "method": method,
                                        "description": function_desc,
                                        "signature": inspect.signature(method)
                                    }
                            plugin_found = True
                        except Exception as inst_error:
                            print(f"Error instantiating plugin class {name}: {str(inst_error)}")
                            traceback.print_exc()
                if not plugin_found:
                    print(f"No valid plugin classes found in {module_name}")
        except Exception as e:
            print(f"Error loading plugin {module_name}: {str(e)}")
            traceback.print_exc()

load_python_plugins()

@app.get("/api/plugins")
def get_plugins() -> Any:
    plugins: List[Dict[str, str]] = []
    functions: List[Dict[str, Any]] = []
    # Directory-based plugins
    if os.path.exists(PLUGINS_DIR):
        for plugin_dir in glob.glob(os.path.join(PLUGINS_DIR, "*")):
            if not os.path.isdir(plugin_dir):
                continue
            plugin_name = os.path.basename(plugin_dir)
            plugin_id = plugin_name.lower()
            plugins.append({"id": plugin_id, "name": plugin_name, "type": "directory"})
            for function_dir in glob.glob(os.path.join(plugin_dir, "*")):
                if not os.path.isdir(function_dir):
                    continue
                if os.path.exists(os.path.join(function_dir, "skprompt.txt")):
                    function_name = os.path.basename(function_dir)
                    function_id = f"{plugin_id}.{function_name.lower()}"
                    description = ""
                    config_path = os.path.join(function_dir, "config.json")
                    if os.path.exists(config_path):
                        try:
                            with open(config_path, "r", encoding="utf-8") as config_file:
                                config = json.load(config_file)
                                description = config.get("description", "")
                        except:
                            pass
                    functions.append({
                        "id": function_id,
                        "name": function_name,
                        "plugin": plugin_id,
                        "description": description,
                        "type": "directory"
                    })
    # Python plugins
    for plugin_name, plugin_data in python_plugins.items():
        plugins.append({"id": plugin_name, "name": plugin_name.capitalize(), "type": "python"})
        for function_name, function_info in plugin_data["methods"].items():
            function_id = f"{plugin_name}.{function_name.lower()}"
            functions.append({
                "id": function_id,
                "name": function_name,
                "plugin": plugin_name,
                "description": function_info["description"],
                "type": "python"
            })
    return {"plugins": plugins, "functions": functions}

@app.post("/api/run_plugin")
def run_plugin(plugin_id: str, function_id: str, input_text: str) -> Any:
    if not plugin_id or not function_id:
        return {"error": "Missing plugin_id or function_id"}
    parts = function_id.split(".")
    if len(parts) != 2:
        return {"error": "Invalid function_id format"}
    plugin_name, function_name = parts
    function_dir = os.path.join(PLUGINS_DIR, plugin_name, function_name)
    prompt_file = os.path.join(function_dir, "skprompt.txt")
    if not os.path.exists(prompt_file):
        return {"error": "Plugin function not found"}
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_template = f.read()
        prompt = prompt_template.replace("{{$input}}", input_text)
        payload = {
            "model": "microsoft/phi-4-mini-reasoning",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.0,
        }
        lm_response = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
        lm_response.raise_for_status()
        data = lm_response.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "[No response]")
        return {"result": reply}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/run_python")
def run_python_plugin(plugin_id: str, function_id: str, input_text: str, param2: Optional[str] = None) -> Any:
    parts = function_id.split(".")
    if len(parts) != 2:
        return {"error": "Invalid function_id format"}
    plugin_name, function_name = parts
    if plugin_name not in python_plugins:
        return {"error": f"Plugin {plugin_name} not found"}
    if function_name not in python_plugins[plugin_name]["methods"]:
        return {"error": f"Function {function_name} not found in plugin {plugin_name}"}
    try:
        method = python_plugins[plugin_name]["methods"][function_name]["method"]
        signature = python_plugins[plugin_name]["methods"][function_name]["signature"]
        kwargs: Dict[str, Any] = {}
        param_names = list(signature.parameters.keys())
        if len(param_names) == 1:
            kwargs[param_names[0]] = input_text
        elif len(param_names) == 2:
            kwargs[param_names[0]] = input_text
            kwargs[param_names[1]] = param2 or ""
        result = method(**kwargs)
        return {"result": result}
    except Exception as e:
        return {"error": f"Error executing function: {str(e)}"}

# --- File Operations ---
@app.get("/files/list")
def list_files() -> List[str]:
    files: List[str] = []
    for root, _, filenames in os.walk(BASE_DIR):
        for f in filenames:
            rel_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
            files.append(rel_path)
    return files

@app.get("/files/read")
def read_file(path: Annotated[str, Query(...)]) -> Any:
    abs_path = os.path.abspath(os.path.join(BASE_DIR, path))
    if not abs_path.startswith(BASE_DIR):
        return {"error": "Invalid path"}
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

@app.post("/files/write")
def write_file(req: FileWriteRequest) -> Any:
    abs_path = os.path.abspath(os.path.join(BASE_DIR, req.path))
    if not abs_path.startswith(BASE_DIR):
        return {"error": "Invalid path"}
    try:
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(req.content)
        return {"status": "OK"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/files/delete")
def delete_file(req: FileDeleteRequest) -> Any:
    abs_path = os.path.abspath(os.path.join(BASE_DIR, req.path))
    if not abs_path.startswith(BASE_DIR):
        return {"error": "Invalid path"}
    try:
        os.remove(abs_path)
        return {"status": "OK"}
    except Exception as e:
        return {"error": str(e)}

# --- File Analyzer ---
try:
    from file_analyzer import FileAnalyzer
    analyzer_available = True
except ImportError:
    analyzer_available = False
    class FileAnalyzer:
        @staticmethod
        def analyze_file(file_path: str) -> Dict[str, Any]:
            return {"error": "File analyzer module not available"}

def auto_analyze_file(filename: str) -> Dict[str, Any]:
    try:
        file_path = os.path.join(UPLOADS_DIR, filename)
        if not os.path.exists(file_path):
            return {"error": f"File not found: {filename}"}
        if not analyzer_available:
            return {"type": "unknown", "summary": f"File: {filename}", "details": {"info": "File analyzer not available"}}
        return FileAnalyzer.analyze_file(file_path)
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

# --- Upload/Download/Analyze Endpoints ---
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)) -> Any:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOADS_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_size = os.path.getsize(file_path)
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        elif file_size > 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size} bytes"
        analysis = auto_analyze_file(filename)
        return {
            "filename": filename,
            "originalName": file.filename,
            "size": size_str,
            "analysis": analysis
        }
    except Exception as e:
        return {"error": f"Failed to upload file: {str(e)}"}

@app.get("/api/files")
def list_uploaded_files() -> Any:
    try:
        if not os.path.exists(UPLOADS_DIR):
            return {"files": []}
        files: List[Dict[str, str]] = []
        for filename in os.listdir(UPLOADS_DIR):
            file_path = os.path.join(UPLOADS_DIR, filename)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                if file_size > 1024 * 1024:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                elif file_size > 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size} bytes"
                files.append({
                    "name": filename,
                    "size": size_str,
                    "path": f"uploads/{filename}"
                })
        return {"files": files}
    except Exception as e:
        return {"error": f"Failed to list files: {str(e)}"}

@app.get("/api/download/{filename}")
def download_file(filename: str) -> Any:
    file_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")

@app.get("/api/analyze/{filename}")
def analyze_file_endpoint(filename: str) -> Any:
    file_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    analysis = auto_analyze_file(filename)
    return analysis

# --- Chat Endpoint ---
@app.post("/api/chat")
def chat_endpoint(req: ChatRequest) -> Any:
    if not req.message or not req.message.strip():
        return {"reply": "Please enter a message."}
    payload = {
        "model": req.model or "microsoft/phi-4-mini-reasoning",
        "messages": [
            {"role": "user", "content": req.message}
        ],
        "max_tokens": req.max_tokens or 500,
        "temperature": req.temperature if req.temperature is not None else 0.7,
    }
    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "[No response]")
        return {"reply": reply}
    except Exception:
        return {"reply": f"[AI unavailable] You said: {req.message}"}