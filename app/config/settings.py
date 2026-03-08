from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    """
    Application Configuration.
    Loads settings from environment variables with type safety.
    """
    # App Info
    app_name: str = "Startup Idea Validator Agent"
    app_env: str = "development"
    debug: bool = True

    # LLM Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Vector DB Configuration
    vector_db_path: str = "./data/chroma_db"

    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8000

    # Feature Flags
    enable_web_search: bool = False
    enable_competitor_analysis: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the settings.
    Ensures settings are loaded only once per process.
    """
    return Settings()

# Create a global instance for easy import in main.py
settings = get_settings()
