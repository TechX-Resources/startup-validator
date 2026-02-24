# app/services

**Purpose:** Business logic layer — connects the API (main.py) to the agent and optional side effects (e.g. saving to memory, logging).

**What students will implement:**
- **validation_service.py:** Entry point that:
  - Accepts idea (and optional user/session id).
  - Optionally loads context from memory (app/memory).
  - Calls the validator agent (app/agents).
  - Optionally stores the result in memory.
  - Returns structured response (using app/schemas).
- Keep HTTP-specific details in main.py; keep orchestration in agents; services = glue + business rules.

**Weeks:** 5–6 (once agent and memory are in place).
