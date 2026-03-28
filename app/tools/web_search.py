import logging
import httpx
from app.config import settings
from app.utils.helpers import save_data

logger = logging.getLogger(__name__)

SERPER_ENDPOINT = "https://google.serper.dev/search"

def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web for the given query and return a list of results using Serper.dev.
    """
    api_key = settings.serper_api_key

    if not api_key:
        logger.error("SERPER_API_KEY not found in settings.")
        return []

    headers = {
        'X-API-KEY': api_key,
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
        
        # Save raw Serper data for history and debugging
        try:
            save_data(data, category='raw', base_filename='web_search')
        except Exception as e:
            logger.warning(f"Failed to save raw search data: {e}")

    except httpx.HTTPStatusError as e:
        logger.error(f"Serper error (status {e.response.status_code}): {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error during search for '{query}': {e}")
        return []

    results = []
    # Serper returns results in "organic" list
    organic = data.get("organic", [])
    if not organic:
        logger.warning(f"No organic results found for query: {query}")
        return []

    for item in organic[:max_results]:
        results.append({
            "title": item.get("title", "No Title"),
            "snippet": item.get("snippet", "No Snippet"),
            "link": item.get("link", "#"),
        })

    return results
