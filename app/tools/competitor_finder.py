"""
Competitor finder tool — find potential competitors for a startup idea/domain.

For now this is a pure SerpAPI-based implementation with **no LLM dependency** so it
can run end-to-end with only finished components.
"""

from __future__ import annotations

from typing import List, Dict, Optional

from app.tools.web_search import web_search


def competitor_finder(idea_summary: str, domain: Optional[str] = None) -> List[Dict]:
    """
    Given a short idea summary (and optional domain), return a list of potential competitors.

    Implementation note:
    - Uses `web_search` to fetch relevant results.
    - Maps the top results directly into competitor objects.
    """
    query = (
        f"{idea_summary} in {domain} competitors list"
        if domain
        else f"{idea_summary} competitors list"
    )

    search_results = web_search(query, max_results=10)

    competitors: List[Dict] = []
    for result in search_results:
        competitors.append(
            {
                "name": result.get("title") or "",
                "description": result.get("snippet") or "",
                "url": result.get("url") or "",
            }
        )

    return competitors


if __name__ == "__main__":
    idea = "Online Meeting AI Transcriber and Summarizer"
    for c in competitor_finder(idea):
        print(f"- {c['name']} ({c['url']}): {c['description']}")