import logging
import os
import httpx
from dotenv import load_dotenv

# Load env variables
load_dotenv()

logger = logging.getLogger(__name__)

SERPER_ENDPOINT = "https://google.serper.dev/search"
SERPAPI_ENDPOINT = "https://serpapi.com/search"

# Mock results used when no API key is set (for testing / offline dev)
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
    Search the web for the given query and return a list of results using SerpAPI or Serper.dev.
    Falls back to mock data if no API keys are set or if the request fails.
    """
    serpapi_key = os.environ.get("SERPAPI_API_KEY")
    serper_key = os.environ.get("SERPER_API_KEY")

    # Prioritize SerpAPI for backward compatibility and test suite environment patching
    if serpapi_key:
        logger.info("Using SerpAPI for search.")
        params = {
            "q": query,
            "api_key": serpapi_key,
            "engine": "google",
            "num": max_results,
        }
        try:
            response = httpx.get(SERPAPI_ENDPOINT, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
            results = []
            organic = data.get("organic_results", [])
            for item in organic[:max_results]:
                results.append({
                    "title": item.get("title", "No Title"),
                    "snippet": item.get("snippet", "No Snippet"),
                    "link": item.get("link", "#"),
                })
            return results
        except Exception as e:
            logger.error(f"Unexpected error during SerpAPI search for '{query}': {e}")
            # Fall through to mock

    elif serper_key:
        logger.info("Using Serper.dev for search.")
        headers = {
            'X-API-KEY': serper_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'q': query,
            'num': max_results
        }
        try:
            response = httpx.post(SERPER_ENDPOINT, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            results = []
            organic = data.get("organic", [])
            for item in organic[:max_results]:
                results.append({
                    "title": item.get("title", "No Title"),
                    "snippet": item.get("snippet", "No Snippet"),
                    "link": item.get("link", "#"),
                })
            return results
        except Exception as e:
            logger.error(f"Unexpected error during Serper search for '{query}': {e}")
            # Fall through to mock

    logger.info("No search API key provided or search failed; returning mock results.")
    return MOCK_RESULTS[:max_results]
