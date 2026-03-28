import json
import logging
import re
from app.tools.web_search import web_search
from app.models.llm_client import LLMClient
from app.utils.helpers import save_data

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
        
        if not raw_response:
            logger.error("LLM returned an empty response. Retrying once.")
            raw_response = llm.chat(messages).strip() # Retry once
        
        if not raw_response:
            logger.error("LLM returned an empty response after retry.")
            raise ValueError("LLM returned an empty response")

        # Robust JSON extraction
        json_match = re.search(r"(\[.*\]|\{.*\})", raw_response, re.DOTALL)
        if json_match:
            raw_response = json_match.group(1)
        
        try:
            competitors = json.loads(raw_response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in competitor_finder. Raw response: {raw_response}")
            raise e
        if not isinstance(competitors, list):
            logger.warning("LLM returned non-list for competitors. Falling back.")
            competitors = [{"name": res["title"], "description": res["snippet"], "url": res["link"]} for res in search_results[:3]]

        # Save processed results
        try:
            save_data(competitors, category='processed', base_filename='competitors')
        except Exception as e:
            logger.warning(f"Failed to save processed competitor data: {e}")

        return competitors

    except Exception as e:
        logger.error(f"Error in competitor_finder: {e}")
        # Fallback to a simpler search-based list if LLM fails
        return [{"name": res["title"], "description": res["snippet"], "url": res["link"]} for res in search_results[:3]]
