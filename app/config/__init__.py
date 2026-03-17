
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
