# app/schemas

**Purpose:** Structured inputs and outputs — VERY IMPORTANT for a clean API and for the LLM to produce parseable results. Use Pydantic models for request/response and for the agent’s final validation object.

**What students will implement:**
- **idea_schema.py:** Request shape for “validate this idea” (e.g. idea text, optional fields).
- **response_schema.py:** Response shape: score, summary, strengths, risks, competitors, market_notes, etc. Keep it stable so the frontend and agent can rely on it.
- Include example JSON in comments so students and the LLM know the expected format.

**Weeks:** 2 (define schemas), then use everywhere in 3–6.
