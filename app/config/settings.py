from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
from enum import Enum

class LLMProvider(str, Enum):
    AUTO = "auto"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    GROK = "grok"
    GEMINI = "gemini"

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    app_name: str = "startup-idea-validator-agent"
    app_version: str = "0.1.0"
    debug: bool = False
    llm_provider: LLMProvider = LLMProvider.AUTO
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    xai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    serper_api_key: Optional[str] = None
    chroma_path: str = "./data/chroma"
    vector_db_path: str = "./data/embeddings"

settings = Settings()