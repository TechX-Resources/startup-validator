"""
Batch re-scoring and anomaly detection for the startup dataset.

Batch re-scoring: re-evaluates all startups in SQLite against the current
scoring model and stores scores — enables version-controlled model comparisons.

Anomaly detection: flags startups with outlier funding values using
standard deviation — reduces manual QA on ingestion.
"""

import sqlite3
import statistics
from datetime import datetime, UTC
from pathlib import Path
from app.services.startup_db import get_conn, init_db

SCORES_DB = Path("data/processed/startups.db")


def _ensure_scores_table():
    """Add scores table to SQLite if it doesn't exist."""
    init_db()
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS startup_scores (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name  TEXT NOT NULL,
                industry      TEXT NOT NULL,
                score         REAL,
                model_version TEXT,
                scored_at     TEXT
            )
        """)


def batch_rescore(model_version: str = "v1") -> dict:
    """
    Re-score all startups in SQLite using funding + status signals.
    Stores results in startup_scores table for model version comparison.
    """
    _ensure_scores_table()

    with get_conn() as conn:
        startups = conn.execute("SELECT * FROM startups").fetchall()

    scored = []
    for s in startups:
        score = 5.0
        # Reward successful outcomes
        if s["status"] in ("acquired", "ipo"):
            score += 2.0
        elif s["status"] == "closed":
            score -= 2.0
        # Reward VC backing
        if s["has_vc"]:
            score += 1.0
        # Reward top 500
        if s["is_top500"]:
            score += 1.5
        # Reward funding
        if s["funding_total"] and s["funding_total"] > 1_000_000:
            score += 0.5

        score = round(max(1.0, min(score, 10.0)), 1)
        scored.append((s["company_name"], s["industry"], score, model_version, datetime.now(UTC).isoformat()))

    with get_conn() as conn:
        conn.execute("DELETE FROM startup_scores WHERE model_version = ?", (model_version,))
        conn.executemany(
            "INSERT INTO startup_scores (company_name, industry, score, model_version, scored_at) VALUES (?,?,?,?,?)",
            scored
        )

    print(f"\n--- Batch Re-scoring ({model_version}) ---")
    print(f"  Scored {len(scored)} companies")
    avg = round(sum(s[2] for s in scored) / len(scored), 2) if scored else 0
    print(f"  Average score: {avg}")
    return {"model_version": model_version, "total_scored": len(scored), "avg_score": avg}


def detect_anomalies(threshold_std: float = 2.0) -> list[dict]:
    """
    Flag startups with funding values more than threshold_std standard deviations
    from the industry mean. Returns list of anomalous records.
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT company_name, industry, funding_total FROM startups WHERE funding_total IS NOT NULL"
        ).fetchall()

    # Group funding by industry
    by_industry: dict[str, list] = {}
    for r in rows:
        by_industry.setdefault(r["industry"], []).append((r["company_name"], r["funding_total"]))

    anomalies = []
    for industry, companies in by_industry.items():
        if len(companies) < 3:
            continue
        values = [c[1] for c in companies]
        mean = statistics.mean(values)
        std = statistics.stdev(values)
        if std == 0:
            continue
        for name, funding in companies:
            z_score = abs(funding - mean) / std
            if z_score > threshold_std:
                anomalies.append({
                    "company_name": name,
                    "industry":     industry,
                    "funding_total": funding,
                    "industry_mean": round(mean),
                    "z_score":      round(z_score, 2),
                    "flagged_at":   datetime.now(UTC).isoformat(),
                })

    print(f"\n--- Anomaly Detection ---")
    print(f"  Flagged {len(anomalies)} outlier records (z-score > {threshold_std})")
    for a in anomalies[:5]:
        print(f"  {a['company_name']} ({a['industry']}): ${a['funding_total']:,.0f} — z={a['z_score']}")

    return anomalies


if __name__ == "__main__":
    batch_rescore("v1")
    detect_anomalies()
