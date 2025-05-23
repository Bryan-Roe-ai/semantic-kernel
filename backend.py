# Save as backend.py and run with: uvicorn backend:app --reload

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from typing import List, Dict, Any, Optional

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.getcwd()  # Or set to your workspace root

class FileWriteRequest(BaseModel):
    path: str
    content: str

class FileDeleteRequest(BaseModel):
    path: str

class ChatRequest(BaseModel):
    message: str
    agentic: Dict[str, Any] = {}
    system: Optional[str] = None  # Optional system prompt
    model: Optional[str] = None  # Optional model override
    temperature: Optional[float] = None  # Optional temperature override
    max_tokens: Optional[int] = None  # Optional max_tokens override
    stream: Optional[bool] = False  # Optional stream flag

# LM Studio API endpoint (adjust as needed)
LM_STUDIO_URL = os.environ.get("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")

@app.get("/files/list")
def list_files() -> List[str]:
    files: List[str] = []
    for root, _, filenames in os.walk(BASE_DIR):
        for f in filenames:
            rel_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
            files.append(rel_path)
    return files

@app.get("/files/read")
def read_file(path: str = Query(...)):
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
def write_file(req: FileWriteRequest):
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
def delete_file(req: FileDeleteRequest):
    abs_path = os.path.abspath(os.path.join(BASE_DIR, req.path))
    if not abs_path.startswith(BASE_DIR):
        return {"error": "Invalid path"}
    try:
        os.remove(abs_path)
        return {"status": "OK"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    # Build messages array for LM Studio
    messages = []
    # Use system prompt if provided, else default to empty
    if req.system:
        messages.append({"role": "system", "content": req.system})
    # Always add user message
    messages.append({"role": "user", "content": req.message})
    # Compose payload for LM Studio
    payload = {
        "model": req.model or req.agentic.get("model", "microsoft/phi-4-mini-reasoning"),
        "messages": messages,
        "max_tokens": req.max_tokens if req.max_tokens is not None else req.agentic.get("turnLimit", -1),
        "temperature": req.temperature if req.temperature is not None else req.agentic.get("temperature", 0.7),
        "stream": req.stream if req.stream is not None else False,
    }
    try:
        lm_response = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
        lm_response.raise_for_status()
        data = lm_response.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "[No response]")
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"[LM Studio error: {str(e)}]"}