from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging

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
