"""
Market estimator tool — rough market size or growth for a given market/industry.
Week 3: Implement (placeholder/mock or real data source).
"""


from typing import Dict, Optional
import random
from datetime import datetime
from app.config import settings

# Mock market data database
MOCK_MARKET_DATA = [
    {
        "market": "AI Document Summarization",
        "tam": 2500000000,
        "sam": 750000000,
        "som": 75000000,
        "growth_rate": 0.35,
        "source": "TechCrunch Market Analysis 2024"
    },
    {
        "market": "EdTech Learning Tools",
        "tam": 320000000000,
        "sam": 96000000000,
        "som": 9600000000,
        "growth_rate": 0.12,
        "source": "Statista EdTech Report 2024"
    },
    {
        "market": "Legal Tech Automation",
        "tam": 45000000000,
        "sam": 13500000000,
        "som": 1350000000,
        "growth_rate": 0.25,
        "source": "Legal Tech Industry Report 2024"
    },
    {
        "market": "SaaS Content Writing Tools",
        "tam": 15000000000,
        "sam": 4500000000,
        "som": 450000000,
        "growth_rate": 0.18,
        "source": "Gartner AI Writing Tools 2024"
    },
    {
        "market": "AI Customer Support",
        "tam": 28000000000,
        "sam": 8400000000,
        "som": 840000000,
        "growth_rate": 0.22,
        "source": "Forbes AI Support Market 2024"
    },
    {
        "market": "Healthcare AI Diagnostics",
        "tam": 180000000000,
        "sam": 54000000000,
        "som": 5400000000,
        "growth_rate": 0.28,
        "source": "McKinsey Healthcare AI 2024"
    },
    {
        "market": "E-commerce Personalization",
        "tam": 65000000000,
        "sam": 19500000000,
        "som": 1950000000,
        "growth_rate": 0.15,
        "source": "eMarketer Personalization 2024"
    },
    {
        "market": "Financial Planning AI",
        "tam": 35000000000,
        "sam": 10500000000,
        "som": 1050000000,
        "growth_rate": 0.20,
        "source": "Bloomberg Fintech AI 2024"
    }
]


def market_estimator(market_or_industry: str) -> dict:
    """
    Given a market or industry name, return a rough estimate (TAM, SAM, SOM, growth rate).
    
    Week 3 Implementation: Mock data with keyword matching
    Future Enhancement: Integrate with Statista, Gartner, or IBISWorld API
    
    Args:
        market_or_industry: Market or industry name to estimate
    
    Returns:
        Dictionary with market data:
        {
            "market": str,
            "tam": float (Total Addressable Market in USD),
            "sam": float (Serviceable Addressable Market in USD),
            "som": float (Serviceable Obtainable Market in USD),
            "growth_rate": float (Annual growth rate as decimal),
            "source": str (Data source reference)
        }
    """
    
    # Normalize input for matching
    query = market_or_industry.lower()
    keywords = query.split()
    
    # Find matching market data
    matching_results = []
    
    for market_data in MOCK_MARKET_DATA:
        market_lower = market_data["market"].lower()
        # Check if any keyword matches
        matches = sum(1 for keyword in keywords if keyword in market_lower)
        
        if matches >= 1:
            matching_results.append(market_data)
    
    # If no matches found, return random market data
    if not matching_results:
        matching_results = [random.choice(MOCK_MARKET_DATA)]
    
    # Return best match (first one)
    result = matching_results[0].copy()
    result["market"] = market_or_industry  # Use original input for market name
    
    return result


def market_estimator_detailed(market_or_industry: str) -> dict:
    """
    Extended version with additional market insights.
    
    Returns:
        Dictionary with detailed market analysis:
        {
            "market": str,
            "tam": float,
            "sam": float,
            "som": float,
            "growth_rate": float,
            "cagr_5yr": float,
            "key_players": list[str],
            "market_trends": list[str],
            "source": str,
            "last_updated": str
        }
    """
    
    base_data = market_estimator(market_or_industry)
    
    # Add additional insights
    detailed_data = {
        **base_data,
        "cagr_5yr": base_data["growth_rate"] * 1.1,  # 5-year CAGR estimate
        "key_players": [
            "Market Leader A",
            "Market Leader B",
            "Emerging Competitor C"
        ],
        "market_trends": [
            "AI integration increasing",
            "Mobile-first adoption",
            "Enterprise demand growing"
        ],
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    
    return detailed_data


def market_estimator_real_api(market_or_industry: str) -> dict:
    """
    TODO: Week 3+ - Implement real API integration (Statista, Gartner, IBISWorld)
    This is a placeholder for future enhancement.
    
    Returns:
        Dictionary with real market data from external API
    """
    # Example integration with Statista API (requires API key)
    # import requests
    # import os
    #
    # API_KEY = os.getenv("STATISTA_API_KEY")
    # if not API_KEY:
    #     return market_estimator(market_or_industry)  # Fallback to mock
    #
    # response = requests.get(
    #     f"https://api.statista.com/v3/market/{market_or_industry}",
    #     headers={"Authorization": f"Bearer {API_KEY}"}
    # )
    #
    # if response.status_code == 200:
    #     data = response.json()
    #     return {
    #         "market": data.get("market_name", market_or_industry),
    #         "tam": data.get("tam", 0),
    #         "sam": data.get("sam", 0),
    #         "som": data.get("som", 0),
    #         "growth_rate": data.get("growth_rate", 0),
    #         "source": "Statista API",
    #         "last_updated": data.get("last_updated", "")
    #     }
    #
    # return market_estimator(market_or_industry)  # Fallback to mock
    
    raise NotImplementedError("Real API integration not yet implemented.")
