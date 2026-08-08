import json
from app.models.llm_client import LLMClient

llm = LLMClient()

SYSTEM_PROMPT = """
You are a startup idea validator. Respond ONLY with a valid JSON object:
{
  "score": <float 0-10>,
  "summary": "<short summary>",
  "strengths": ["<strength1>", "<strength2>"],
  "risks": ["<risk1>", "<risk2>"],
  "competitors": ["<competitor1>", "<competitor2>"],
  "market_notes": "<market size or growth notes>"
}
"""

def run_validation(idea: str, user_id: str = None, session_id: str = None) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Validate this startup idea: {idea}"}
    ]
    try:
        raw = llm.chat(messages).strip()
        
        # Check if the chat returned an error dict structure
        if "error" in raw and ("LLM call failed" in raw or "No LLM provider initialized" in raw):
            raise ValueError(f"LLM Client returned error: {raw}")

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
                
        result = json.loads(raw)
        
        # Verify required keys exist
        required_keys = ["score", "summary", "strengths", "risks", "competitors"]
        if not all(k in result for k in required_keys):
            raise ValueError("LLM response missing required validation keys")
            
        return result
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Validation service LLM call failed ({e}). Falling back to mock validation data.")
        
        # Return a robust mock validation response matching the schema
        return {
            "score": 7.0,
            "summary": f"Mock Validation: The idea of '{idea}' looks promising with growing demand, but requires attention to scalability and competition.",
            "strengths": ["High automation potential", "Low upfront capital compared to traditional models"],
            "risks": ["High platform risk (algorithm dependency)", "High initial content creation effort"],
            "competitors": ["Other automation channels", "AI-powered video editors"],
            "market_notes": "Note: This is mock data returned because the LLM provider API call failed (e.g. quota exhausted or no API keys configured)."
        }