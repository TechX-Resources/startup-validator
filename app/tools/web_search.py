"""
Web search tool — external capability for the agent to look up information.
Uses SerpAPI for real search results, falls back to mock data when no API key is set.
"""

import os
import httpx


SERPAPI_ENDPOINT = "https://serpapi.com/search"

# Mock results used when SERPAPI_API_KEY is not set (for testing / offline dev)
MOCK_RESULTS = [
    {
        "title": "Market Analysis: Startup Trends 2025",
        "snippet": "The startup ecosystem continues to grow with AI-driven solutions leading investment rounds.",
        "link": "https://example.com/market-analysis",
    },
    {
        "title": "How to Validate a Startup Idea",
        "snippet": "Key validation steps include market sizing, competitor analysis, and customer interviews.",
        "link": "https://example.com/validate-idea",
    },
    {
        "title": "Emerging Industries Report",
        "snippet": "Healthcare AI, climate tech, and developer tools are seeing the fastest growth.",
        "link": "https://example.com/emerging-industries",
    },
]


def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web for the given query and return a list of results.

    Each result is a dict with keys: title, snippet, link.
    Falls back to mock data when SERPAPI_API_KEY is not set.
    """
    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        return MOCK_RESULTS[:max_results]

    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": max_results,
    }

    try:
        response = httpx.get(SERPAPI_ENDPOINT, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return MOCK_RESULTS[:max_results]

    results = []
    for item in data.get("organic_results", [])[:max_results]:
        results.append({
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "link": item.get("link", ""),
        })

    return results
