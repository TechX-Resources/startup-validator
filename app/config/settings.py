from pydantic_settings import BaseSettings
from typing import Optional
from enum import Enum

class LLMProvider(str, Enum):
    AUTO = "auto"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class Settings(BaseSettings):
    # App
    app_name: str = "startup-idea-validator-agent"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # LLM
    llm_provider: LLMProvider = LLMProvider.AUTO
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    # Paths (Week 4+)
    chroma_path: str = "./data/chroma"
    vector_db_path: str = "./data/embeddings"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()
