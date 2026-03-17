# Config Layer ⚙️

**Week 1: Environment Configuration**

Centralized settings management. Load API keys, paths, feature flags from `.env`.

## 🎯 Purpose

- **Secrets**: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` (never in code)
- **Paths**: `VECTOR_DB_PATH` (Week 4 Chroma DB)
- **Flags**: `DEBUG`, `LOG_LEVEL` 
- **App**: `APP_NAME`, `APP_VERSION`

**MCP Layer**: Shared across **Model**, **Context**, **Tools**

## 🏗️ What Students Implement (Week 1)

```python
# app/config/__init__.py - Your TODO
import os

# Load from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/chroma")

# App settings  
APP_NAME = os.getenv("APP_NAME", "startup-idea-validator-agent")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
**Test**
python -c "from app.config import OPENAI_API_KEY; print('✅ Config OK')"
