# Architecture — MCP-Style Agent

This document describes the **Model + Context + Tools + Orchestration** architecture used by the Startup Idea Validator Agent.

---

## High-Level Flow

```
User (Frontend / API client)
        │
        ▼
┌───────────────────┐
│  FastAPI Gateway   │  POST /validate-idea  { "idea": "..." }
│  (app/main.py)     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ ValidationService  │  Glue layer — connects API to agent + memory
│ (app/services/)    │
└────────┬──────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Memory │ │ValidatorAgent│  MCP orchestration loop
│ (app/  │ │ (app/agents/) │
│ memory)│ └──┬───────────┘
└────────┘    │
         ┌────┼────────────┐
         ▼    ▼            ▼
     ┌──────┐┌───────────┐┌──────────────┐
     │WebSrch││CompFinder ││MarketEstimtr │  External tools
     │(tools)││(tools)    ││(tools)       │
     └──────┘└───────────┘└──────────────┘
         │    │            │
         └────┼────────────┘
              ▼
       ┌────────────┐
       │  LLMClient  │  Model layer — OpenAI / Claude abstraction
       │ (app/models) │
       └──────┬─────┘
              ▼
      ValidationResponse  →  returned to user as JSON
```

---

## The Four MCP Layers

### 1. Model (`app/models/`)

Abstracted LLM client. A single `LLMClient` class wraps OpenAI and Claude behind the same `.chat()` / `.chat_with_tools()` interface so the rest of the codebase never imports a provider SDK directly.

**Key file:** `llm_client.py`
**Week:** 2

### 2. Context (`app/memory/` + `data/`)

Persistence layer for past validations and embeddings. Enables similarity search so the agent can reference "I've seen an idea like this before."

| Sub-folder | Purpose |
|------------|---------|
| `data/raw/` | Raw input ideas (text files, CSVs) |
| `data/processed/` | Cleaned / structured data |
| `data/embeddings/` | Vector embeddings for similarity search |
| `app/memory/memory_store.py` | `save()` and `get_context()` functions |

**Week:** 4

### 3. Tools (`app/tools/`)

External capabilities the agent can invoke mid-reasoning:

| Tool | File | Purpose |
|------|------|---------|
| Web Search | `web_search.py` | Fetch live web snippets for market signals |
| Competitor Finder | `competitor_finder.py` | Discover existing products in the space |
| Market Estimator | `market_estimator.py` | Estimate TAM, growth rate, industry context |

Each tool is a standalone function: `(query: str) -> str`. The agent calls them via the orchestration loop.

**Week:** 3

### 4. Orchestration (`app/agents/` + `app/services/`)

The agent loop: **reason → choose tool → execute → repeat → final answer**.

```
while not done:
    response = llm.chat(messages)
    if response.wants_tool_call:
        result = call_tool(response.tool_name, response.tool_args)
        messages.append(tool_result_message(result))
    else:
        return parse_final_answer(response)
```

**Key files:** `validator_agent.py` (loop), `validation_service.py` (glue)
**Week:** 5

---

## API Contract

### `GET /health`

Returns `200` with `{"status": "ok", "service": "startup-idea-validator-agent"}`.

### `POST /validate-idea`

**Request body** (`IdeaInput`):
```json
{ "idea": "An AI app that summarizes PDFs for students." }
```

**Response body** (`ValidationResponse`):
```json
{
  "score": 7.5,
  "summary": "Strong idea with clear use case; market is crowded.",
  "strengths": ["Clear pain point", "Scalable"],
  "risks": ["Many existing tools", "Monetization unclear"],
  "competitors": ["Notion AI", "ChatPDF"],
  "market_notes": "EdTech document tools growing ~12% CAGR."
}
```

**Status codes:** `200` success, `422` validation error, `501` not yet implemented (pre-Week 5).

---

## Prompt Architecture (`app/prompts/`)

All LLM prompts are centralized in `app/prompts/templates.py` rather than scattered as inline strings. This gives:

- **Version control** — prompt changes show up in git diffs
- **Single source of truth** — agent, service, and tests all reference the same prompts
- **Easy tuning** — adjust tone, output format, or evaluation criteria in one place

Key exports: `SYSTEM_PROMPT`, `build_user_prompt()`, `build_validation_messages()`, `build_tool_result_message()`.

---

## Middleware Stack

Requests pass through middleware in this order:

1. **RequestLoggingMiddleware** — logs `→ method path body ts` and `← method path status latency`
2. **CORSMiddleware** — allows cross-origin requests from the frontend

Both are registered in `app/main.py`.

---

## Data Flow Summary

```
1. User submits idea via POST /validate-idea
2. ValidationService (optional) loads context from memory
3. ValidatorAgent builds prompt using app/prompts/templates.py
4. Agent loop: LLM reasons, calls tools, collects evidence
5. LLM produces final JSON matching ValidationResponse schema
6. ValidationService (optional) saves result + embedding to memory
7. FastAPI returns ValidationResponse to user
```
