# app/tools

**Purpose:** Tools = external capabilities the agent can call (search, scraping, market data, etc.). Each tool is a focused function the orchestrator invokes.

**What students will implement:**
- **web_search.py:** Given a query, return search results (e.g. via SerpAPI placeholder or mock).
- **competitor_finder.py:** Given a startup idea/domain, return a list of potential competitors (mock or real API).
- **market_estimator.py:** Given a market/industry, return a rough market size or growth estimate (placeholder/mock).

Keep interfaces simple: input (str or dict) → output (str or structured dict) so the agent can parse and reason.

**Weeks:** 3 (implement stubs first, then real or mock implementations).
