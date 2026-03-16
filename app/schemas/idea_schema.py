"""
Idea schema — structured input for validation requests.
Week 2: Define; use in main.py and validation_service.
Enhanced with full validation report structure for Week 5-6 agent output.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.models.base import ValidationScore  # Cross-layer reference

# === INPUT SCHEMAS (Your original structure preserved) ===
class IdeaInput(BaseModel):
    """Request body for /validate-idea."""
    
    idea: str = Field(
        ...,
        description="The startup idea to validate (plain text).",
        min_length=10,
        max_length=2000
    )
    
    # Optional: domain, industry, or extra context (uncomment when needed)
    # domain: Optional[str] = Field(None, description="Problem domain")
    # industry: Optional[str] = Field(None, description="Target industry")
    # founder_experience: Optional[str] = Field(None, description="Your background")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "idea": "An AI app that summarizes long PDFs for students in 3 bullet points.",
                    "domain": "EdTech",
                    "industry": "AI Tools"
                }
            ]
        }
    }


class IdeaWithContext(IdeaInput):
    """
    Optional: idea + context from memory (used internally by service/agent).
    Week 4+: Populated from vector store / session memory.
    """
    # context_from_memory: List[Dict[str, Any]] = Field(
    #     default_factory=list,
    #     description="Relevant past ideas / market data from memory"
    # )
    session_id: Optional[str] = Field(None, description="Session tracking")

# === VALIDATION OUTPUT SCHEMAS (New - Week 2 enhancement) ===
class MarketPotential(BaseModel):
    """Market size estimation (Week 3 tool output)"""
    tam: str  # Total Addressable Market
    sam: str  # Serviceable Addressable Market  
    som: str  # Serviceable Obtainable Market
    growth_rate: Optional[str] = None
    score: ValidationScore

class CompetitionAnalysis(BaseModel):
    """Competitor landscape (Week 3 tool output)"""
    direct_competitors: List[str] = Field(default_factory=list)
    indirect_competitors: List[str] = Field(default_factory=list)
    competitive_moat: str
    score: ValidationScore

class FeasibilityAssessment(BaseModel):
    """Technical & execution feasibility (Week 5 agent reasoning)"""
    technical_feasibility: str
    execution_risk: str
    time_to_mvp: str
    score: ValidationScore

class ValidationReport(BaseModel):
    """Complete structured validation output (Week 5-6 final response)"""
    idea_summary: Dict[str, Any]
    overall_score: ValidationScore
    market_potential: MarketPotential
    competition: CompetitionAnalysis
    feasibility: FeasibilityAssessment
    recommendations: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
    validated_at: str = Field(..., description="ISO timestamp")

# === API RESPONSE WRAPPERS ===
class IdeaResponse(BaseModel):
    """Success response for /validate-idea"""
    success: bool = True
    data: ValidationReport

class IdeaErrorResponse(BaseModel):
    """Error response for /validate-idea"""
    success: bool = False
    error: Dict[str, str]
    idea_summary: Dict[str, str]  # Echo back for debugging

# === BACKWARD COMPATIBILITY ALIASES ===
# Your main.py can use these - no breaking changes!
IdeaRequest = IdeaInput      # For main.py endpoint
IdeaValidationResponse = IdeaResponse
ValidationErrorResponse = IdeaErrorResponse
