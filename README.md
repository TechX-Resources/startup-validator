# Startup Idea Validator Agent

A production-grade scaffold for an **AI-powered startup idea validation agent**. Built over 6 weeks by AI + Data Science students, following an MCP-style architecture (Model + Context + Tools + Orchestration).

---

## Project Overview

This agent helps validate startup ideas by:
- Taking a user's idea as input
- Using LLMs for reasoning and orchestration
- Calling external tools (search, competitor analysis, market estimation)
- Storing context and past validations in memory
- Returning structured validation reports

**Tech stack:** Python, FastAPI, LLM API (OpenAI/Claude abstracted), Vector DB (Chroma placeholder). No real API keys in repo.

---

## MCP Architecture (Simple)

| Layer | Purpose |
|-------|--------|
| **Model** | LLM client abstraction — single interface for OpenAI/Claude. |
| **Context** | Memory + embeddings — past ideas, session context, vector store. |
| **Tools** | External capabilities — web search, competitor finder, market estimator. |
| **Orchestration** | Agent loop — reason → choose tool → execute → repeat until done. |

Flow: **User idea** → **Agent** (uses Model + Context) → **Tools** → **Structured response**.

---

## 6-Week Build Roadmap

| Week | Focus | Key Folders |
|------|--------|-------------|
| 1 | Project setup, FastAPI skeleton, config, health + placeholder `/validate-idea` | `app/`, `app/config/` |
| 2 | Models layer + LLM client abstraction, schemas (idea + response) | `app/models/`, `app/schemas/` |
| 3 | Tools: web search, competitor finder, market estimator (stubs → real) | `app/tools/` |
| 4 | Memory: raw/processed data, embeddings, vector store placeholder | `app/memory/`, `data/` |
| 5 | Agent orchestration: validator agent, MCP loop, tool calling | `app/agents/`, `app/services/` |
| 6 | Integration, tests, docs, optional frontend | `tests/`, `docs/`, `frontend/` |

Each folder has a **README.md** with week mapping and implementation notes.

---

## How to Run (Placeholder)

```bash
# 1. Clone repo
git clone <repo-url>
cd startup-idea-validator-agent

# 2. Create virtual environment (recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy env example (add your keys locally; do NOT commit .env)
cp .env.example .env

# 5. Run FastAPI app
uvicorn app.main:app --reload
```

Then open: `http://localhost:8000/docs` for Swagger UI.  
**Health check:** `GET http://localhost:8000/health`

---

## Run and test locally (before pushing to GitHub)

1. **From project root**, create and activate a venv, then install:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. **Start the server:**
   ```powershell
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
3. **Check that everything works:**
   - **Health:** Open http://127.0.0.1:8000/health in a browser, or run:
     ```powershell
     Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get
     ```
     You should see `{"status":"ok","service":"startup-idea-validator-agent"}`.
   - **API docs:** Open http://127.0.0.1:8000/docs and try **GET /health** and **POST /validate-idea** (the latter returns 501 until Week 5–6).
   - **Placeholder endpoint:** `POST /validate-idea` with body `{"idea": "My startup idea"}` should return **501** with message "Not implemented yet...".
4. **Optional:** Add `pytest` to `requirements.txt` and run `pytest tests/` when you add tests.

---

## Contribution Guidelines for Students

- **One folder, one README:** Every directory has a README explaining purpose and which week(s) it belongs to.
- **TODOs over full logic:** Prefer clear TODO comments and stubs; implement incrementally each week.
- **No secrets in repo:** Use `.env` and `.env.example` only; never commit API keys.
- **Tests:** Add unit tests in `tests/` as you implement; keep them simple and focused.
- **Docs:** Update `docs/` with architecture notes and design decisions as you go.

---

## Repository Structure (High-Level)

```
├── app/           # Backend application (FastAPI, agents, tools, models, memory)
├── data/          # raw, processed, embeddings
├── notebooks/     # Experimentation (embeddings, clustering, scoring)
├── tests/         # Unit and integration tests
├── frontend/      # Placeholder UI (optional stretch)
├── docs/          # Architecture and design docs
├── .env.example   # Example environment variables
├── requirements.txt
└── README.md      # This file
```

See each folder’s **README.md** for detailed instructions.
