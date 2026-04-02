"""
Standalone FastAPI test app for PostgreSQL integration.
Used to verify the startup intelligence database layer.
"""

from fastapi import FastAPI
from app.db.queries import get_top_funded_startups

app = FastAPI(title="Startup DB Test API")


@app.get("/health")
def health():
    return {"status": "ok", "service": "startup-db-test-api"}


@app.get("/db/top-funded")
def fetch_top_funded_startups():
    """
    Returns the top funded startups from PostgreSQL.
    """
    return {
        "source": "postgresql",
        "data": get_top_funded_startups()
    }
