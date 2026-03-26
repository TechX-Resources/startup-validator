# TODO (Week 1): Load config from env (e.g. os.getenv or pydantic-settings).
# Export: OPENAI_API_KEY, VECTOR_DB_PATH, and any app-level settings.
"""
Config layer — Centralized settings management.
Week 1: Pydantic Settings + .env loading.
Single source of truth for all app configuration.
"""

from .settings import settings, Settings
from typing import Any

__all__ = ["settings", "Settings"]

# Quick access (Week 3+ convenience)
OPENAI_API_KEY = settings.openai_api_key
ANTHROPIC_API_KEY = settings.anthropic_api_key
VECTOR_DB_PATH = settings.vector_db_path
DEBUG = settings.debug

# App metadata
APP_NAME = settings.app_name
APP_VERSION = settings.app_version

def get(key: str, default: Any = None) -> Any:
    """
    Dot-access config helper.
    
    Usage: config.get('llm.provider') or config.get('app.name')
    """
    from pydantic import ValidationError
    
    keys = key.split('.')
    value = settings
    
    for k in keys:
        if hasattr(value, k):
            value = getattr(value, k)
        else:
            return default
    
    return value
