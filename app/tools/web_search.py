import logging
import os
import httpx

logger = logging.getLogger(__name__)

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
        logger.info("SERPAPI_API_KEY not found, using mock results.")
        return MOCK_RESULTS[:max_results]

    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": max_results,
    }

    try:
        response = httpx.get(SERPAPI_ENDPOINT, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"SerpAPI error (status {e.response.status_code}): {e}")
        return MOCK_RESULTS[:max_results]
    except Exception as e:
        logger.error(f"Unexpected error during search for '{query}': {e}")
        return MOCK_RESULTS[:max_results]

    results = []
    organic = data.get("organic_results", [])
    if not organic:
        logger.warning(f"No organic results found for query: {query}")
        return MOCK_RESULTS[:max_results]

    for item in organic[:max_results]:
        results.append({
            "title": item.get("title", "No Title"),
            "snippet": item.get("snippet", "No Snippet"),
            "link": item.get("link", "#"),
        })

    return results
