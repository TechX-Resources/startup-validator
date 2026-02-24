# app/memory

**Purpose:** Storing past ideas, embeddings, and context so the agent can use history (e.g. “similar ideas we’ve seen”) or persist results for later analysis.

**What students will implement:**
- **memory_store.py:** Interface to:
  - Save a validated idea + result (and optional embedding).
  - Retrieve context for a new idea (e.g. similar past ideas, or last N results).
  - Use a vector DB (Chroma or similar) as placeholder: store embeddings in `data/embeddings`, query by similarity.
- Week 4: Implement storage and retrieval; Week 5: plug into agent/services.

**Weeks:** 4 (storage + embeddings), 5 (integration).
