"""
SQLite storage layer for the startup dataset.
Replaces JSON file storage with a queryable database.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("data/processed/startups.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the startups table if it doesn't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS startups (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name    TEXT NOT NULL,
                industry        TEXT NOT NULL,
                description     TEXT,
                founded_year    INTEGER,
                status          TEXT,
                funding_total   REAL,
                funding_rounds  REAL,
                has_vc          INTEGER,
                is_top500       INTEGER
            )
        """)


def save_records(records: list[dict]):
    """Wipe and reload all startup records into SQLite."""
    init_db()
    with get_conn() as conn:
        conn.execute("DELETE FROM startups")
        conn.executemany("""
            INSERT INTO startups
                (company_name, industry, description, founded_year,
                 status, funding_total, funding_rounds, has_vc, is_top500)
            VALUES
                (:company_name, :industry, :description, :founded_year,
                 :status, :funding_total, :funding_rounds, :has_vc, :is_top500)
        """, [
            {
                "company_name":  r["company_name"],
                "industry":      r["industry"],
                "description":   r.get("description"),
                "founded_year":  r.get("founded_year"),
                "status":        r.get("status"),
                "funding_total": r.get("funding_total"),
                "funding_rounds":r.get("funding_rounds"),
                "has_vc":        int(r["has_VC"]) if r.get("has_VC") is not None else None,
                "is_top500":     int(r["is_top500"]) if r.get("is_top500") is not None else None,
            }
            for r in records
        ])


def query_all() -> list[dict]:
    """Return all startups as a list of dicts."""
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM startups").fetchall()
    return [dict(r) for r in rows]


def query_by_industry(industry: str) -> list[dict]:
    """Return startups filtered by industry."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM startups WHERE LOWER(industry) = LOWER(?)", (industry,)
        ).fetchall()
    return [dict(r) for r in rows]


def industry_stats(industry: str) -> dict:
    """Aggregate funding and success stats for an industry."""
    with get_conn() as conn:
        row = conn.execute("""
            SELECT
                COUNT(*)                                        AS total,
                AVG(funding_total)                              AS avg_funding,
                SUM(CASE WHEN status IN ('acquired','ipo')
                         THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS success_rate,
                SUM(has_vc)                                     AS vc_backed
            FROM startups
            WHERE LOWER(industry) = LOWER(?)
        """, (industry,)).fetchone()
    return {
        "total_companies":  row["total"] or 0,
        "avg_funding_usd":  round(row["avg_funding"] or 0),
        "success_rate_pct": round(row["success_rate"] or 0, 1),
        "vc_backed":        row["vc_backed"] or 0,
    }
