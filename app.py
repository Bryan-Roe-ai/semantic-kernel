from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import requests

app = FastAPI()

class TaskRequest(BaseModel):
    purpose: str
    audience: str
    topic: str
    difficulty: str
    task_type: str

class TaskResponse(BaseModel):
    tasks: List[str]

@app.get("/")
def greet_json():
    return {"Hello": "World!"}

@app.post("/generate-tasks", response_model=TaskResponse)
def generate_tasks(request: TaskRequest):
    try:
        # Placeholder for task generation logic
        tasks = [
            f"Task 1 for {request.topic}",
            f"Task 2 for {request.topic}",
            f"Task 3 for {request.topic}"
        ]
        return TaskResponse(tasks=tasks)
    except Exception as e:
        logging.error(f"Error generating tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/test-model")
def test_model():
    try:
        # Placeholder for model testing logic
        return {"status": "Model is running successfully"}
    except Exception as e:
        logging.error(f"Error testing model: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/run-ai")
def run_ai():
    try:
        ai_service_url = "https://your-ai-service-url.com/api/ai"
        response = requests.get(ai_service_url)
        response.raise_for_status()
        ai_response = response.text
        return {"ai_response": ai_response}
    except Exception as e:
        logging.error(f"Error running AI: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

class LLMRequest(BaseModel):
    prompt: str

class LLMResponse(BaseModel):
    response: str

@app.post("/interact-llm", response_model=LLMResponse)
def interact_llm(request: LLMRequest):
    try:
        # Placeholder for LLM interaction logic
        llm_response = f"Response to prompt: {request.prompt}"
        return LLMResponse(response=llm_response)
    except Exception as e:
        logging.error(f"Error interacting with LLM: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
