"""
Web search tool — external capability for the agent to look up information.

Uses SerpAPI to fetch Google search results and returns a simple, structured list
of results the agent (and downstream tools) can consume.
"""

from __future__ import annotations

import os
from typing import Any, List, Dict

import requests

from app.utils.logger import get_logger

logger = get_logger(__name__)

SERP_URL = "https://serpapi.com/search.json"


def web_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Run a web search and return structured search results.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return (capped to a small number).

    Returns:
        List of dicts: [{"title": str, "snippet": str, "url": str}, ...]
    """
    query = (query or "").strip()
    if not query:
        return []

    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable not set")

    max_results = max(1, min(int(max_results), 10))

    params = {
        "engine": "google",
        "q": query,
        "num": max_results,
        "api_key": api_key,
    }

    logger.info("Calling SerpAPI web search", extra={"query": query, "max_results": max_results})
    response = requests.get(SERP_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    organic = data.get("organic_results") or []

    results: List[Dict[str, Any]] = []
    for item in organic[:max_results]:
        results.append(
            {
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "url": item.get("link"),
            }
        )

    logger.info("SerpAPI web search returned %d results", len(results))
    return results


if __name__ == "__main__":
    q = "Online Meeting AI Transcriber and Summarizer"
    for idx, result in enumerate(web_search(q), start=1):
        print(f"{idx}. {result['title']}\n   {result['snippet']}\n   URL: {result['url']}\n")