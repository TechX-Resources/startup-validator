# Startup Idea Validator Agent — FastAPI app package
"""
Startup Idea Validator Agent 
MCP Architecture: Model + Context + Tools + Orchestration
Built over 6 weeks by AI + Data Science students
"""

__version__ = "0.1.0"
__description__ = "AI-powered startup idea validation agent"

from .config import settings
from .schemas import IdeaInput, ValidationResponse, IdeaWithContext

__all__ = [
    "settings",
    "IdeaInput", 
    "ValidationResponse",
    "IdeaWithContext",
    "__version__",
    "__description__"
]

# MCP Layer Status
MCP_STATUS = {
    "Model": "✅ Week 2 (LLM abstraction)",
    "Context": "⏳ Week 4 (Memory/VectorDB)", 
    "Tools": "✅ Week 3 (Search/Competitors/Market)",
    "Orchestration": "⏳ Week 5 (Agent loop)"
}
