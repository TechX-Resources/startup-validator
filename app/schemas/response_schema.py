"""
Response schema — structured output from validation agent.
Week 2: Define; returned by validation_service and /validate-idea.
"""

from pydantic import BaseModel, Field
from typing import List


class ValidationResponse(BaseModel):
    """Structured validation result returned by the agent and API."""

    score: float = Field(..., ge=0, le=10, description="Overall validation score 0–10.")
    summary: str = Field(..., description="Short summary of the validation.")
    strengths: list[str] = Field(default_factory=list, description="List of strengths.")
    risks: list[str] = Field(default_factory=list, description="List of risks or concerns.")
    competitors: list[str] = Field(default_factory=list, description="Notable competitors or alternatives.")
    market_notes: str | None = Field(None, description="Optional market size or growth notes.")

    # Example JSON:
    # {
    #   "score": 7.5,
    #   "summary": "Strong idea with clear use case; market is crowded.",
    #   "strengths": ["Clear pain point", "Scalable"],
    #   "risks": ["Many existing tools", "Monetization unclear"],
    #   "competitors": ["Notion AI", "ChatPDF"],
    #   "market_notes": "EdTech document tools growing ~12% CAGR."
    # }
