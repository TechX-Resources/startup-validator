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


# app/schemas/idea_schema.py
"""
Schemas for startup idea validation.
Week 2: Input validation and response structures.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ValidationStatus(str, Enum):
    """Status of the validation process."""
    PENDING = "pending"
    VALIDATED = "validated"
    REJECTED = "rejected"


class MarketPotential(str, Enum):
    """Market potential rating."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CompetitionLevel(str, Enum):
    """Competition level rating."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IdeaInput(BaseModel):
    """Request body for /validate-idea."""

    idea: str = Field(
        ..., 
        min_length=10, 
        max_length=1000, 
        description="The startup idea to validate (plain text)."
    )
    # Optional: domain, industry, or extra context
    domain: Optional[str] = Field(default=None, max_length=100)
    industry: Optional[str] = Field(default=None, max_length=100)

    @field_validator('idea')
    @classmethod
    def validate_idea_text(cls, v):
        if not v.strip():
            raise ValueError("Idea description cannot be empty or whitespace only")
        return v

    # Example JSON:
    # {"idea": "An AI app that summarizes long PDFs for students in 3 bullet points."}


class IdeaWithContext(IdeaInput):
    """Optional: idea + context from memory (used internally by service/agent)."""
    context_from_memory: List[dict] = Field(default_factory=list)


class ValidationReport(BaseModel):
    """Structured validation report from the agent."""

    idea: str
    validation_status: ValidationStatus = ValidationStatus.VALIDATED
    market_potential: MarketPotential = MarketPotential.MEDIUM
    competition_level: CompetitionLevel = CompetitionLevel.MEDIUM
    key_findings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.0)
    model_used: str
    timestamp: datetime = Field(default_factory=datetime.now)
    validation_id: Optional[str] = None  # For tracking in memory (Week 4)


class APIResponse(BaseModel):
    """Standard HTTP response wrapper."""

    success: bool
    message: str
    data: Optional[dict] = None
    error: Optional[str] = None
    status_code: int = 200

    class Config:
        from_attributes = True
