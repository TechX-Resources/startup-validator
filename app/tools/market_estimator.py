"""
Market estimator tool — rough market size or growth for a given market/industry.
"""

import json

def market_estimator(market_or_industry: str) -> dict:
    import json
from openai import OpenAI
from app.tools.web_search import web_search

client = OpenAI()


def market_estimator(market_or_industry: str) -> dict:
    """
    Given a market or industry name, return a rough estimate
    (TAM and growth signals) using search results + LLM extraction.

    Returns:
    {
        "market": "...",
        "tam": "...",
        "growth": "...",
        "source": "..."
    }
    """

    query = f"{market_or_industry} market size growth rate industry report"

    results = web_search(query, max_results=8)

    snippets = "\n".join(
        f"{r['title']} - {r['snippet']} ({r['url']})"
        for r in results
    )

    prompt = f"""
You are a startup market research assistant.

Using the search results below, estimate the market size
and growth rate for the industry.

Industry:
{market_or_industry}

Search results:
{snippets}

Return ONLY valid JSON in this format:

{{
  "market": "{market_or_industry}",
  "tam": "Estimated total addressable market with units if available",
  "growth": "Estimated growth rate or growth trend",
  "source": "URL of the most relevant source"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You extract market size estimates."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        market_data = json.loads(content)
    except json.JSONDecodeError:
        market_data = {
            "market": market_or_industry,
            "tam": "unknown",
            "growth": "unknown",
            "source": results[0]["url"] if results else "unknown"
        }

    return market_data


#testing
if __name__ == "__main__":
    result = market_estimator("AI recruiting software")
    print(result)