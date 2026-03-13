# Config (Week 1)

## Purpose
Centralized configuration using Pydantic Settings.

## Environment Variables
- `LLM_PROVIDER`: openai/anthropic
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key  
- `SERPER_API_KEY`: Google search (serper.dev)

## Usage
```python
from app.config import settings
print(settings.VERSION)  # 0.1.0
