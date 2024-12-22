from fastapi import FastAPI, Request
from pydantic import BaseModel
import asyncio
import AgentDocs.AssistantFileSearch.Program as assistant

app = FastAPI()

class AIRequest(BaseModel):
    user_input: str

@app.get("/")
def greet_json():
    return {"Hello": "World!"}

@app.post("/ai-interact")
async def ai_interact(request: Request, ai_request: AIRequest):
    user_input = ai_request.user_input
    response = await assistant.HandleAIInteraction(user_input)
    return {"response": response}
