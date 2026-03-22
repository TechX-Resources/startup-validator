
from typing import Dict, Any, Optional
import re
from app.models import get_llm, ValidationScore
from app.config import OPENAI_API_KEY

MARKET_DATA = {
    # Tech/Software
    "fintech": {"tam": "$500B", "sam": "$100B", "growth": "18% CAGR", "source": "McKinsey 2024"},
    "edtech": {"tam": "$400B", "sam": "$80B", "growth": "12% CAGR", "source": "HolonIQ 2024"},
    "healthtech": {"tam": "$600B", "sam": "$120B", "growth": "15% CAGR", "source": "CB Insights"},
    "saas": {"tam": "$300B", "sam": "$60B", "growth": "20% CAGR", "source": "Gartner 2024"},
    "ecommerce": {"tam": "$8T", "sam": "$1.5T", "growth": "10% CAGR", "source": "Statista"},
    
    # AI/ML
    "ai": {"tam": "$1T", "sam": "$200B", "growth": "37% CAGR", "source": "McKinsey Global"},
    "generative ai": {"tam": "$400B", "sam": "$80B", "growth": "45% CAGR", "source": "Bloomberg"},
    "computer vision": {"tam": "$50B", "sam": "$15B", "growth": "25% CAGR", "source": "MarketsandMarkets"},
    
    # Consumer
    "fitness": {"tam": "$100B", "sam": "$20B", "growth": "8% CAGR", "source": "Statista"},
    "personal finance": {"tam": "$200B", "sam": "$40B", "growth": "12% CAGR", "source": "Forrester"},
}


async def market_estimator(market_or_industry: str) -> Dict[str, Any]:
   
    
    market_or_industry = market_or_industry.lower().strip()
    
    # 1. Exact match in known data
    if market_or_industry in MARKET_DATA:
        data = MARKET_DATA[market_or_industry]
        return {
            **data,
            "market": market_or_industry.title(),
            "confidence": "high",
            "score": ValidationScore(score=9.0, reasoning=f"Known market: {data['source']}"),
            "method": "lookup"
        }
    
    # 2. Fuzzy match (plural/singular)
    for known_market, data in MARKET_DATA.items():
        if known_market in market_or_industry or market_or_industry in known_market:
            return {
                **data, 
                "market": data["market"] if "market" in data else known_market.title(),
                "confidence": "medium",
                "score": ValidationScore(score=8.0, reasoning=f"Fuzzy match: {known_market}"),
                "method": "fuzzy_match"
            }
    
    # 3. LLM estimation for unknown markets
    return await _llm_market_estimate(market_or_industry)


async def _llm_market_estimate(market: str) -> Dict[str, Any]:
    """LLM-powered estimation for unknown markets"""
    if not OPENAI_API_KEY:
        return _mock_fallback(market)
    
    try:
        llm = get_llm()
        prompt = f"""
        Estimate market size for "{market}" startup opportunity.
        
        Return ONLY valid JSON:
        {{
            "tam": "$XXXB" or "$XXXT",
            "sam": "$XXXB", 
            "growth": "XX% CAGR",
            "confidence": "high|medium|low",
            "reasoning": "1-2 sentences"
        }}
        
        Examples:
        - FinTech: {{"tam": "$500B", "sam": "$100B", "growth": "18% CAGR"}}
        - EdTech: {{"tam": "$400B", "sam": "$80B", "growth": "12% CAGR"}}
        """
        
       response = await llm.chat([{"role": "user", "content": prompt}])
        
        # Parse LLM JSON response
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            import json
            data = json.loads(json_match.group())
            return {
                **data,
                "market": market.title(),
                "confidence": data.get("confidence", "low"),
                "score": ValidationScore(
                    score=6.0 if data.get("confidence") == "low" else 7.5,
                    reasoning=data.get("reasoning", "LLM estimate")
                ),
                "method": "llm_estimate"
            }
    
    except Exception as e:
        print(f"LLM estimation failed: {e}")
    
    # 4. Fallback
    return _mock_fallback(market)



def _mock_fallback(market: str) -> Dict[str, Any]:
    """Graceful degradation for missing LLM"""
    return {
        "market": market.title(),
        "tam": "TBD ($10B-$100B)",
        "sam": "TBD ($1B-$10B)", 
        "growth": "TBD (10-20% CAGR)",
        "source": "Estimator fallback",
        "confidence": "low",
        "score": ValidationScore(score=4.0, reasoning="No data available"),
        "method": "fallback"
    }


if __name__ == "__main__":
    import asyncio
    async def demo():
        print("=== Market Estimator Demo ===\n")
        
        # Known markets
        print("1. Known:", await market_estimator("fintech"))
        print("2. Fuzzy:", await market_estimator("AI tools"))
        
        # Unknown (LLM)
        print("3. Unknown:", await market_estimator("quantum computing"))
    
    asyncio.run(demo())
