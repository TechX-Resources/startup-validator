"""
LLM client abstraction — single interface for OpenAI/Claude.
Week 2: Implement chat completion and (optional) structured output.
"""


from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import os

from app.config import settings


class LLMClient(ABC):
    """Abstracted client for LLM API calls. Swap provider without changing agent code."""

    def __init__(self, api_key: str = None, model_name: str = "gpt-4"):
        # Load api_key from config/env if not passed
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model_name = model_name
        self._client = None

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Send messages to LLM and return assistant reply as string.
        messages: [{"role": "user"|"system"|"assistant", "content": "..."}]
        """
        pass

    def chat_with_tools(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """
        Optional: support tool/function calling from the API.
        Returns dict with either 'content' or 'tool_calls' for the agent to handle.
        """
        raise NotImplementedError("Optional: implement for native tool-calling in Week 5.")


class OpenAIClient(LLMClient):
    """OpenAI API client implementation."""

    def __init__(self, api_key: str = None, model_name: str = "gpt-4o"):
        super().__init__(api_key, model_name)
        self._client = None

    def _get_client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Call OpenAI API and return assistant reply as string.
        """
        client = self._get_client()
        
        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2000),
        )
        
        return response.choices[0].message.content


class ClaudeClient(LLMClient):
    """Anthropic Claude API client implementation."""

    def __init__(self, api_key: str = None, model_name: str = "claude-3-5-sonnet-20241022"):
        super().__init__(api_key, model_name)
        self._client = None

    def _get_client(self):
        """Lazy initialization of Anthropic client."""
        if self._client is None:
            from anthropic import Anthropic
            self._client = Anthropic(api_key=self.api_key)
        return self._client

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Call Claude API and return assistant reply as string.
        """
        client = self._get_client()
        
        # Convert messages to Claude format
        formatted_messages = []
        system_message = None
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                formatted_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        response = client.messages.create(
            model=self.model_name,
            messages=formatted_messages,
            system=system_message,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2000),
        )
        
        return response.content[0].text


class LLMClientFactory:
    """Factory to create LLM clients based on configuration."""

    @staticmethod
    def create_client(provider: str = "openai") -> LLMClient:
        """Create an LLM client based on the provider."""
        if provider == "openai":
            return OpenAIClient()
        elif provider == "claude":
            return ClaudeClient()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")


# Default client instance (uses OpenAI by default)
default_llm_client = LLMClientFactory.create_client("openai")
