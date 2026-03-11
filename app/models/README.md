# app/models

Models Layer README
Project: Startup Idea Validator Agent
Directory: app/models/
Week: 2
Status: ✅ Complete
Focus: LLM client abstraction, model configuration

📋 Overview
The Models layer provides a single interface for LLM API calls (OpenAI/Claude). This abstraction allows you to swap providers without changing agent code, following the MCP Architecture principle.

Key Features
✅ Provider Abstraction - Single interface for OpenAI/Claude
✅ Config Integration - Loads API key from .env via app.config
✅ Chat Completion - Standard LLM calls with chat() method
✅ Streaming - Real-time UI updates with stream_chat()
✅ Model Selection - Support for gpt-4o, gpt-4-turbo, etc.
✅ Tool Calling Stub - chat_with_tools() for Week 5 integration
📁 Directory Structure
text

Copy code
app/models/
├── __init__.py          # Exports LLMClient and singleton
├── llm_client.py        # LLM client abstraction (Week 2)
└── README.md            # This file
🛠️ Components
1. LLMClient Class (llm_client.py)
Method

Description

Week 1

__init__()

Initialize with API key and model name

Week 2

chat()

Send messages and return assistant reply

Week 2

stream_chat()

Stream response for real-time UI

Week 2

chat_with_tools()

Tool/function calling (stub)

Week 5

get_model_info()

Get model configuration info

Week 2

2. Singleton Instance (__init__.py)
llm_client = LLMClient()  # Ready to use across application

 Configuration
Environment Variables (.env)



# LLM Configuration (Week 2)
OPENAI_API_KEY=your_openai_api_key_here
Import Settings

from app.config import settings, OPENAI_API_KEY
from app.models import llm_client, LLMClient

🧪 Testing

# Run all LLM client tests
pytest tests/test_llm_client.py -v

# Run with coverage
pytest tests/test_llm_client.py --cov=app.models
