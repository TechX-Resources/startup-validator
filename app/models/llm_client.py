import os
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, api_key: str = None, model_name: str = None):
        self.xai_key = settings.xai_api_key
        self.openai_key = api_key or settings.openai_api_key
        self.anthropic_key = settings.anthropic_api_key
        self.gemini_key = settings.gemini_api_key
        self._provider = None # Will be set below
        self._client = None
        self.model_name = model_name

        provider_preference = settings.llm_provider.lower() if hasattr(settings, 'llm_provider') else "grok"

        # 1. Try OpenAI if preferred or if auto
        if (provider_preference in ["auto", "openai"]) and self.openai_key:
            try:
                from openai import OpenAI
                self.model_name = self.model_name or "gpt-4o-mini"
                self._client = OpenAI(api_key=self.openai_key)
                self._provider = "openai"
                logger.info(f"LLMClient initialized with OpenAI ({self.model_name})")
            except ImportError:
                logger.warning("OpenAI library not found even though key is provided.")

        # 2. Try Grok if preferred or if auto
        if not self._provider and (provider_preference in ["auto", "grok", "groq", "xai"]) and self.xai_key:
            try:
                from openai import OpenAI
                self.model_name = self.model_name or "llama-3.1-8b-instant"
                self._client = OpenAI(
                    api_key=self.xai_key,
                    base_url="https://api.groq.com/openai/v1",
                )
                self._provider = "grok"
                logger.info(f"LLMClient initialized with Grok ({self.model_name})")
            except ImportError:
                logger.warning("OpenAI library not found for Groq initialization.")

        # 3. Try Anthropic if preferred or if auto
        if not self._provider and (provider_preference in ["auto", "anthropic"]) and self.anthropic_key:
            try:
                from anthropic import Anthropic
                self.model_name = self.model_name or "claude-3-5-sonnet-20240620"
                self._client = Anthropic(api_key=self.anthropic_key)
                self._provider = "anthropic"
                logger.info(f"LLMClient initialized with Anthropic ({self.model_name})")
            except ImportError:
                logger.warning("Anthropic library not found even though key is provided.")

        # 4. Try Gemini if preferred or if auto
        if not self._provider and (provider_preference in ["auto", "gemini"]) and self.gemini_key:
            try:
                from google import genai
                self.model_name = self.model_name or "gemini-2.0-flash"
                self._client = genai.Client(api_key=self.gemini_key)
                self._provider = "gemini"
                logger.info(f"LLMClient initialized with Gemini ({self.model_name})")
            except ImportError:
                logger.warning("Google GenAI library (google-genai) not found even though GEMINI_API_KEY is provided.")
            except Exception as e:
                logger.error(f"Gemini init error: {e}")


        if not self._provider:
            logger.error("No LLM provider could be initialized. Please set API keys and install required libraries.")
            # We don't raise here yet to allow the 'chat' method to handle it or for mock mode.

    def chat(self, messages: list[dict], **kwargs) -> str:
        if not self._provider:
            return '{"error": "No LLM provider initialized", "message": "Please set API keys and install required libraries."}'

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
                # Convert messages to format expected by google-genai (simple list of content strings or parts)
                # Actually, google-genai accepts content objects. For simplicity, we just join them like before
                # or pass them as a list if we want to be more sophisticated.
                prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                return response.text
            elif self._provider == "grok":
                logger.info(f"Chatting with Groq using model {self.model_name}")
                try:
                    response = self._client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        **kwargs
                    )
                    # Log the full response for more visibility during debug
                    logger.debug(f"Groq response: {response}")
                    
                    if not response.choices:
                        logger.warning("Groq returned no choices.")
                        return ""
                        
                    content = response.choices[0].message.content
                    if not content:
                        logger.warning("Groq returned empty content.")
                        # Check for finish_reason
                        finish_reason = response.choices[0].finish_reason
                        logger.info(f"Groq finish_reason: {finish_reason}")
                        
                    return content or ""
                except Exception as api_err:
                    logger.error(f"Groq API call failed: {api_err}")
                    raise api_err
        except Exception as e:
            logger.error(f"Error during LLM chat with {self._provider}: {e}")
            return '{"error": "LLM call failed", "details": "' + str(e) + '"}'

        return ""