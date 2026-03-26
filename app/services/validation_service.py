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
    raw = llm.chat(messages).strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)