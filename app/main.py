from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import IdeaInput, ValidationResponse
from app.services.validation_service import run_validation

app = FastAPI(title="Startup Idea Validator Agent", version="0.2.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "startup-idea-validator-agent", "version": "0.2.0"}

@app.post("/validate-idea", response_model=ValidationResponse)
def validate_idea(body: IdeaInput):
    if not body.idea or len(body.idea.strip()) < 10:
        raise HTTPException(status_code=422, detail="Idea must be at least 10 characters long.")
    try:
        result = run_validation(body.idea)
        return ValidationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")