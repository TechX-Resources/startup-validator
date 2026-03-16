from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.schemas.idea import IdeaRequest, IdeaResponse  # Week 2 import
import logging

# Configure logging
logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    yield
    # Shutdown
    logger.info("👋 Shutting down gracefully")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }

@app.post("/validate-idea", response_model=IdeaResponse, status_code=501)
async def validate_idea(request: IdeaRequest):
    """
    Validate startup idea - PLACEHOLDER (Week 5-6 implementation)
    
    TODO Week 5: Replace with agent orchestration
    """
    raise HTTPException(
        status_code=501,
        detail={
            "error": "NotImplementedError",
            "message": "Idea validation agent coming in Week 5-6 🚀",
            "idea_summary": {
                "description": request.idea,
                "status": "placeholder"
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
