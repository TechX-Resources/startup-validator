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
