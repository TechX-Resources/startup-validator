
"""
Concrete LLM implementations (OpenAI + Anthropic)
Week 2: Switchable LLM client
"""

import openai
import anthropic
from typing import List, Dict, Any, AsyncGenerator
import asyncio
from app.models.base import LLMClient, BaseLLMResponse
from app.config.settings import settings

class OpenAILLM(LLMClient):
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-4o-mini",
        **kwargs
    ) -> BaseLLMResponse:
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        choice = response.choices[0]
        return BaseLLMResponse(
            content=choice.message.content or "",
            usage=response.usage.model_dump() if response.usage else None
        )
    
    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        **kwargs
    ) -> AsyncGenerator[BaseLLMResponse, None]:
        stream = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            **kwargs
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield BaseLLMResponse(content=chunk.choices[0].delta.content)

class AnthropicLLM(LLMClient):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "claude-3-5-sonnet-20240620",
        **kwargs
    ) -> BaseLLMResponse:
        # Convert OpenAI format to Anthropic
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_messages = [m for m in messages if m["role"] != "system"]
        
        response = await self.client.messages.create(
            model=model,
            max_tokens=4096,
            messages=user_messages,
            system=system,
            **kwargs
        )
        return BaseLLMResponse(content=response.content[0].text)
    
    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-5-sonnet-20240620",
        **kwargs
    ) -> AsyncGenerator[BaseLLMResponse, None]:
        # Streaming implementation for Anthropic
        raise NotImplementedError("Anthropic streaming - Week 3 stretch")

class LLMFactory:
    @staticmethod
    def create() -> LLMClient:
        if settings.llm_provider == "openai" or (
            settings.llm_provider == "auto" and settings.openai_api_key
        ):
            return OpenAILLM()
        elif settings.anthropic_api_key:
            return AnthropicLLM()
        else:
            raise ValueError("No valid LLM provider configured")
