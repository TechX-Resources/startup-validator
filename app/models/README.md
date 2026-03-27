# Models Layer 🧠

**Week 2: LLM Client Abstraction + Base Classes**

Single interface for OpenAI/Claude LLMs. Switch providers with one config change.

## 🎯 Purpose

- **Abstraction**: `LLMClient` interface - swap OpenAI ↔ Claude without code changes
- **Scoring**: Standardized `ValidationScore` across all validation dimensions  
- **Factory**: `LLMFactory.create()` - auto-detects best available provider
- **Type Safety**: Full Pydantic + type hints for agent tooling

# Unit tests
pytest tests/test_models.py

# Connection test (requires API key)
python -c "from app.models import test_connection; test_connection(True)"

# Live test
uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
