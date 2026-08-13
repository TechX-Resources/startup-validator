from pydantic import BaseModel
from typing import Optional, Dict, Any

class BaseLLMResponse(BaseModel):
    content: str
    usage: Optional[Dict[str, Any]] = None

class LLMClient:
    """Abstract base class for switchable LLM clients."""
    async def chat(self, messages: list[dict], **kwargs) -> BaseLLMResponse:
        raise NotImplementedError("Subclasses must implement chat")

    async def stream_chat(self, messages: list[dict], **kwargs):
        raise NotImplementedError("Subclasses must implement stream_chat")

class ValidationScore(BaseModel):
    score: float
    reason: str
