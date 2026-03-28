import json
import logging
import re
from app.tools.web_search import web_search
from app.models.llm_client import LLMClient

logger = logging.getLogger(__name__)
llm = LLMClient()

MARKET_PROMPT = """
You are a startup market analyst. Given a market or industry name and a list of search results, provide a rough estimate of the market size (TAM) and growth rate.
Focus on finding concrete numbers if available in the snippets.

Market/Industry: {market}

Search Results:
{search_results}

Respond ONLY with a JSON object:
{{
  "market": "{market}",
  "tam": "Estimated Total Addressable Market (e.g. $50B by 2030 or 'Unknown')",
  "growth": "Estimated CAGR or growth trend (e.g. 15% or 'Stagnant')",
  "source_summary": "Short snippet about where this data comes from (e.g. 'Based on Grand View Research snippets')"
}}
"""

def market_estimator(market_or_industry: str) -> dict:
    """
    Given a market or industry name, return a rough estimate (e.g. TAM, growth rate).
    Uses web search and LLM to synthesize market data.
    """
    query = f"{market_or_industry} market size growth rate TAM 2025 2030"
    
    logger.info(f"Estimating market for: {market_or_industry}")
    
    try:
        search_results = web_search(query, max_results=8)
        
        # Format results for LLM
        results_text = ""
        for i, res in enumerate(search_results):
            results_text += f"{i+1}. {res['title']}\n   Snippet: {res['snippet']}\n   Link: {res['link']}\n\n"
        
        prompt = MARKET_PROMPT.format(market=market_or_industry, search_results=results_text)
        
        messages = [
            {"role": "system", "content": "You are a helpful market analysis assistant."},
            {"role": "user", "content": prompt}
        ]
        
        raw_response = llm.chat(messages).strip()
        
        # Robust JSON extraction
        json_match = re.search(r"(\{.*\})", raw_response, re.DOTALL)
        if json_match:
            raw_response = json_match.group(1)
        
        market_data = json.loads(raw_response)
        if not isinstance(market_data, dict):
            logger.warning("LLM returned non-dict for market estimate. Falling back.")
            raise ValueError("LLM returned non-dict for market estimate")
        
        # Save processed results
        from app.utils.helpers import save_data
        try:
            save_data(market_data, category='processed', base_filename='market_estimate')
        except Exception as e:
            logger.warning(f"Failed to save processed market data: {e}")
            
        return market_data

    except Exception as e:
        logger.error(f"Error in market_estimator: {e}")
        return {
            "market": market_or_industry,
            "tam": "Market size data unavailable (Fallback)",
            "growth": "Growth data unavailable (Fallback)",
            "source_summary": "Search failed or LLM provided incompatible format"
        }
