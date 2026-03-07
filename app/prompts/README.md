# app/prompts/

**Purpose:** Centralized, version-controlled prompt templates for the validator agent.

**Week mapping:** Supports Week 2 (schemas), Week 5 (agent orchestration).

## Why a separate module?

Keeping prompts out of inline strings inside agent/service code gives you:

1. **Diffable history** — prompt changes show up in git as clear text diffs.
2. **Single source of truth** — the system prompt and output contract live in one place; every caller uses the same version.
3. **Easy tuning** — adjust wording, scoring rubric, or output schema without touching orchestration logic.
4. **Testability** — you can unit-test `build_user_prompt()` and `build_validation_messages()` with known inputs.

## Key exports

| Name | Type | Purpose |
|------|------|---------|
| `SYSTEM_PROMPT` | `str` | Full system-level prompt: persona, tools, evaluation criteria, JSON output contract. |
| `RESPONSE_FORMAT_INSTRUCTIONS` | `str` | Short one-liner you can append to any message to remind the LLM of the output schema. |
| `build_user_prompt(idea, ...)` | `func` | Assembles the user turn from the raw idea and optional tool/memory results. |
| `build_validation_messages(idea, ...)` | `func` | Returns a complete `[system, user]` message list ready for `LLMClient.chat()`. |
| `build_tool_result_message(tool_name, result)` | `func` | Formats a single tool output as a conversation message for the multi-turn agent loop. |

## Usage

```python
from app.prompts import build_validation_messages

messages = build_validation_messages(
    "An AI app that summarizes long PDFs for students in 3 bullet points.",
    web_results="...",           # optional
    competitor_results="...",    # optional
    market_results="...",        # optional
    memory_context="...",        # optional
)

response = llm_client.chat(messages=messages)
```
