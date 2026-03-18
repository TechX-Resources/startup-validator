import os

class LLMClient:
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