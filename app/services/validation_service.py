import json
from app.models.llm_client import LLMClient

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

MAX_RETRIES = 3


def _parse_json(raw: str) -> dict:
    """Strip markdown fences and parse JSON. Raises ValueError if malformed."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def run_validation(idea: str, user_id: str = None, session_id: str = None) -> dict:
    """
    Validate a startup idea using LLM. Retries up to MAX_RETRIES times
    if the response is malformed JSON before raising.
    """
    llm = LLMClient()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Validate this startup idea: {idea}"}
    ]

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        raw = llm.chat(messages).strip()
        try:
            return _parse_json(raw)
        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            # Ask LLM to fix its own output on retry
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": "That was not valid JSON. Please respond with only a valid JSON object."})

    raise ValueError(f"LLM returned malformed JSON after {MAX_RETRIES} attempts: {last_error}")
