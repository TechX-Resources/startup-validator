"""
Response schema — structured validation output. VERY IMPORTANT: keep stable for API and agent.
Week 2: Define; use in agent output and API response.
"""

from pydantic import BaseModel, Field
from typing import List , Optional

class ValidationResponse(BaseModel):
    """Structured validation result returned by the agent and API."""

    score: float = Field(..., ge=0, le=10, description="Overall validation score 0–10.")
    summary: str = Field(..., description="Short summary of the validation.")
    strengths: List[str] = Field(default_factory=list, description="List of strengths.")
    risks: List[str] = Field(default_factory=list, description="List of risks or concerns.")
    competitors: List[str] = Field(default_factory=list, description="Notable competitors or alternatives.")
    market_notes: Optional[str] = Field(None, description="Optional market size or growth notes.")

class Config:
    schema_extra = {
        "example": {
            "score": 7.5,
            "summary": "Strong idea with clear use case; market is crowded.",
            "strengths": ["Clear pain point", "Scalable"],
            "risks": ["Many existing tools", "Monetization unclear"],
            "competitors": ["Notion AI", "ChatPDF"],
            "market_notes": "EdTech document tools growing ~12% CAGR."
        }
    }

    # Example JSON:
    # {
    #   "score": 7.5,
    #   "summary": "Strong idea with clear use case; market is crowded.",
    #   "strengths": ["Clear pain point", "Scalable"],
    #   "risks": ["Many existing tools", "Monetization unclear"],
    #   "competitors": ["Notion AI", "ChatPDF"],
    #   "market_notes": "EdTech document tools growing ~12% CAGR."
    # }

