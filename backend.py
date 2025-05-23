# Save as backend.py and run with: uvicorn backend:app --reload

from fastapi import FastAPI, Query, File, UploadFile, Form
from typing import Annotated
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import requests
from typing import List, Dict, Any, Optional
import json
import glob
import importlib.util
import traceback
import sys
import inspect
import shutil
import base64
from datetime import datetime

app: FastAPI = FastAPI()
app.add_middleware(  # type: ignore
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
def ping():
    return {"status": "OK"}

# Import Python plugins
sys.path.insert(0, os.path.join(BASE_DIR, "plugins"))
PYTHON_PLUGINS = {}

def load_python_plugins():
    """Dynamically load Python plugin modules"""
    global PYTHON_PLUGINS
    plugin_files = glob.glob(os.path.join(BASE_DIR, "plugins", "*.py"))
    
    for plugin_file in plugin_files:
        module_name = os.path.basename(plugin_file).replace(".py", "")
        
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find plugin classes in the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and name.endswith("Functions"):
                        # Store the class as a plugin
                        plugin_name = name.replace("Functions", "").lower() 
                        instance = obj()
                        PYTHON_PLUGINS[plugin_name] = {
                            "instance": instance,
                            "methods": {}
                        }
                        
                        # Find methods with kernel_function decorator
                        for method_name, method in inspect.getmembers(instance):
                            if hasattr(method, "__sk_function_name__"):
                                function_name = getattr(method, "__sk_function_name__")
                                function_desc = getattr(method, "__sk_function_description__", "")
                                
                                PYTHON_PLUGINS[plugin_name]["methods"][function_name] = {
                                    "method": method,
                                    "description": function_desc,
                                    "signature": inspect.signature(method)
                                }
                print(f"Loaded plugin: {plugin_name} with {len(PYTHON_PLUGINS[plugin_name]['methods'])} functions")
                
        except Exception as e:
            print(f"Error loading plugin {module_name}: {str(e)}")
            traceback.print_exc()

# Load plugins on startup
load_python_plugins()

@app.get("/api/plugins")
def get_plugins():
    # Include both directory-based plugins and Python plugins
    plugins = []
    functions = []
    
    # Get directory-based plugins first
    if os.path.exists(PLUGINS_DIR):
        for plugin_dir in glob.glob(os.path.join(PLUGINS_DIR, "*")):
            if not os.path.isdir(plugin_dir):
                continue
                
            plugin_name = os.path.basename(plugin_dir)
            plugin_id = plugin_name.lower()
            plugins.append({"id": plugin_id, "name": plugin_name, "type": "directory"})
            
            # Find all functions (subdirectories with skprompt.txt)
            for function_dir in glob.glob(os.path.join(plugin_dir, "*")):
                if not os.path.isdir(function_dir):
                    continue
                    
                if os.path.exists(os.path.join(function_dir, "skprompt.txt")):
                    function_name = os.path.basename(function_dir)
                    function_id = f"{plugin_id}.{function_name.lower()}"
                    
                    # Try to get description from config.json
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
    
    # Now add Python plugins
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
def run_plugin(plugin_id: str, function_id: str, input_text: str):
    if not plugin_id or not function_id:
        return {"error": "Missing plugin_id or function_id"}
    
    # Parse function ID to get plugin and function names
    parts = function_id.split(".")
    if len(parts) != 2:
        return {"error": "Invalid function_id format"}
    
    plugin_name = parts[0]
    function_name = parts[1]
    
    # Check if the function exists
    function_dir = os.path.join(PLUGINS_DIR, plugin_name, function_name)
    prompt_file = os.path.join(function_dir, "skprompt.txt")
    
    if not os.path.exists(prompt_file):
        return {"error": "Plugin function not found"}
    
    try:
        # Read the prompt template
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_template = f.read()
        
        # Simple template replacement (in a real app, use a proper template engine)
        prompt = prompt_template.replace("{{$input}}", input_text)
        
        # Send to LM Studio
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
def run_python_plugin(plugin_id: str, function_id: str, input_text: str, param2: Optional[str] = None):
    """Run a Python plugin function"""
    # Parse function ID to get plugin and function names
    parts = function_id.split(".")
    if len(parts) != 2:
        return {"error": "Invalid function_id format"}
    
    plugin_name = parts[0]
    function_name = parts[1]
    
    # Check if plugin and function exist
    if plugin_name not in PYTHON_PLUGINS:
        return {"error": f"Plugin {plugin_name} not found"}
        
    if function_name not in PYTHON_PLUGINS[plugin_name]["methods"]:
        return {"error": f"Function {function_name} not found in plugin {plugin_name}"}
    
    try:
        # Get the method and its signature
        method = PYTHON_PLUGINS[plugin_name]["methods"][function_name]["method"]
        signature = PYTHON_PLUGINS[plugin_name]["methods"][function_name]["signature"]
        
        # Prepare arguments based on signature
        kwargs = {}
        param_names = list(signature.parameters.keys())
        
        if len(param_names) == 1:
            # Only one parameter, use input_text
            kwargs[param_names[0]] = input_text
        elif len(param_names) == 2:
            # Two parameters, use input_text and param2
            kwargs[param_names[0]] = input_text
            kwargs[param_names[1]] = param2 or ""
        
        # Call the method with the appropriate arguments
        result = method(**kwargs)
        return {"result": result}
        
    except Exception as e:
        return {"error": f"Error executing function: {str(e)}"}

@app.get("/files/list")  # type: ignore
def list_files() -> List[str]:
    files: List[str] = []
    for root, _, filenames in os.walk(BASE_DIR):
        for f in filenames:
            rel_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
            files.append(rel_path)
    return files

@app.get("/files/read")  # type: ignore
def read_file(path: Annotated[str, Query(...)]) -> Dict[str, Any]:
    abs_path = os.path.abspath(os.path.join(BASE_DIR, path))
    if not abs_path.startswith(BASE_DIR):
        return {"error": "Invalid path"}
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

@app.post("/files/write")  # type: ignore
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

@app.post("/files/delete")  # type: ignore
def delete_file(req: FileDeleteRequest) -> Dict[str, str]:
    abs_path = os.path.abspath(os.path.join(BASE_DIR, req.path))
    if not abs_path.startswith(BASE_DIR):
        return {"error": "Invalid path"}
    try:
        os.remove(abs_path)
        return {"status": "OK"}
    except Exception as e:
        return {"error": str(e)}

# Create uploads directory if it doesn't exist
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file uploads"""
    try:
        # Create a unique filename to prevent overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOADS_DIR, filename)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return the file info
        file_size = os.path.getsize(file_path)
        size_str = f"{file_size} bytes"
        if file_size > 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
            
        return {"filename": filename, "originalName": file.filename, "size": size_str}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to upload file: {str(e)}"}
        )
        
@app.get("/api/files")
def list_uploaded_files():
    """List all uploaded files"""
    try:
        if not os.path.exists(UPLOADS_DIR):
            return {"files": []}
            
        files = []
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
def download_file(filename: str):
    """Download a file from the uploads directory"""
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

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest) -> Dict[str, str]:
    # Build messages array for LM Studio
    messages: List[Dict[str, str]] = []
    if req.system:
        messages.append({"role": "system", "content": req.system})
    messages.append({"role": "user", "content": req.message})
    
    # Default to a simple model if not specified
    model = req.model or "microsoft/phi-4-mini-reasoning"
    
    # Compose payload for LM Studio
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": req.max_tokens if req.max_tokens is not None else 500,  # Use reasonable default
        "temperature": req.temperature if req.temperature is not None else 0.7,
        "stream": req.stream if req.stream is not None else False,
    }
    
    # Only POST to LM_STUDIO_URL, do not append /api/chat
    try:
        print(f"Sending request to LM Studio: {payload}")
        lm_response = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
        lm_response.raise_for_status()
        data = lm_response.json()
        
        # Extract the AI's reply from the response
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "[No response]")
        
        # Log the reply for debugging
        print(f"Received reply from LM Studio: {reply[:100]}...")
        
        return {"reply": reply}
    except Exception as e:
        error_msg = f"[LM Studio error: {str(e)}]"
        print(f"Error: {error_msg}")
        return {"reply": error_msg}