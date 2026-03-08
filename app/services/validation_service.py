"""
Validation service — connects API to validator agent and memory.
Week 5–6: Implemented with AI-powered validation.
"""

from __future__ import annotations

import re
from app.agents.validator_agent import run_validator


KEYWORD_SIGNALS: dict[str, float] = {
    "ai": 0.7,
    "automation": 0.5,
    "b2b": 0.4,
    "saas": 0.5,
    "students": 0.3,
    "health": 0.3,
    "fintech": 0.3,
    "marketplace": 0.2,
    "api": 0.2,
    "subscription": 0.3,
}

RISK_TRIGGERS: dict[str, str] = {
    "social": "Customer acquisition can be expensive in social products.",
    "crypto": "Regulatory volatility may impact launch and growth.",
    "health": "Compliance and data privacy obligations can slow execution.",
    "fintech": "Licensing and compliance requirements may increase go-to-market time.",
    "marketplace": "Two-sided marketplaces often face a cold-start liquidity problem.",
}

COMPETITOR_MAP: dict[str, list[str]] = {
    "pdf": ["ChatPDF", "Humata", "Adobe Acrobat AI Assistant"],
    "education": ["Quizlet", "Khan Academy", "Notion AI"],
    "students": ["Notion AI", "Grammarly", "ChatGPT"],
    "health": ["Ada Health", "K Health", "Teladoc"],
    "fintech": ["Stripe", "Wise", "Plaid"],
    "marketplace": ["Etsy", "Upwork", "Fiverr"],
    "saas": ["Notion", "Airtable", "Zapier"],
}


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def _keyword_hits(idea: str, lookup: dict[str, object]) -> list[str]:
    lower = idea.lower()
    return [key for key in lookup if key in lower]


def _build_strengths(idea: str, score: float) -> list[str]:
    strengths: list[str] = []
    lower = idea.lower()

    if any(token in lower for token in ("for", "helps", "solve", "pain")):
        strengths.append("Clear target user and problem framing.")

    if any(token in lower for token in ("ai", "automation", "assistant", "copilot")):
        strengths.append("Automation angle can reduce user effort and increase retention.")

    if any(token in lower for token in ("b2b", "teams", "business", "company", "enterprise")):
        strengths.append("B2B positioning can support stronger monetization potential.")

    if score >= 7.5:
        strengths.append("Idea appears actionable with a practical MVP path.")
    elif score >= 6:
        strengths.append("Concept has promise if positioned around a narrow niche.")

    if not strengths:
        strengths.append("Concept is understandable and can be tested with a lightweight MVP.")

    return strengths[:4]


def _build_risks(idea: str, score: float) -> list[str]:
    risks: list[str] = []
    lower = idea.lower()

    for trigger, message in RISK_TRIGGERS.items():
        if trigger in lower:
            risks.append(message)

    if len(idea.split()) < 8:
        risks.append("Idea description is short; unclear scope can hurt execution and prioritization.")

    if score < 6:
        risks.append("Differentiation is not obvious yet; competitors may already solve similar needs.")

    risks.append("Validation currently uses heuristic scoring; verify with customer interviews and landing-page tests.")
    return risks[:4]


def _build_competitors(idea: str) -> list[str]:
    matches = _keyword_hits(idea, COMPETITOR_MAP)
    competitors: list[str] = []
    for key in matches:
        competitors.extend(COMPETITOR_MAP[key])

    deduped: list[str] = []
    for name in competitors:
        if name not in deduped:
            deduped.append(name)

    if not deduped:
        deduped = ["Generic incumbent alternatives", "DIY spreadsheet workflows"]

    return deduped[:5]


def _estimate_score(idea: str) -> float:
    lower = idea.lower()
    word_count = len(idea.split())

    score = 4.8
    score += min(word_count / 40, 1.0) * 1.4

    for keyword, weight in KEYWORD_SIGNALS.items():
        if keyword in lower:
            score += weight

    if "for" in lower:
        score += 0.4

    return round(max(0.0, min(10.0, score)), 1)


def run_validation(idea: str, user_id: str = None, session_id: str = None) -> dict:
    """
    Run full validation pipeline: optional context from memory → agent → optional save to memory → response.
    idea: Raw text of the startup idea.
    user_id / session_id: Optional, for memory lookup and storage.
    Returns: Dict matching response_schema (see app/schemas/response_schema.py).
    """
    normalized_idea = _normalize_text(idea)
    if not normalized_idea:
        raise ValueError("Idea cannot be empty.")

    # TODO (Week 4): Retrieve context from memory if user_id/session_id provided
    context = None
    
    # Run AI-powered validation
    result = run_validator(normalized_idea, context=context)
    
    # TODO (Week 4): Save result to memory if needed
    # memory_store.save(normalized_idea, result)
    
    return result


# ═══════════════════════════════════════════════════════════════
# Legacy heuristic functions (kept for reference/fallback)
# ═══════════════════════════════════════════════════════════════

