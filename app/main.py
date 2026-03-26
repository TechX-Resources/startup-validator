from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import RequestLoggingMiddleware
from app.schemas import IdeaInput, ValidationResponse
from app.services import run_validation

app = FastAPI(title="Startup Idea Validator Agent", version="0.2.0")

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "startup-idea-validator-agent",
        "status": "ok",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "validate": "/validate-idea",
        },
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "startup-idea-validator-agent", "version": "0.2.0"}

@app.post("/validate-idea", response_model=ValidationResponse)
def validate_idea(body: IdeaInput):
    try:
        return run_validation(body.idea)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Validation failed unexpectedly.") from exc
