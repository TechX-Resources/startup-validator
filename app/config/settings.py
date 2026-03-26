from pydantic_settings import BaseSettings, SettingsConfigDict
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
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_openai_deployment_name: Optional[str] = None
    azure_openai_embedding_deployment: Optional[str] = None
    
    # Paths (Week 4+)
    chroma_path: str = "./data/chroma"
    vector_db_path: str = "./data/embeddings"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()
