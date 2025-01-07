from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

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
    # Placeholder for task generation logic
    tasks = [
        f"Task 1 for {request.topic}",
        f"Task 2 for {request.topic}",
        f"Task 3 for {request.topic}"
    ]
    return TaskResponse(tasks=tasks)
