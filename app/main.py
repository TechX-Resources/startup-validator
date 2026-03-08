"""
Startup Idea Validator Agent — FastAPI application entry point.
Week 1: Basic skeleton; Week 5–6: wire up validation service.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import RequestLoggingMiddleware
from app.schemas import IdeaInput, ValidationResponse

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
    Validate a startup idea. Placeholder until Week 5–6.
    TODO: Call validation_service.run_validation(body.idea) and return ValidationResponse.
    """
    # TODO (Week 5–6): return run_validation(body.idea)
    raise HTTPException(status_code=501, detail="Not implemented yet. Wire validation_service in Week 5–6.")


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    print(f"Starting {settings.app_name} in {settings.app_env} mode...")
    print(f"Debug Mode: {settings.debug}")
    print(f"Server: {settings.host}:{settings.port}")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    print(f"Shutting down {settings.app_name}...")
