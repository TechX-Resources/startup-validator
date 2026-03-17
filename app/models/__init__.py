
from .llm_client import LLMClient, llm_client

__all__ = ["LLMClient", "llm_client"]

# Singleton instance for easy importing across the application
llm_client = LLMClient()
