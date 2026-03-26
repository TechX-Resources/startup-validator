"""
Validation service — connects API to validator agent and memory.
"""

from __future__ import annotations

import re

from app.agents.validator_agent import run_validator


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def run_validation(idea: str, user_id: str | None = None, session_id: str | None = None) -> dict:
    """
    Run the validation pipeline and return a response-schema compatible dict.
    """
    normalized_idea = _normalize_text(idea)
    if not normalized_idea:
        raise ValueError("Idea cannot be empty.")

    # TODO (memory phase): pull context by user_id/session_id and pass to validator.
    context = None

    result = run_validator(normalized_idea, context=context)

    # TODO (memory phase): persist result with memory store.
    return result
