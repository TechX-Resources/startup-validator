"""
LLM client abstraction — single interface for multiple providers (OpenAI, Anthropic, Gemini).
Week 2: Implement chat completion and (optional) structured output.
"""

from typing import Optional
from openai import OpenAI
from anthropic import Anthropic
from google import genai
from google.genai import types
from app.config import settings

class LLMClient:
    """Abstracted client for LLM API calls. Supports OpenAI, Anthropic, and Google Gemini."""

    def __init__(self, provider: Optional[str] = None, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        
        # Infer provider if not given
        if provider is None:
            if model_name.startswith("gpt") or model_name.startswith("o1"):
                self.provider = "openai"
            elif model_name.startswith("claude"):
                self.provider = "anthropic"
            elif model_name.startswith("gemini"):
                self.provider = "gemini"
            else:
                self.provider = "openai" 
        else:
            self.provider = provider.lower()

        if self.provider == "openai":
            self.api_key = api_key or settings.openai_api_key
            if not self.api_key:
                raise ValueError("OpenAI API Key is required. Set OPENAI_API_KEY in environment or .env file.")
            self.client = OpenAI(api_key=self.api_key)
            
        elif self.provider == "anthropic":
            self.api_key = api_key or settings.anthropic_api_key
            if not self.api_key:
                raise ValueError("Anthropic API Key is required. Set ANTHROPIC_API_KEY in environment or .env file.")
            self.client = Anthropic(api_key=self.api_key)
            
        elif self.provider == "gemini":
            self.api_key = api_key or settings.gemini_api_key
            if not self.api_key:
                raise ValueError("Gemini API Key is required. Set GEMINI_API_KEY in environment or .env file.")
            self.client = genai.Client(api_key=self.api_key)
            
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _convert_messages_for_anthropic(self, messages: list[dict]) -> tuple[Optional[str], list[dict]]:
        """Extracts system messages since Anthropic expects them separately."""
        system_msg = None
        converted = []
        for msg in messages:
            if msg.get("role") == "system":
                system_msg = msg.get("content")
            else:
                converted.append(msg)
        return system_msg, converted

    def _convert_messages_for_gemini(self, messages: list[dict]) -> tuple[Optional[str], list[types.Content]]:
        """Converts standard OpenAI-style messages to Gemini Content types."""
        system_instruction = None
        contents = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "system":
                system_instruction = content
            elif role == "user":
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=content)]))
            elif role == "assistant":
                contents.append(types.Content(role="model", parts=[types.Part.from_text(text=content)]))
        return system_instruction, contents

    def chat(self, messages: list[dict], **kwargs) -> str:
        """
        Send messages to LLM and return assistant reply as string.
        messages: [{"role": "user"|"system"|"assistant", "content": "..."}]
        """
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
            
        elif self.provider == "anthropic":
            system_msg, converted_messages = self._convert_messages_for_anthropic(messages)
            
            # Anthropic requires max_tokens
            max_tokens = kwargs.pop("max_tokens", 1024)
            params = {
                "model": self.model_name,
                "messages": converted_messages,
                "max_tokens": max_tokens,
                **kwargs
            }
            if system_msg:
                params["system"] = system_msg
                
            response = self.client.messages.create(**params)
            return response.content[0].text
            
        elif self.provider == "gemini":
            system_instruction, contents = self._convert_messages_for_gemini(messages)
            
            config = types.GenerateContentConfig()
            if system_instruction:
                config.system_instruction = system_instruction
            if "temperature" in kwargs:
                config.temperature = kwargs["temperature"]
                
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config,
            )
            return response.text

    def chat_with_tools(self, messages: list[dict], tools: list[dict], **kwargs) -> dict:
        """
        Optional: support tool/function calling from the API.
        Returns dict with either 'content' or 'tool_calls' for the agent to handle.
        """
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools,
                **kwargs
            )
            message = response.choices[0].message
            
            if message.tool_calls:
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
            
        elif self.provider == "anthropic":
            raise NotImplementedError("Tool calling with Claude is not fully implemented yet in the abstraction.")
            
        elif self.provider == "gemini":
            raise NotImplementedError("Tool calling with Gemini is not fully implemented yet in the abstraction.")
