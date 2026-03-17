# Models Layer 🧠

**Week 2: LLM Client Abstraction + Base Classes**

Single interface for OpenAI/Claude LLMs. Switch providers with one config change.

## 🎯 Purpose

- **Abstraction**: `LLMClient` interface - swap OpenAI ↔ Claude without code changes
- **Scoring**: Standardized `ValidationScore` across all validation dimensions  
- **Factory**: `LLMFactory.create()` - auto-detects best available provider
- **Type Safety**: Full Pydantic + type hints for agent tooling

## 🏗️ Architecture

