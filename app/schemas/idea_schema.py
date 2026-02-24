"""
Idea schema — structured input for validation requests.
Week 2: Define; use in main.py and validation_service.
"""

from pydantic import BaseModel, Field


class IdeaInput(BaseModel):
    """Request body for /validate-idea."""

    idea: str = Field(..., description="The startup idea to validate (plain text).")
    # Optional: domain, industry, or extra context
    # domain: str | None = None
    # industry: str | None = None

    # Example JSON:
    # {"idea": "An AI app that summarizes long PDFs for students in 3 bullet points."}


class IdeaWithContext(IdeaInput):
    """Optional: idea + context from memory (used internally by service/agent)."""
    # context_from_memory: list[dict] = []
    pass
