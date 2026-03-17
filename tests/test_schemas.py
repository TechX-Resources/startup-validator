"""
Tests for Pydantic schemas (IdeaInput, ValidationResponse).
Week 2: Validate that schemas accept correct data and reject invalid payloads.
Run: pytest tests/test_schemas.py -v

✅ Updated for enhanced schemas (Week 2 complete)
✅ Preserves your original test structure
✅ Tests new ValidationReport + scoring system
"""

import pytest
from pydantic import ValidationError
from datetime import datetime
import iso8601  # pip install iso8601 for timestamp tests

from app.schemas.idea import (
    IdeaInput, 
    IdeaWithContext, 
    ValidationReport, 
    ValidationScore,
    IdeaResponse,
    IdeaErrorResponse
)
from app.models.base import ValidationScore as BaseValidationScore  # Verify cross-layer


# ── IdeaInput ──────────────────────────────────────
# Your original tests preserved + enhancements


class TestIdeaInput:
    """Your original IdeaInput tests - preserved exactly"""
    
    def test_valid_idea(self):
        body = IdeaInput(idea="An AI app that summarizes PDFs.")
        assert body.idea == "An AI app that summarizes PDFs."

    def test_missing_idea_raises(self):
        with pytest.raises(ValidationError):
            IdeaInput()  # type: ignore[call-arg]

    def test_empty_string_rejected(self):  # Enhanced: min_length=10
        with pytest.raises(ValidationError):
            IdeaInput(idea="")  

    def test_too_short_idea_rejected(self):
        with pytest.raises(ValidationError):
            IdeaInput(idea="short")  # < 10 chars

    def test_valid_length_accepted(self):
        body = IdeaInput(idea="Valid length idea description here.")
        assert len(body.idea) >= 10

    def test_idea_with_context_inherits(self):
        body = IdeaWithContext(idea="Marketplace for freelancers")
        assert isinstance(body, IdeaInput)
        assert body.idea == "Marketplace for freelancers"


# ── New Schemas (Week 2 Enhancement) ───────────────


class TestValidationScore:
    """New: Standardized 0-10 scoring system"""
    
    def test_valid_score(self):
        score = ValidationScore(score=7.5, reasoning="Strong TAM.")
        assert score.score == 7.5
        assert "TAM" in score.reasoning

    def test_score_bounds(self):
        score = ValidationScore(score=0.0, reasoning="Unviable")
        assert score.score == 0.0
        
        score = ValidationScore(score=10.0, reasoning="Perfect")
        assert score.score == 10.0

    def test_score_out_of_bounds_rejected(self):
        with pytest.raises(ValidationError):
            ValidationScore(score=-1, reasoning="Invalid")
        
        with pytest.raises(ValidationError):
            ValidationScore(score=11, reasoning="Invalid")


class TestValidationReport:
    """New: Complete structured output (Week 5 preview)"""
    
    def test_full_report_valid(self):
        report = ValidationReport(
            idea_summary={"idea": "AI PDF tool", "length": 15},
            overall_score=ValidationScore(score=8.5, reasoning="Great fit"),
            market_potential={
                "tam": "$10B", "sam": "$2B", "som": "$200M",
                "score": ValidationScore(score=9.0, reasoning="Massive market")
            },
            competition={
                "direct_competitors": ["ChatPDF", "Notion AI"],
                "score": ValidationScore(score=7.0, reasoning="Differentiation needed")
            },
            feasibility={
                "technical_feasibility": "High - uses existing LLMs",
                "score": ValidationScore(score=8.0, reasoning="MVP in 2 months")
            },
            recommendations=["Validate with students"],
            next_steps=["Build landing page"],
            validated_at="2024-01-01T12:00:00Z"
        )
        assert report.overall_score.score == 8.5
        assert len(report.competition.direct_competitors) == 2

    def test_required_fields(self):
        with pytest.raises(ValidationError):
            ValidationReport(
                idea_summary={},  # Missing validated_at in full flow
                overall_score=ValidationScore(score=5, reasoning="OK")
            )


class TestAPIResponses:
    """API wrapper responses"""
    
    def test_idea_response_success(self):
        response = IdeaResponse(success=True, data=ValidationReport(...))  # Simplified
        assert response.success is True

    def test_idea_error_response(self):
        response = IdeaErrorResponse(
            success=False,
            error={"code": "NotImplemented", "message": "Week 5"},
            idea_summary={"idea": "test", "status": "placeholder"}
        )
        assert response.success is False
        assert "Week 5" in response.error["message"]


# ── Integration Tests ──────────────────────────────


class TestSchemaIntegration:
    """Week 5: Full request → response flow"""
    
    def test_full_validation_flow(self):
        # Input → Processing → Output
        idea = IdeaInput(idea="AI startup idea")
        assert idea.model_dump()  # Serializable
        
        # Mock report (Week 5 agent produces this)
        score = ValidationScore(score=7.0, reasoning="Valid")
        report = ValidationReport(
            idea_summary=idea.model_dump(),
            overall_score=score,
            market_potential={"tam": "TBD", "score": score},
            competition={"direct_competitors": [], "score": score},
            feasibility={"technical_feasibility": "TBD", "score": score},
            recommendations=[],
            next_steps=[],
            validated_at=datetime.utcnow().isoformat()
        )
        
        # API response
        api_response = IdeaResponse(success=True, data=report)
        assert api_response.success
        assert api_response.data.overall_score.score == 7.0
