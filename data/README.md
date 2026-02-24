# data

**Purpose:** All data used or produced by the project — raw inputs, processed datasets, and embeddings for the vector store.

**Subfolders:**
- **raw/** — Scraped or ingested data (e.g. search results, competitor lists). Do not commit large or sensitive files; use .gitignore.
- **processed/** — Cleaned, normalized data ready for the agent or analysis.
- **embeddings/** — Vector representations (e.g. from Chroma or saved numpy arrays). Used by memory/vector store.

**What students will implement:** Populate these in Week 3–4 when building tools and memory; add .gitkeep so empty dirs are tracked; optionally add sample/mock files for testing.

**Weeks:** 3 (raw/processed from tools), 4 (embeddings for memory).
