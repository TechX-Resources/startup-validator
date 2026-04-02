"""
Response schema — structured validation output.

VERY IMPORTANT:
This schema defines the contract between:
- the validator agent
- the API
- the frontend UI

Keep these fields stable once the frontend depends on them.

Week 2: Define
Weeks 3–6: Used by agent, services, and API responses.

Example JSON response:

{
  "score": 7.5,
  "summary": "Strong idea addressing a real student pain point. However, the space already has several competitors.",
  "strengths": [
    "Clear user problem",
    "Large student market",
    "AI summarization already proven"
  ],
  "risks": [
    "High competition",
    "Difficult differentiation"
  ],
  "competitors": [
    "ChatPDF",
    "Humata AI",
    "Notion AI"
  ],
  "market_notes": "AI productivity tools in education are growing rapidly with increasing demand for study assistance."
}
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class ValidationResponse(BaseModel):
    """
    Structured validation result returned by the validator agent and API.

    This model ensures the AI output is predictable and safe for the frontend.
    """

    # Pydantic configuration
    model_config = ConfigDict(
        extra="ignore",  # Ignore unexpected LLM fields
        json_schema_extra={
            "example": {
                "score": 7.5,
                "summary": "Strong idea addressing a real student pain point. However, the space already has several competitors.",
                "strengths": [
                    "Clear user problem",
                    "Large student market"
                ],
                "risks": [
                    "High competition",
                    "Difficult differentiation"
                ],
                "competitors": [
                    "ChatPDF",
                    "Humata AI"
                ],
                "market_notes": "AI tools for academic productivity are growing rapidly."
            }
        }
    )

    score: float = Field(
        ...,
        ge=0,
        le=10,
        description="Overall startup viability score between 0 and 10."
    )

    summary: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="High-level explanation of the idea's viability."
    )

    strengths: List[str] = Field(
        default_factory=list,
        description="Key strengths or advantages of the startup idea."
    )

    risks: List[str] = Field(
        default_factory=list,
        description="Potential risks, weaknesses, or execution challenges."
    )

    competitors: List[str] = Field(
        default_factory=list,
        description="Known competitors or existing alternatives in the market."
    )

    market_notes: Optional[str] = Field(
        None,
        description="Additional insights about market size, trends, or growth."
    )