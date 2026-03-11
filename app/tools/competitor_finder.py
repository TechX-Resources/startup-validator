"""
Competitor finder tool — find potential competitors for a startup idea/domain.
Week 3: Implement (mock list or real source).
""

from typing import List, Optional
import random
from app.config import settings

def competitor_finder(idea_summary: str, domain: str = None) -> list[dict]:
    """
    Given a short idea summary (and optional domain), return a list of potential competitors.
    Expected: [{"name": "...", "description": "...", "url": "..."}, ...]
    
    Week 3 Implementation: Mock data with keyword matching
    Future Enhancement: Integrate with Crunchbase API, Serper API, or similar
    """
    
    # Mock competitor database for demonstration
    MOCK_COMPETITORS = [
        {
            "name": "Notion AI",
            "description": "AI-powered workspace and document tool",
            "url": "https://www.notion.so"
        },
        {
            "name": "ChatPDF",
            "description": "AI chat interface for PDF documents",
            "url": "https://www.chatpdf.com"
        },
        {
            "name": "Jasper AI",
            "description": "AI content generation platform",
            "url": "https://www.jasper.ai"
        },
        {
            "name": "Grammarly",
            "description": "AI writing assistant and grammar checker",
            "url": "https://www.grammarly.com"
        },
        {
            "name": "Copy.ai",
            "description": "AI copywriting and content creation tool",
            "url": "https://www.copy.ai"
        },
        {
            "name": "Quillbot",
            "description": "AI paraphrasing and writing tool",
            "url": "https://www.quillbot.com"
        },
        {
            "name": "Frase",
            "description": "AI content research and writing platform",
            "url": "https://www.frase.io"
        },
        {
            "name": "Surfer SEO",
            "description": "AI-powered SEO content optimization",
            "url": "https://www.surferseo.com"
        }
    ]
    
    # Keyword matching to find relevant competitors
    keywords = idea_summary.lower().split()
    relevant_competitors = []
    
    for competitor in MOCK_COMPETITORS:
        # Check if competitor description contains any idea keywords
        description_lower = competitor["description"].lower()
        matches = sum(1 for keyword in keywords if keyword in description_lower)
        
        if matches >= 1:
            relevant_competitors.append(competitor)
    
    # If no matches found, return random subset
    if not relevant_competitors:
        relevant_competitors = random.sample(MOCK_COMPETITORS, min(3, len(MOCK_COMPETITORS)))
    
    # Limit to top 5 results
    return relevant_competitors[:5]


def competitor_finder_real_api(idea_summary: str, domain: str = None) -> list[dict]:
    """
    TODO: Week 3+ - Implement real API integration (Serper, Crunchbase, etc.)
    This is a placeholder for future enhancement.
    """
    # Example integration with Serper API (requires API key)
    # import requests
    # 
    # API_KEY = os.getenv("SERPER_API_KEY")
    # if not API_KEY:
    #     return competitor_finder(idea_summary, domain)  # Fallback to mock
    #
    # response = requests.get(
    #     f"https://google.serper.dev/search?q={idea_summary}",
    #     headers={"X-API-KEY": API_KEY}
    # )
    # results = response.json().get("organic", [])
    #
    # return [
    #     {"name": r.get("title", ""), "description": r.get("snippet", ""), "url": r.get("link", "")}
    #     for r in results[:5]
    # ]
    
    raise NotImplementedError("Real API integration not yet implemented.")
