"""
Web search tool — external capability for the agent to look up information.
Week 3: Implement (mock or real API e.g. SerpAPI).
"""


from typing import List, Optional
import random
from datetime import datetime
from app.config import settings

def web_search(query: str, max_results: int = 5) -> str:
    """
    Run a web search for the given query and return results as a string.
    Returns structured search results that the agent can use for validation context.
    
    Week 3 Implementation: Mock data with keyword matching
    Future Enhancement: Integrate with SerpAPI, Google Custom Search, or Serper API
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Formatted string of search results for agent consumption
    """
    
    # Mock search results database
    MOCK_SEARCH_RESULTS = [
        {
            "title": "AI Startup Market Analysis 2024",
            "snippet": "The AI startup market is growing at 35% CAGR with over 10,000 new AI companies founded in 2023.",
            "url": "https://techcrunch.com/ai-startup-market-2024"
        },
        {
            "title": "Document Summarization Tools Comparison",
            "snippet": "Top document summarization tools include Notion AI, ChatPDF, and Quillbot with varying pricing models.",
            "url": "https://producthunt.com/document-summarization-tools"
        },
        {
            "title": "EdTech Market Size and Growth",
            "snippet": "EdTech market valued at $320B in 2024, expected to reach $404B by 2025 with 12% CAGR.",
            "url": "https://statista.com/edtech-market-size"
        },
        {
            "title": "Legal Tech Automation Trends",
            "snippet": "Legal tech automation market growing 25% annually with document review and contract analysis leading.",
            "url": "https://legaltech.com/automation-trends"
        },
        {
            "title": "SaaS Startup Success Metrics",
            "snippet": "Successful SaaS startups achieve $1M ARR in 18 months on average with strong product-market fit.",
            "url": "https://a16z.com/saas-success-metrics"
        },
        {
            "title": "Competitor Analysis Framework",
            "snippet": "Framework for analyzing startup competitors: direct, indirect, and substitute products.",
            "url": "https://ycombinator.com/competitor-analysis"
        },
        {
            "title": "Market Validation Best Practices",
            "snippet": "Key steps for validating startup ideas: customer interviews, landing page tests, and pre-orders.",
            "url": "https://steveblank.com/market-validation"
        },
        {
            "title": "AI Writing Tools Market Report",
            "snippet": "AI writing tools market expected to reach $15B by 2027 with Grammarly and Jasper leading.",
            "url": "https://gartner.com/ai-writing-tools"
        }
    ]
    
    # Keyword matching to find relevant results
    keywords = query.lower().split()
    relevant_results = []
    
    for result in MOCK_SEARCH_RESULTS:
        # Check if result contains any idea keywords
        content = f"{result['title']} {result['snippet']}".lower()
        matches = sum(1 for keyword in keywords if keyword in content)
        
        if matches >= 1:
            relevant_results.append(result)
    
    # If no matches found, return random subset
    if not relevant_results:
        relevant_results = random.sample(MOCK_SEARCH_RESULTS, min(max_results, len(MOCK_SEARCH_RESULTS)))
    
    # Limit to max_results
    relevant_results = relevant_results[:max_results]
    
    # Format results as string for agent consumption
    formatted_results = []
    for i, result in enumerate(relevant_results, 1):
        formatted_results.append(
            f"[{i}] {result['title']}\n"
            f"    {result['snippet']}\n"
            f"    URL: {result['url']}\n"
        )
    
    return "\n\n".join(formatted_results)


def web_search_structured(query: str, max_results: int = 5) -> List[dict]:
    """
    Alternative version that returns structured data (list of dicts).
    Useful for programmatic access to search results.
    
    Returns:
        List of dicts with 'title', 'snippet', 'url' keys
    """
    # Reuse mock data logic
    keywords = query.lower().split()
    relevant_results = []
    
    for result in MOCK_SEARCH_RESULTS:
        content = f"{result['title']} {result['snippet']}".lower()
        matches = sum(1 for keyword in keywords if keyword in content)
        
        if matches >= 1:
            relevant_results.append(result)
    
    if not relevant_results:
        relevant_results = random.sample(MOCK_SEARCH_RESULTS, min(max_results, len(MOCK_SEARCH_RESULTS)))
    
    return relevant_results[:max_results]


def web_search_real_api(query: str, max_results: int = 5, api_provider: str = "serper") -> str:
    """
    TODO: Week 3+ - Implement real API integration (SerpAPI, Google Custom Search, Serper)
    This is a placeholder for future enhancement.
    
    Args:
        query: Search query string
        max_results: Maximum number of results
        api_provider: 'serper', 'serpapi', or 'google_custom'
    
    Returns:
        Formatted string of search results
    """
    # Example integration with Serper API (requires API key)
    # import requests
    # import os
    #
    # API_KEY = os.getenv("SERPER_API_KEY")
    # if not API_KEY:
    #     return web_search(query, max_results)  # Fallback to mock
    #
    # response = requests.get(
    #     f"https://google.serper.dev/search?q={query}",
    #     headers={"X-API-KEY": API_KEY}
    # )
    # results = response.json().get("organic", [])
    #
    # formatted_results = []
    # for i, result in enumerate(results[:max_results], 1):
    #     formatted_results.append(
    #         f"[{i}] {result.get('title', '')}\n"
    #         f"    {result.get('snippet', '')}\n"
    #         f"    URL: {result.get('link', '')}\n"
    #     )
    #
    # return "\n\n".join(formatted_results)
    
    raise NotImplementedError("Real API integration not yet implemented.")
