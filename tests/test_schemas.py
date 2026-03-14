"""
Tests for Pydantic schemas (IdeaInput, ValidationResponse).
Week 2: Validate that schemas accept correct data and reject invalid payloads.
Run: pytest tests/test_schemas.py -v
"""

import pytest
from pydantic import ValidationError

from app.schemas.idea_schema import IdeaInput, IdeaWithContext
from app.schemas.response_schema import ValidationResponse


# ── IdeaInput ──────────────────────────────────────


class TestIdeaInput:
    def test_valid_idea(self):
        body = IdeaInput(idea="An AI app that summarizes PDFs.")
        assert body.idea == "An AI app that summarizes PDFs."

    def test_missing_idea_raises(self):
        with pytest.raises(ValidationError):
            IdeaInput()  # type: ignore[call-arg]

    def test_empty_string_accepted(self):
        body = IdeaInput(idea="")
        assert body.idea == ""

    def test_idea_with_context_inherits(self):
        body = IdeaWithContext(idea="Marketplace for freelancers")
        assert isinstance(body, IdeaInput)


# ── ValidationResponse ─────────────────────────────


class TestValidationResponse:
    def test_valid_full_response(self):
        resp = ValidationResponse(
            score=7.5,
            summary="Strong idea with clear use case.",
            strengths=["Clear pain point", "Scalable"],
            risks=["Crowded market"],
            competitors=["Notion AI", "ChatPDF"],
            market_notes="EdTech ~12% CAGR",
        )
        assert resp.score == 7.5
        assert len(resp.strengths) == 2
        assert resp.market_notes is not None

    def test_defaults_for_optional_lists(self):
        resp = ValidationResponse(score=5.0, summary="Decent idea.")
        assert resp.strengths == []
        assert resp.risks == []
        assert resp.competitors == []
        assert resp.market_notes is None

    def test_score_lower_bound(self):
        resp = ValidationResponse(score=0, summary="Unviable.")
        assert resp.score == 0

    def test_score_upper_bound(self):
        resp = ValidationResponse(score=10, summary="Perfect.")
        assert resp.score == 10

    def test_score_below_zero_raises(self):
        with pytest.raises(ValidationError):
            ValidationResponse(score=-1, summary="Bad.")

    def test_score_above_ten_raises(self):
        with pytest.raises(ValidationError):
            ValidationResponse(score=11, summary="Impossible.")

    def test_missing_required_fields_raises(self):
        with pytest.raises(ValidationError):
            ValidationResponse()  # type: ignore[call-arg]

    def test_market_notes_null_accepted(self):
        resp = ValidationResponse(score=6.0, summary="OK.", market_notes=None)
        assert resp.market_notes is None
