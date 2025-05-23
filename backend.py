# Save as backend.py and run with: uvicorn backend:app --reload

from fastapi import FastAPI, Query, File, UploadFile
from typing import Annotated, List, Dict, Any, Optional, Union
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from fastapi.responses import JSONResponse
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
import base64
from datetime import datetime
import csv
import mimetypes

# Try to import PIL for image analysis, but don't fail if not available
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.getcwd()  # Or set to your workspace root
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")

class FileWriteRequest(BaseModel):
    path: str
    content: str

class FileDeleteRequest(BaseModel):
    path: str

class ChatRequest(BaseModel):
    message: str
    system: Optional[str] = None  # Optional system prompt
    model: Optional[str] = None  # Optional model override
    temperature: Optional[float] = None  # Optional temperature override
    max_tokens: Optional[int] = None  # Optional max_tokens override
    stream: Optional[bool] = False  # Optional stream flag

# LM Studio API endpoint (do NOT append /api/chat)
LM_STUDIO_URL = os.environ.get("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")

@app.get("/ping")
def ping() -> Dict[str, str]:
    return {"status": "OK"}

# Import Python plugins
def load_python_plugins() -> None:
    global PYTHON_PLUGINS
    plugin_files = glob.glob(os.path.join(BASE_DIR, "plugins", "*.py"))
    PYTHON_PLUGINS.clear()
    for plugin_file in plugin_files:
        module_name = os.path.basename(plugin_file).replace(".py", "")
        try:
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and name.endswith("Functions"):
                        try:
                            plugin_name = name.replace("Functions", "").lower()
                            instance = obj()
                            PYTHON_PLUGINS[plugin_name] = {
                                "instance": instance,
                                "methods": {}
                            }
                            for method_name, method in inspect.getmembers(instance):
                                if hasattr(method, "__sk_function_name__"):
                                    function_name = getattr(method, "__sk_function_name__")
                                    function_desc = getattr(method, "__sk_function_description__", "")
                                    PYTHON_PLUGINS[plugin_name]["methods"][function_name] = {
                                        "method": method,
                                        "description": function_desc,
                                        "signature": inspect.signature(method)
                                    }
                        except Exception as inst_error:
                            print(f"Error instantiating plugin class {name}: {str(inst_error)}")
                            traceback.print_exc()
        except Exception as e:
            print(f"Error loading plugin {module_name}: {str(e)}")
            traceback.print_exc()

PYTHON_PLUGINS: Dict[str, Dict[str, Any]] = {}
load_python_plugins()

@app.get("/api/plugins")
def get_plugins() -> Dict[str, Union[List[Dict[str, str]], List[Dict[str, Union[str, Dict[str, str]]]]]]:
    plugins: List[Dict[str, str]] = []
    functions: List[Dict[str, Union[str, Dict[str, str]]]] = []
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
    for plugin_name, plugin_data in PYTHON_PLUGINS.items():
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
def run_plugin(plugin_id: str, function_id: str, input_text: str) -> Dict[str, Union[str, Dict[str, str]]]:
    if not plugin_id or not function_id:
        return {"error": "Missing plugin_id or function_id"}
    parts = function_id.split(".")
    if len(parts) != 2:
        return {"error": "Invalid function_id format"}
    plugin_name = parts[0]
    function_name = parts[1]
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
def run_python_plugin(plugin_id: str, function_id: str, input_text: str, param2: Optional[str] = None) -> Dict[str, Union[str, Dict[str, str]]]:
    parts = function_id.split(".")
    if len(parts) != 2:
        return {"error": "Invalid function_id format"}
    plugin_name = parts[0]
    function_name = parts[1]
    if plugin_name not in PYTHON_PLUGINS:
        return {"error": f"Plugin {plugin_name} not found"}
    if function_name not in PYTHON_PLUGINS[plugin_name]["methods"]:
        return {"error": f"Function {function_name} not found in plugin {plugin_name}"}
    try:
        method = PYTHON_PLUGINS[plugin_name]["methods"][function_name]["method"]
        signature = PYTHON_PLUGINS[plugin_name]["methods"][function_name]["signature"]
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

@app.get("/files/list")
def list_files() -> List[str]:
    files: List[str] = []
    for root, _, filenames in os.walk(BASE_DIR):
        for f in filenames:
            rel_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
            files.append(rel_path)
    return files

@app.get("/files/read")
def read_file(path: Annotated[str, Query(...)]) -> Dict[str, Union[str, Dict[str, str]]]:
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
def write_file(req: FileWriteRequest) -> Dict[str, str]:
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
def delete_file(req: FileDeleteRequest) -> Dict[str, str]:
    abs_path = os.path.abspath(os.path.join(BASE_DIR, req.path))
    if not abs_path.startswith(BASE_DIR):
        return {"error": "Invalid path"}
    try:
        os.remove(abs_path)
        return {"status": "OK"}
    except Exception as e:
        return {"error": str(e)}

# Import the file analyzer module
try:
    from file_analyzer import FileAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False
    class FileAnalyzer:
        @staticmethod
        def analyze_file(file_path: str) -> Dict[str, Union[str, Dict[str, str]]]:
            return {"error": "File analyzer module not available"}

UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

def auto_analyze_file(filename: str) -> Dict[str, Union[str, Dict[str, str]]]:
    try:
        file_path = os.path.join(UPLOADS_DIR, filename)
        if not os.path.exists(file_path):
            return {"error": f"File not found: {filename}"}
        if not ANALYZER_AVAILABLE:
            return {"type": "unknown", "summary": f"File: {filename}", "details": {"info": "File analyzer not available"}}
        return FileAnalyzer.analyze_file(file_path)
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, Union[str, Dict[str, str]]]:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOADS_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_size = os.path.getsize(file_path)
        size_str = f"{file_size} bytes"
        if file_size > 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        analysis = auto_analyze_file(filename)
        return {
            "filename": filename,
            "originalName": file.filename,
            "size": size_str,
            "analysis": analysis
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to upload file: {str(e)}"}
        )

@app.get("/api/files")
def list_uploaded_files() -> Dict[str, List[Dict[str, str]]]:
    try:
        if not os.path.exists(UPLOADS_DIR):
            return {"files": []}
        files: List[Dict[str, str]] = []
        for filename in os.listdir(UPLOADS_DIR):
            file_path = os.path.join(UPLOADS_DIR, filename)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                size_str = f"{file_size} bytes"
                if file_size > 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                if file_size > 1024 * 1024:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                files.append({
                    "name": filename,
                    "size": size_str,
                    "path": f"uploads/{filename}"
                })
        return {"files": files}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to list files: {str(e)}"}
        )

@app.get("/api/download/{filename}")
def download_file(filename: str) -> Union[FileResponse, JSONResponse]:
    file_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404,
            content={"error": "File not found"}
        )
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

@app.get("/api/analyze/{filename}")
def analyze_file_endpoint(filename: str) -> Dict[str, Union[str, Dict[str, str]]]:
    file_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404,
            content={"error": "File not found"}
        )
    analysis = auto_analyze_file(filename)
    return analysis

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest) -> Dict[str, str]:
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
    except Exception as e:
        return {"reply": f"[AI unavailable] You said: {req.message}"}