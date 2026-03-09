"""
Web search tool — external capability for the agent to look up information.
Week 3: Implement (mock or real API e.g. SerpAPI).
"""
import os
import json
import requests

SERP_URL = "https://serpapi.com/search.json"


def _run_search(query: str, max_results: int = 5):
    """Internal helper to call SerpAPI and return structured results."""

    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY not set")

    params = {
        "engine": "google",
        "q": query,
        "num": max_results,
        "api_key": api_key
    }

    response = requests.get(SERP_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    results = []
    for r in data.get("organic_results", [])[:max_results]:
        results.append({
            "title": r.get("title"),
            "snippet": r.get("snippet"),
            "url": r.get("link")
        })

    return results


def web_search_market_analysis(startup_idea: str, max_results: int = 5) -> dict:
    """
    Search the web to analyze startup market density and competitiveness.
    Saves results to JSON for MCP usage.
    """

    queries = {
        "competitors": f"{startup_idea} competitors startups",
        #"market_size": f"{startup_idea} market size growth",
        #"funding_activity": f"{startup_idea} startup funding venture capital",
        #"user_pain_points": f"problems with {startup_idea}"
    }

    analysis = {}

    for category, query in queries.items():
        try:
            analysis[category] = _run_search(query, max_results)
        except Exception as e:
            analysis[category] = {"error": str(e)}

    result_data = {
        "startup_idea": startup_idea,
        "analysis": analysis
    }

    #filename = f"{startup_idea.replace(' ', '_')}_market_analysis.json"
    #with open(filename, "w", encoding="utf-8") as f:
    #    json.dump(result_data, f, indent=4)
    return result_data
    
#testing:
if __name__ == "__main__":
    test_query = "Online meeting transcribing tool"
    analysis = web_search_market_analysis(test_query)
    print(analysis)