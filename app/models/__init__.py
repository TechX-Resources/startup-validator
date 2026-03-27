"""
Models layer — LLM abstraction + base classes.
Week 2: Single import point for all model-related functionality.
Usage: from app.models import LLMFactory, ValidationScore
"""

__version__ = "0.1.0"

# Base classes
from .base import (
    BaseLLMResponse,
    LLMClient,
    ValidationScore,
    BaseModel as PydanticBaseModel  # Alias for convenience
)

# Concrete LLM implementations
from .llm import (
    LLMFactory,
    OpenAILLM,
    AnthropicLLM
)

# Re-exports for convenience (Week 5+ agent will use these)
__all__ = [
    # Base
    "BaseLLMResponse",
    "LLMClient", 
    "ValidationScore",
    "PydanticBaseModel",
    
    # Factory & Implementations
    "LLMFactory",
    "OpenAILLM",
    "AnthropicLLM",
]

# Quick factory access (Week 5 convenience)
get_llm = LLMFactory.create

# Default model names (Week 3+ tool usage)
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"

# Quick test function (remove in production)
def test_connection(verbose: bool = False) -> bool:
    """
    Test LLM connection (Week 2 dev utility).
    
    Usage: python -c "from app.models import test_connection; test_connection()"
    """
    try:
        llm = get_llm()
        # Minimal test message
        messages = [{"role": "user", "content": "Say 'OK' if connected."}]
        response = asyncio.run(llm.chat(messages))
        if verbose:
            print(f"✅ LLM connected: {response.content.strip()}")
        return True
    except Exception as e:
        if verbose:
            print(f"❌ LLM test failed: {e}")
        return False
