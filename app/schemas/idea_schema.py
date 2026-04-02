

"""
Idea schema — structured input for validation requests.
Week 2: Define; use in main.py and validation_service.

Example JSON request:

{
  "idea": "An AI app that summarizes long PDFs for students in 3 bullet points.",
  "domain": "education",
  "industry": "edtech"
}
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class IdeaInput(BaseModel):
    """Request body for POST /validate-idea."""

    idea: str = Field(
        ...,
        description="The startup idea to validate (plain text).",
        min_length=10,
        max_length=500,
        examples=[
            "An AI app that summarizes long PDFs for students in 3 bullet points."
        ],
    )

    # Optional context fields (useful later for better validation)
    domain: Optional[str] = Field(
        None,
        description="Optional domain or category of the idea (e.g. fintech, edtech, healthtech).",
        examples=["edtech"]
    )

    industry: Optional[str] = Field(
        None,
        description="Optional industry segment the idea targets.",
        examples=["education"]
    )


class IdeaWithContext(IdeaInput):
    """
    Internal schema used by validation services or agents.
    Extends IdeaInput with memory/context retrieved from vector DB.
    """

    context_from_memory: List[Dict] = Field(
        default_factory=list,
        description="Relevant past ideas and results retrieved from memory."
    )