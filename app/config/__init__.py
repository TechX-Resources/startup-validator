# TODO (Week 1): Load config from env (e.g. os.getenv or pydantic-settings).
# Export: OPENAI_API_KEY, VECTOR_DB_PATH, and any app-level settings.

"""
Configuration module for the Startup Idea Validator Agent.
Exports all configuration settings for use across the application.

Week 1: Load config from environment variables (pydantic-settings).
Exports: OPENAI_API_KEY, VECTOR_DB_PATH, and app-level settings.
"""

from .settings import Settings, get_settings, settings

# Export all configuration values
__all__ = [
    "Settings",
    "get_settings",
    "settings",
    # App-level settings
    "APP_NAME",
    "APP_VERSION",
    "DEBUG",
    "HOST",
    "PORT",
    # External service settings
    "OPENAI_API_KEY",
    "VECTOR_DB_PATH",
    # Feature flags
    "ENABLE_SEARCH_TOOL",
    "ENABLE_COMPETITOR_TOOL",
]

# Re-export individual settings for convenience
APP_NAME: str = settings.APP_NAME
APP_VERSION: str = settings.APP_VERSION
DEBUG: bool = settings.DEBUG
HOST: str = settings.HOST
PORT: int = settings.PORT
OPENAI_API_KEY: str | None = settings.OPENAI_API_KEY
VECTOR_DB_PATH: str = settings.CHROMA_DB_PATH
ENABLE_SEARCH_TOOL: bool = settings.ENABLE_SEARCH_TOOL
ENABLE_COMPETITOR_TOOL: bool = settings.ENABLE_COMPETITOR_TOOL
