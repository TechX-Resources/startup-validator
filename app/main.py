"""
Startup Idea Validator Agent — FastAPI application entry point.
Week 1: Basic skeleton; Week 5–6: wire up validation service.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import RequestLoggingMiddleware
from app.schemas import IdeaInput, ValidationResponse
from app.services import run_validation

app = FastAPI(
    title="Startup Idea Validator Agent",
    description="API for validating startup ideas using MCP-style agent (Model + Context + Tools + Orchestration).",
    version="0.1.0",
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health check for deployment and load balancers."""
    return {"status": "ok", "service": "startup-idea-validator-agent"}


@app.post("/validate-idea", response_model=ValidationResponse)
def validate_idea(body: IdeaInput):
    """
    Validate a startup idea and return a structured report.
    """
    try:
        return run_validation(body.idea)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Validation failed unexpectedly.") from exc
