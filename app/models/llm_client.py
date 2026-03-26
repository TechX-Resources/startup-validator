"""
LLM client abstraction for Azure OpenAI and OpenAI.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Provider-agnostic LLM client with Azure OpenAI as first preference."""

    def __init__(self, api_key: str | None = None, model_name: str | None = None):
        azure_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")

        openai_key = api_key or os.getenv("OPENAI_API_KEY")

        if azure_key and azure_endpoint:
            from openai import AzureOpenAI

            self._provider = "azure"
            self.model_name = model_name or azure_deployment
            self._client = AzureOpenAI(
                api_key=azure_key,
                api_version=azure_api_version,
                azure_endpoint=azure_endpoint,
            )
        elif openai_key:
            from openai import OpenAI

            self._provider = "openai"
            self.model_name = model_name or "gpt-4o-mini"
            self._client = OpenAI(api_key=openai_key)
        else:
            raise ValueError(
                "No API key found. Set AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT "
                "or OPENAI_API_KEY in .env"
            )

    def chat(self, messages: list[dict], **kwargs) -> str:
        """Send chat messages and return assistant text content."""
        try:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            raise RuntimeError(f"Error calling {self._provider} API: {str(exc)}") from exc

    def chat_with_tools(self, messages: list[dict], tools: list[dict], **kwargs) -> dict:
        """Send chat messages with tool definitions and return content/tool calls."""
        try:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools,
                **kwargs,
            )
            message = response.choices[0].message
            result = {"content": message.content}
            if message.tool_calls:
                result["tool_calls"] = message.tool_calls
            return result
        except Exception as exc:
            raise RuntimeError(f"Error calling {self._provider} API with tools: {str(exc)}") from exc
