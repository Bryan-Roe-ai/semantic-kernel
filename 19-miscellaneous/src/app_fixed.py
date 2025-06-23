from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
import requests
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Task Generation API",
    description="API for generating educational tasks",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TaskRequest(BaseModel):
    purpose: str = Field(..., description="The purpose of the tasks")
    audience: str = Field(..., description="Target audience for the tasks")
    topic: str = Field(..., description="Topic for the tasks")
    difficulty: str = Field(..., description="Difficulty level")
    task_type: str = Field(..., description="Type of task")
    
    class Config:
        schema_extra = {
            "example": {
                "purpose": "Practice",
                "audience": "High School Students",
                "topic": "Photosynthesis",
                "difficulty": "Medium",
                "task_type": "Multiple Choice"
            }
        }

class TaskResponse(BaseModel):
    tasks: List[str] = Field(..., description="List of generated tasks")

class LLMRequest(BaseModel):
    prompt: str = Field(..., description="Prompt for the LLM")

class LLMResponse(BaseModel):
    response: str = Field(..., description="Response from the LLM")

# Dependencies
def get_html_path():
    """Dependency to get the HTML file path."""
    docs_dir = Path(__file__).parent / "docs"
    docs_dir.mkdir(exist_ok=True)
    return docs_dir / "index.html"

# Routes
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint returning a greeting."""
    return {"Hello": "World!"}

@app.post("/generate-tasks", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def generate_tasks(request: TaskRequest):
    """
    Generate educational tasks based on input parameters.
    """
    try:
        logger.info(f"Generating tasks for topic: {request.topic}")
        # Placeholder for task generation logic
        tasks = [
            f"Task 1 for {request.topic}",
            f"Task 2 for {request.topic}",
            f"Task 3 for {request.topic}"
        ]
        return TaskResponse(tasks=tasks)
    except Exception as e:
        logger.error(f"Error generating tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to generate tasks"
        )

@app.get("/test-model", status_code=status.HTTP_200_OK)
async def test_model():
    """
    Test if the model is running properly.
    """
    try:
        logger.info("Testing model")
        # Placeholder for model testing logic
        return {"status": "Model is running successfully"}
    except Exception as e:
        logger.error(f"Error testing model: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Model test failed"
        )

@app.get("/run-ai", status_code=status.HTTP_200_OK)
async def run_ai():
    """
    Run AI service and update webpage with response.
    """
    try:
        logger.info("Running AI service")
        ai_service_url = os.environ.get("AI_SERVICE_URL", "https://your-ai-service-url.com/api/ai")
        
        response = requests.get(ai_service_url, timeout=10)
        response.raise_for_status()
        ai_response = response.text
        
        await update_webpage(ai_response)
        return {"ai_response": ai_response}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to AI service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="AI service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error in run_ai: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to run AI"
        )

@app.post("/interact-llm", response_model=LLMResponse, status_code=status.HTTP_200_OK)
async def interact_llm(request: LLMRequest):
    """
    Interact with the LLM model using the provided prompt.
    """
    try:
        logger.info(f"Processing LLM request with prompt length: {len(request.prompt)}")
        # Placeholder for LLM interaction logic
        llm_response = f"Response to prompt: {request.prompt}"
        return LLMResponse(response=llm_response)
    except Exception as e:
        logger.error(f"Error interacting with LLM: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="LLM interaction failed"
        )

@app.post("/update-webpage", status_code=status.HTTP_200_OK)
async def update_webpage(ai_response: str, html_path: Path = Depends(get_html_path)):
    """
    Update the webpage with AI response.
    """
    try:
        logger.info("Updating webpage with AI response")
        if not html_path.exists():
            with open(html_path, "w") as file:
                file.write("<html><body><div id=\"ai-response\"></div></body></html>")
        
        with open(html_path, "r") as file:
            content = file.read()
            
        updated_content = content.replace(
            "<div id=\"ai-response\"></div>", 
            f"<div id=\"ai-response\">{ai_response}</div>"
        )
        
        with open(html_path, "w") as file:
            file.write(updated_content)
            
        return {"status": "Webpage updated successfully"}
    except Exception as e:
        logger.error(f"Error updating webpage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update webpage"
        )

# Run the application with: uvicorn app:app --reload