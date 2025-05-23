# Save as backend.py and run with: uvicorn backend:app --reload

from fastapi import FastAPI, Query  # type: ignore
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from typing import List, Dict, Any, Optional

app: FastAPI = FastAPI()
app.add_middleware(  # type: ignore
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
    system: Optional[str] = None  # Optional system prompt
    model: Optional[str] = None  # Optional model override
    temperature: Optional[float] = None  # Optional temperature override
    max_tokens: Optional[int] = None  # Optional max_tokens override
    stream: Optional[bool] = False  # Optional stream flag

# LM Studio API endpoint (do NOT append /api/chat)
LM_STUDIO_URL = os.environ.get("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")

@app.get("/files/list")  # type: ignore
def list_files() -> List[str]:
    files: List[str] = []
    for root, _, filenames in os.walk(BASE_DIR):
        for f in filenames:
            rel_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
            files.append(rel_path)
    return files
@app.get("/files/read")  # type: ignore
def read_file(path: str = Query(...)) -> Dict[str, Any]:
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

@app.post("/api/chat")  # type: ignore
def chat_endpoint(req: ChatRequest) -> Dict[str, str]:
    # Build messages array for LM Studio
    messages: List[Dict[str, str]] = []
    if req.system:
        messages.append({"role": "system", "content": req.system})
    messages.append({"role": "user", "content": req.message})
    # Compose payload for LM Studio
    payload: Dict[str, Any] = {
        "model": req.model or "microsoft/phi-4-mini-reasoning",
        "messages": messages,
        "max_tokens": req.max_tokens if req.max_tokens is not None else -1,
        "temperature": req.temperature if req.temperature is not None else 0.7,
        "stream": req.stream if req.stream is not None else False,
    }
    # Only POST to LM_STUDIO_URL, do not append /api/chat
    try:
        lm_response = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
        lm_response.raise_for_status()
        data = lm_response.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "[No response]")
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"[LM Studio error: {str(e)}]"}