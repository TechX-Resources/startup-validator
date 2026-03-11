"""
LLM client abstraction — single interface for OpenAI/Claude.
Week 2: Implement chat completion and (optional) structured output.
"""


from typing import Optional, List, Dict, Any
from openai import OpenAI
from app.config import settings

class LLMClient:
    """
    Abstracted client for LLM API calls.
    Swap provider without changing agent code.
    
    Week 2: Implement chat completion with OpenAI API.
    Future: Support Claude, Anthropic, or other providers.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-4o"):
        """
        Initialize LLM client with API key and model name.
        
        Args:
            api_key: API key for the LLM provider (defaults to OPENAI_API_KEY from config)
            model_name: Model name (e.g., gpt-4o, gpt-4-turbo, claude-3-sonnet)
        """
        # Load API key from config if not passed
        self.api_key = api_key or settings.OPENAI_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY is required. "
                "Set it in .env file or pass api_key parameter."
            )
        
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Send messages to LLM and return assistant reply as string.
        
        Args:
            messages: List of message dicts with role and content
                     [{"role": "user"|"system"|"assistant", "content": "..."}]
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        
        Returns:
            String content of the last message from the assistant
        
        Example:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"}
            ]
            response = llm_client.chat(messages)
        """
        # Default parameters
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
        # TODO: Week 5 - Implement tool calling
        # For now, raise NotImplementedError
        raise NotImplementedError(
            "Tool calling not yet implemented. "
            "This will be used in Week 5 for agent orchestration."
        )

    def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Stream chat response for real-time UI updates.
        
        Args:
            messages: List of message dicts
            **kwargs: Additional parameters
        
        Returns:
            Complete response string (accumulated from stream)
        """
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
