from dotenv import load_dotenv
load_dotenv()

import uuid
import threading
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import RequestLoggingMiddleware
from app.schemas import IdeaInput, ValidationResponse
from app.tools.competitor_finder import competitor_finder
from app.tools.market_estimator import market_estimator
from app.services.scoring import batch_rescore, detect_anomalies

# In-memory job store: {job_id: {"status": "...", "result": ...}}
_jobs: dict = {}

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


def _llm_summary(idea: str, industry: str, market: dict, competitors: list[dict], score: float) -> str | None:
    """Generate a data-driven summary using all pipeline signals."""
    try:
        from app.models.llm_client import LLMClient
        llm = LLMClient()
        insights = market.get("dataset_insights", {})
        top_competitor = competitors[0] if competitors else {}
        prompt = f"""You are a startup analyst. Analyze this startup idea using the data below and give a clear, honest 2-3 sentence verdict on whether it's viable.

Startup idea: {idea}

Data:
- Industry: {industry}
- Market size (TAM): {market.get('tam', 'Unknown')}
- Market growth rate: {market.get('growth', 'Unknown')}
- Competition level: {market.get('competition', 'Unknown')}
- Viability score: {score}/10
- Companies already in this space: {insights.get('total_companies', 0)}
- Industry success rate (acquired or IPO): {insights.get('success_rate_pct', 0)}%
- Average funding raised in this industry: ${insights.get('avg_funding_usd', 0):,}
- VC-backed companies in space: {insights.get('vc_backed', 0)}
- Closest competitor: {top_competitor.get('name', 'None')} (similarity score: {top_competitor.get('similarity_score', 0)})

Using ALL of this data, write 2-3 sentences that:
1. State whether this idea is viable and why based on the numbers
2. Mention the biggest opportunity signal from the data
3. Mention the biggest risk signal from the data

Be specific and reference the actual numbers. Do not be generic."""

        return llm.chat([{"role": "user", "content": prompt}])
    except Exception:
        return None


def _run_validation_job(job_id: str, idea: str):
    """Runs validation in a background thread and stores result in _jobs."""
    try:
        competitors = competitor_finder(idea)
        industry = competitors[0]["industry"] if competitors else "unknown"
        market = market_estimator(industry)
        score = _viability_score(competitors, market)
        summary = _llm_summary(idea, industry, market, competitors, score) or (
            f"Your idea competes in the {industry} space with a "
            f"{market['tam']} market growing at {market['growth']}."
        )
        insights = market["dataset_insights"]
        _jobs[job_id]["result"] = ValidationResponse(
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
                f"{insights.get('total_companies', 0)} companies tracked. "
                f"Avg funding: ${insights.get('avg_funding_usd', 0):,}."
            ),
        )
        _jobs[job_id]["status"] = "done"
    except Exception:
        _jobs[job_id]["status"] = "failed"


@app.get("/scores")
def get_scores(model_version: str = "v1"):
    """Return batch re-scoring results for all startups."""
    from app.services.startup_db import get_conn
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM startup_scores WHERE model_version = ? ORDER BY score DESC",
            (model_version,)
        ).fetchall()
    return {"model_version": model_version, "total": len(rows), "scores": [dict(r) for r in rows]}


@app.get("/anomalies")
def get_anomalies(threshold: float = 2.0):
    """Return funding anomalies flagged by z-score outlier detection."""
    anomalies = detect_anomalies(threshold_std=threshold)
    return {"total_flagged": len(anomalies), "anomalies": anomalies}


@app.post("/rescore")
def rescore(model_version: str = "v1"):
    """Trigger a batch re-score of all startups against the current scoring model."""
    result = batch_rescore(model_version)
    return result


@app.get("/stats")
def stats():
    """High-level dataset statistics — pipeline health at a glance."""
    from app.services.startup_db import get_conn
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM startups").fetchone()[0]
        industries = conn.execute("SELECT COUNT(DISTINCT industry) FROM startups").fetchone()[0]
        avg_funding = conn.execute("SELECT AVG(funding_total) FROM startups WHERE funding_total IS NOT NULL").fetchone()[0]
        vc_backed = conn.execute("SELECT COUNT(*) FROM startups WHERE has_vc = 1").fetchone()[0]
        acquired = conn.execute("SELECT COUNT(*) FROM startups WHERE status = 'acquired'").fetchone()[0]
        top500 = conn.execute("SELECT COUNT(*) FROM startups WHERE is_top500 = 1").fetchone()[0]
    return {
        "total_companies":   total,
        "industries_tracked": industries,
        "avg_funding_usd":   round(avg_funding or 0),
        "vc_backed":         vc_backed,
        "acquired_or_ipo":   acquired,
        "top500_companies":  top500,
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "startup-idea-validator-agent", "version": "0.2.0"}


@app.post("/validate-idea/async")
def validate_idea_async(body: IdeaInput):
    """Submit a validation job — returns job_id immediately, runs in background."""
    if not body.idea or len(body.idea.strip()) < 10:
        raise HTTPException(status_code=422, detail="Idea must be at least 10 characters long.")
    job_id = str(uuid.uuid4())
    _jobs[job_id] = {"status": "processing", "result": None}
    thread = threading.Thread(target=_run_validation_job, args=(job_id, body.idea))
    thread.start()
    return {"job_id": job_id, "status": "processing"}


@app.get("/job/{job_id}")
def get_job(job_id: str):
    """Poll for async validation result by job_id."""
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job["status"] == "done":
        return {"status": "done", "result": job["result"]}
    return {"status": job["status"]}


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
        summary = _llm_summary(body.idea, industry, market, competitors, score)
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
