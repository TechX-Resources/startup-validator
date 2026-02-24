"""
LLM client abstraction — single interface for OpenAI/Claude.
Week 2: Implement chat completion and (optional) structured output.
"""


class LLMClient:
    """Abstracted client for LLM API calls. Swap provider without changing agent code."""

    def __init__(self, api_key: str = None, model_name: str = "gpt-4"):
        # TODO: Load api_key from config/env if not passed.
        # TODO: Support model_name (e.g. gpt-4, claude-3-sonnet).
        self.api_key = api_key
        self.model_name = model_name

    def chat(self, messages: list[dict], **kwargs) -> str:
        """
        Send messages to LLM and return assistant reply as string.
        messages: [{"role": "user"|"system"|"assistant", "content": "..."}]
        TODO: Call OpenAI or Claude API; return content of the last message.
        """
        raise NotImplementedError("Implement in Week 2: call LLM API and return reply text.")

    def chat_with_tools(self, messages: list[dict], tools: list[dict], **kwargs) -> dict:
        """
        Optional: support tool/function calling from the API.
        Returns dict with either 'content' or 'tool_calls' for the agent to handle.
        TODO: Implement when building agent tool-calling loop (Week 5).
        """
        raise NotImplementedError("Optional: implement for native tool-calling in Week 5.")
