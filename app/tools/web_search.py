"""
Web search tool — external capability for the agent to look up information.
Week 3: Implement (mock or real API e.g. SerpAPI).
"""


# def web_search(query: str, max_results: int = 5) -> str:
#     """
#     Run a web search for the given query and return results as a string (or structured dict).
#     Expected: list of snippets/titles/URLs the agent can use for validation context.
#     TODO: Call search API or return mock list of results.
#     """
#     # TODO: Implement in Week 3
#     raise NotImplementedError("Implement web search (mock or API).")
import requests
from typing import List

def search_web(query: str, max_results: int = 5) -> List[str]:
    """
    Perform a web search for the given query.
    Returns a list of search result snippets.
    """
    # TODO: Week 3 - Integrate with Serper API or Google Custom Search
    # Placeholder implementation
    return [
        f"Search result 1 for '{query}'",
        f"Search result 2 for '{query}'",
        f"Search result 3 for '{query}'"
    ]
