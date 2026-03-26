import json
import logging
from app.tools.web_search import web_search
from app.models.llm_client import LLMClient

logger = logging.getLogger(__name__)
llm = LLMClient()

COMPETITOR_PROMPT = """
You are a startup market researcher. Given a startup idea and a list of search results, identify the top 3-5 direct or indirect competitors.
For each competitor, provide:
- name: The company name.
- description: A short (1-sentence) description of what they do.
- url: Their website URL if available.

Startup Idea: {idea}

Search Results:
{search_results}

Respond ONLY with a JSON list of objects:
[
  {{"name": "...", "description": "...", "url": "..."}},
  ...
]
"""

def competitor_finder(idea_summary: str, domain: str = None) -> list[dict]:
    """
    Given a short idea summary (and optional domain), return a list of potential competitors.
    Uses web search and LLM to identify and structure competition.
    """
    query = f"competitors for {idea_summary}"
    if domain:
        query += f" in the {domain} industry"
    
    logger.info(f"Finding competitors for: {idea_summary}")
    
    try:
        search_results = web_search(query, max_results=8)
        
        # Format results for LLM
        results_text = ""
        for i, res in enumerate(search_results):
            results_text += f"{i+1}. {res['title']}\n   Snippet: {res['snippet']}\n   Link: {res['link']}\n\n"
        
        prompt = COMPETITOR_PROMPT.format(idea=idea_summary, search_results=results_text)
        
        messages = [
            {"role": "system", "content": "You are a helpful market research assistant."},
            {"role": "user", "content": prompt}
        ]
        
        raw_response = llm.chat(messages).strip()
        
        # Clean potential markdown wrapping
        if raw_response.startswith("```"):
            raw_response = raw_response.split("```")[1]
            if raw_response.startswith("json"):
                raw_response = raw_response[4:]
        
        competitors = json.loads(raw_response)
        if not isinstance(competitors, list):
            logger.warning("LLM returned non-list for competitors. Falling back.")
            return [{"name": res["title"], "description": res["snippet"], "url": res["link"]} for res in search_results[:3]]
            
        return competitors

    except Exception as e:
        logger.error(f"Error in competitor_finder: {e}")
        # Fallback to a simpler search-based list if LLM fails
        return [{"name": res["title"], "description": res["snippet"], "url": res["link"]} for res in search_results[:3]]
