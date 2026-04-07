from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import RequestLoggingMiddleware
from app.schemas import IdeaInput, ValidationResponse
from app.tools.competitor_finder import competitor_finder
from app.tools.market_estimator import market_estimator

app = FastAPI(title="Startup Idea Validator Agent", version="0.2.0")

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _viability_score(competitors: list[dict], market: dict) -> float:
    """
    Multi-factor viability score (0-10).
    Higher market TAM + lower competition + lower similarity = higher score.
    """
    score = 5.0

    # Competition level
    competition = market.get("competition", "Medium")
    score += {"Low": 2.0, "Medium": 0.0, "High": -1.5}.get(competition, 0)

    # Penalise for very close competitors
    high_sim = sum(1 for c in competitors if c.get("similarity_score", 0) > 0.35)
    score -= high_sim * 1.0

    # Reward high success rate in this industry
    insights = market.get("dataset_insights", {})
    success_rate = insights.get("success_rate_pct", 0)
    score += (success_rate / 100) * 2.0

    # Reward VC-backed presence (validated market)
    vc_ratio = insights.get("vc_backed", 0) / max(insights.get("total_companies", 1), 1)
    score += vc_ratio * 1.5

    return round(max(1.0, min(score, 10.0)), 1)


def _llm_summary(idea: str, industry: str, market: dict, competitors: list[dict]) -> str | None:
    """Generate a summary using Groq LLM if API key is available."""
    try:
        from app.models.llm_client import LLMClient
        llm = LLMClient()
        prompt = (
            f"Startup idea: {idea}\n"
            f"Industry: {industry}\n"
            f"Market: TAM {market['tam']}, Growth {market['growth']}, Competition {market['competition']}\n"
            f"Top competitors: {', '.join(c['name'] for c in competitors[:3])}\n\n"
            "Write one concise sentence summarising the market opportunity and main challenge."
        )
        return llm.chat([{"role": "user", "content": prompt}])
    except Exception:
        return None


@app.get("/health")
def health():
    return {"status": "ok", "service": "startup-idea-validator-agent", "version": "0.2.0"}


@app.post("/validate-idea", response_model=ValidationResponse)
def validate_idea(body: IdeaInput):
    if not body.idea or len(body.idea.strip()) < 10:
        raise HTTPException(status_code=422, detail="Idea must be at least 10 characters long.")
    try:
        competitors = competitor_finder(body.idea)
        industry = competitors[0]["industry"] if competitors else "unknown"
        market = market_estimator(industry)
        score = _viability_score(competitors, market)

        # Try LLM summary, fall back to template
        summary = _llm_summary(body.idea, industry, market, competitors)
        if not summary:
            summary = (
                f"Your idea competes in the {industry} space with a "
                f"{market['tam']} market growing at {market['growth']}."
            )

        insights = market["dataset_insights"]
        return ValidationResponse(
            score=score,
            summary=summary,
            strengths=[
                f"Market size: {market['tam']}",
                f"Growth rate: {market['growth']}",
                f"Industry success rate: {insights.get('success_rate_pct', 0)}% (acquired or IPO)",
                f"VC-backed companies in space: {insights.get('vc_backed', 0)}",
            ],
            risks=[
                f"Found {len(competitors)} similar companies already in this space",
                f"Closest match: {competitors[0]['name']} (similarity: {competitors[0]['similarity_score']})" if competitors else "",
                f"Competition level: {market['competition']}",
            ],
            competitors=[c["name"] for c in competitors],
            market_notes=(
                f"TAM: {market['tam']}, Growth: {market['growth']}. "
                f"{insights.get('total_companies', 0)} companies tracked in dataset. "
                f"Avg funding: ${insights.get('avg_funding_usd', 0):,}."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Validation failed. Please try again.")
