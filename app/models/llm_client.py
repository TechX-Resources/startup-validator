import os
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, api_key: str = None, model_name: str = None):
        self.openai_key = api_key or settings.openai_api_key
        self.anthropic_key = settings.anthropic_api_key
        self.gemini_key = settings.gemini_api_key
        self._provider = None
        self._client = None
        self.model_name = model_name

        if self.openai_key:
            try:
                from openai import OpenAI
                self.model_name = self.model_name or "gpt-4o-mini"
                self._client = OpenAI(api_key=self.openai_key)
                self._provider = "openai"
                logger.info(f"LLMClient initialized with OpenAI ({self.model_name})")
            except ImportError:
                logger.warning("OpenAI library not found even though key is provided.")

        if not self._provider and self.anthropic_key:
            try:
                from anthropic import Anthropic
                self.model_name = self.model_name or "claude-3-5-sonnet-20240620"
                self._client = Anthropic(api_key=self.anthropic_key)
                self._provider = "anthropic"
                logger.info(f"LLMClient initialized with Anthropic ({self.model_name})")
            except ImportError:
                logger.warning("Anthropic library not found even though key is provided.")

        if not self._provider and self.gemini_key:
            try:
                import google.generativeai as genai
                self.model_name = self.model_name or "gemini-1.5-flash"
                genai.configure(api_key=self.gemini_key)
                self._client = genai.GenerativeModel(self.model_name)
                self._provider = "gemini"
                logger.info(f"LLMClient initialized with Gemini ({self.model_name})")
            except ImportError:
                logger.warning("Google Generative AI library not found even though GEMINI_API_KEY is provided.")

        if not self._provider:
            logger.error("No LLM provider could be initialized. Please set API keys and install required libraries.")
            # We don't raise here yet to allow the 'chat' method to handle it or for mock mode.

    def chat(self, messages: list[dict], **kwargs) -> str:
        if not self._provider:
            logger.warning("No LLM provider initialized. Returning mock response.")
            return '{"status": "mock", "message": "Development mock response"}'

        try:
            if self._provider == "openai":
                response = self._client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    **kwargs
                )
                return response.choices[0].message.content
            
            elif self._provider == "anthropic":
                system = next((m['content'] for m in messages if m['role'] == 'system'), "")
                msgs = [m for m in messages if m['role'] != 'system']
                response = self._client.messages.create(
                    model=self.model_name,
                    system=system,
                    messages=msgs,
                    max_tokens=2048,
                    **kwargs
                )
                return response.content[0].text
            
            elif self._provider == "gemini":
                prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
                response = self._client.generate_content(prompt)
                return response.text
                
        except Exception as e:
            logger.error(f"Error during LLM chat with {self._provider}: {e}")
            return '{"error": "LLM call failed", "details": "' + str(e) + '"}'

        return ""