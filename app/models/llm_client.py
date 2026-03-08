"""
LLM client abstraction — single interface for OpenAI/Claude.
Week 2: Implement chat completion and (optional) structured output.
"""

from typing import Optional
from openai import OpenAI
from app.config import settings

class LLMClient:
    """Abstracted client for LLM API calls. Swap provider without changing agent code."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-4-turbo"):
        # Load api_key from config/env if not passed.
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API Key is required. Set OPENAI_API_KEY in environment or .env file.")
        
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key)

    def chat(self, messages: list[dict], **kwargs) -> str:
        """
        Send messages to LLM and return assistant reply as string.
        messages: [{"role": "user"|"system"|"assistant", "content": "..."}]
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

    def chat_with_tools(self, messages: list[dict], tools: list[dict], **kwargs) -> dict:
        """
        Optional: support tool/function calling from the API.
        Returns dict with either 'content' or 'tool_calls' for the agent to handle.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=tools,
            **kwargs
        )
        message = response.choices[0].message
        
        if message.tool_calls:
            # Return list of tool calls to be processed
            return {
                "content": message.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                    for call in (message.tool_calls or [])
                ]
            }
        
        return {"content": message.content}
