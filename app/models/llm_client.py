import os

from typing import Optional, List, Dict, Any
from openai import OpenAI
from app.config import settings

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-4o"):
       
        self.api_key = api_key or settings.OPENAI_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY is required. "
                "Set it in .env file or pass api_key parameter."
            )
        
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        params = {
            "model": self.model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000),
        }
        
        # Add optional parameters
        if "stream" in kwargs:
            params["stream"] = kwargs["stream"]
        
        # Call OpenAI API
        response = self.client.chat.completions.create(**params)
        
        # Return content of the last message
        return response.choices[0].message.content

    def chat_with_tools(self, messages: List[Dict[str, str]], tools: List[Dict], **kwargs) -> Dict[str, Any]:
        """
        Optional: support tool/function calling from the API.
        Returns dict with either 'content' or 'tool_calls' for the agent to handle.
        
        TODO: Implement when building agent tool-calling loop (Week 5).
        
        Args:
            messages: List of message dicts
            tools: List of tool definitions for function calling
            **kwargs: Additional parameters
        
        Returns:
            Dict with 'content' (string) or 'tool_calls' (list of tool call objects)
        """
        raise NotImplementedError(
            "Tool calling not yet implemented. "
            "This will be used in Week 5 for agent orchestration."
        )

    def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        params = {
            "model": self.model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "stream": True,
        }
        
        full_response = ""
        for chunk in self.client.chat.completions.create(**params):
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
        
        return full_response

    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the current model configuration.
        
        Returns:
            Dict with model_name and provider info
        """
        return {
            "model_name": self.model_name,
            "provider": "OpenAI",
            "api_key_configured": bool(self.api_key)
        }
    def __init__(self, api_key: str = None, model_name: str = None):
        openai_key = api_key or os.getenv("OPENAI_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")

        if openai_key:
            from openai import OpenAI
            self.model_name = model_name or "gpt-4o-mini"
            self._client = OpenAI(api_key=openai_key)
            self._provider = "openai"
        elif groq_key:
            from groq import Groq
            self.model_name = model_name or "llama-3.3-70b-versatile"
            self._client = Groq(api_key=groq_key)
            self._provider = "groq"
        else:
            raise ValueError("No API key found. Set OPENAI_API_KEY or GROQ_API_KEY in .env")

    def chat(self, messages: list[dict], **kwargs) -> str:
        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
