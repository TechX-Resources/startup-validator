from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and/or .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # LLM provider (Google Gemini)
    gemini_api_key: str = Field(default="", description="API Key for Google Gemini")

    # LLM provider (OpenAI)
    openai_api_key: str = Field(default="", description="API Key for OpenAI")

    # LLM provider (Anthropic)
    anthropic_api_key: str = Field(default="", description="API Key for Anthropic")

    # Vector DB path for embeddings
    vector_db_path: str = Field(default="./data/embeddings", description="Path to local vector database")


# Create a global instance of settings so we can imported across the app
settings = Settings()
