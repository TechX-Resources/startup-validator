from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.middleware import RequestLoggingMiddleware
from app.schemas import IdeaInput, ValidationResponse
from app.services.validation_service import run_validation
from app.utils.validators import sanitize_idea, validate_idea_length

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Startup Idea Validator Agent", version="0.3.0")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests. Please slow down."})

@app.get("/health")
def health():
    return {"status": "ok", "service": "startup-idea-validator-agent", "version": "0.3.0"}

@app.post("/validate-idea", response_model=ValidationResponse)
@limiter.limit("10/minute")
async def validate_idea(request: Request, body: IdeaInput):
    try:
        idea = sanitize_idea(body.idea)
        idea = validate_idea_length(idea)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    try:
        result = run_validation(idea)
        return ValidationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Validation failed. Please try again.")