# Design Decisions

A running log of architectural and implementation choices, with rationale. This file currently documents **only Week 1** decisions that are already implemented.

---

## 1. FastAPI over Flask/Django

**Decision:** Use FastAPI as the web framework.

**Why:**
- Async-native — handles concurrent LLM API calls without blocking
- Automatic OpenAPI docs at `/docs` — no extra setup for Swagger
- Pydantic integration — request/response validation is built in
- Lightweight — minimal boilerplate for a small API surface (2 endpoints)

**Week:** 1

---

## 2. MCP Architecture (Model + Context + Tools + Orchestration)

**Decision:** Structure the backend as four distinct layers rather than a monolithic script.

**Why:**
- **Swap-ability** — change the LLM provider (Model layer) without touching the agent logic
- **Testability** — each layer can be unit-tested independently with mocks
- **Teachability** — students see a clear separation of concerns from day one
- **Production-readiness** — mirrors how real AI agent systems are structured

**Week:** 1

---

## 3. Starlette-Based Request Logging Middleware

**Decision:** Use `BaseHTTPMiddleware` for request/response logging rather than FastAPI dependencies or a third-party library.

**Why:**
- Wraps **every** request — no need to add logging to individual route handlers
- Uses the shared `app.utils.logger` for consistent log format
- Truncates request bodies to 1 KB to avoid log flooding with large payloads
- Re-injects the request body stream so downstream handlers can still read it

**Trade-off:** `BaseHTTPMiddleware` reads the full body into memory, which is fine for small payloads but not ideal for file uploads. Acceptable for this API's use case.

**Week:** 1

---

## 4. `.env` + `.env.example` for Secrets

**Decision:** Never commit API keys. Use `.env` (gitignored) with a committed `.env.example` template.

**Why:**
- Students clone the repo and create their own `.env` from the example
- No risk of accidentally pushing real keys to GitHub
- Works with any deployment platform (Render, Railway, etc.) that supports env vars

**Week:** 1

---

## 5. Stub-First Development (TODOs over Full Logic)

**Decision:** Every module starts as a documented stub with `raise NotImplementedError` and `# TODO` comments referencing which week to implement.

**Why:**
- Students can clone and run the full project skeleton on day one
- Each week's work is clearly scoped — search for `TODO (Week N)`
- The codebase compiles and the API starts even before any feature is implemented
- Reduces merge conflicts — students work on different stubs in parallel

**Week:** 1
