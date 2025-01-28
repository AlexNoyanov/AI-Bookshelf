from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

app = FastAPI()

# Models for request/response schemas
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500
    stream: Optional[bool] = False

class ChatChoice(BaseModel):
    message: ChatMessage
    finish_reason: Optional[str] = "stop"
    index: int = 0

class ChatResponse(BaseModel):
    id: str = "mock-response-id"
    object: str = "chat.completion"
    created: int = 1700000000
    model: str
    choices: List[ChatChoice]
    usage: Dict[str, int] = {
        "prompt_tokens": 50,
        "completion_tokens": 100,
        "total_tokens": 150
    }

class ModelInfo(BaseModel):
    name: str
    description: str
    license: str
    context_size: int
    prompt_template: str

# Mock data
AVAILABLE_MODELS = [
    {
        "name": "gpt4all-j-v1.3-groovy",
        "description": "A mock GPT4All model for testing",
        "license": "MIT",
        "context_size": 2048,
        "prompt_template": "### Human: %1\n### Assistant: "
    },
    {
        "name": "mistral-7b-openorca.Q4_0",
        "description": "Mistral 7B model fine-tuned on OpenOrca dataset",
        "license": "Apache 2.0",
        "context_size": 8192,
        "prompt_template": "### Human: %1\n### Assistant: "
    }
]

# Endpoints
@app.get("/v1/models")
async def list_models() -> List[ModelInfo]:
    """List available models"""
    return AVAILABLE_MODELS

@app.get("/v1/models/{model_name}")
async def get_model(model_name: str) -> ModelInfo:
    """Get details of a specific model"""
    for model in AVAILABLE_MODELS:
        if model["name"] == model_name:
            return model
    raise HTTPException(status_code=404, detail="Model not found")

@app.post("/v1/completions")
async def create_completion(request: Dict[str, Any]) -> Dict[str, Any]:
    """Generate text completions"""
    return {
        "id": "mock-completion-id",
        "object": "text_completion",
        "created": 1700000000,
        "model": request.get("model", "default"),
        "choices": [{
            "text": "This is a mock completion response.",
            "index": 0,
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 50,
            "completion_tokens": 100,
            "total_tokens": 150
        }
    }

@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatRequest) -> ChatResponse:
    """Generate chat completions"""
    # Mock different responses based on input
    user_message = request.messages[-1].content.lower()
    
    if "book" in user_message or "reading" in user_message:
        response_text = "I recommend reading 'The Foundation' by Isaac Asimov. It's a classic science fiction novel that explores the concept of psychohistory and the future of human civilization. Would you like to know more about it?"
    elif "hello" in user_message or "hi" in user_message:
        response_text = "Hello! I'm your AI assistant. How can I help you today?"
    else:
        response_text = "I understand your message. As an AI assistant, I aim to provide helpful and informative responses. Could you please provide more details about what you'd like to know?"

    return ChatResponse(
        model=request.model,
        choices=[
            ChatChoice(
                message=ChatMessage(
                    role="assistant",
                    content=response_text
                )
            )
        ]
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4891)
