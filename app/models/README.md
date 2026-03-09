# app/models

**Purpose:** LLM interaction layer — abstraction for model calls so you can swap OpenAI/Claude without changing agent code.

**What students will implement:**
- A single client class/interface that:
  - Accepts a prompt (and optional system message).
  - Calls the chosen LLM API (OpenAI or Claude).
  - Returns raw text or structured output (e.g. JSON) for the agent to use.
- Handle errors and timeouts; no real API keys in repo (use env).

**Weeks:** 2.

**Files:** `llm_client.py` — placeholder class with TODOs.

# Models Layer (`app/models`)

**Week:** 2 (Models + LLM Client)
**Purpose:** LLM client abstraction and schema definitions.

## Overview
This layer provides:
- **LLM Client Abstraction**: Support for multiple LLM providers (OpenAI, Claude)
- **Schema Definitions**: Pydantic models for input/output validation
- **Prompt Templates**: Reusable prompts for validation tasks

## Key Files
- `llm_client.py`: LLM client abstraction with OpenAI/Claude support
- `idea_schema.py`: Input/output schemas for startup ideas
- `response_schema.py`: Standard API response wrapper
- `prompts/`: Prompt templates for validation

## Usage
```python
from app.models import default_llm_client

## Simple chat
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]
response = default_llm_client.chat(messages)
print(response)

##Switch provider
claude_client = LLMClientFactory.create_client("claude")
