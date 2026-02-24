"""
Shared helpers — truncation, safe parse, retries, etc.
Add as needed during Weeks 2–6.
"""


def truncate_for_llm(text: str, max_chars: int = 4000) -> str:
    """Truncate text to max_chars for LLM context. TODO: Implement if needed."""
    # TODO: Optionally add "..." at end
    return text[:max_chars] if len(text) > max_chars else text
