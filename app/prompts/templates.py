"""
Prompt templates for the Startup Idea Validator Agent.

All prompts live here so they can be version-controlled, reviewed, and tuned
independently of the orchestration logic in app/agents/ and app/services/.

The response schema this module targets (app/schemas/response_schema.py):
    score        : float  (0–10)
    summary      : str
    strengths    : list[str]
    risks        : list[str]
    competitors  : list[str]
    market_notes : str | None
"""

from __future__ import annotations

from typing import Any

# ─────────────────────────────────────────────
# System prompt — defines the agent's persona,
# capabilities, and output contract.
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are the Startup Idea Validator, an expert analyst that evaluates early-stage \
startup ideas. You combine the rigour of a seasoned VC partner with the breadth \
of a market-research analyst.

## Capabilities
You have access to three tools that the orchestration layer may call on your behalf:
1. **WebSearch** — retrieve recent web snippets relevant to the idea.
2. **CompetitorFinder** — discover existing products or companies in the same space.
3. **MarketEstimator** — obtain rough TAM, growth-rate, and industry context.

When tool results are provided, incorporate them as evidence. When they are absent, \
rely on your training knowledge and clearly note any assumptions.

## Evaluation Criteria
Assess every idea across these dimensions:
- **Viability** — Is this a real problem? Can it be built and delivered?
- **Market Opportunity** — How large and growing is the addressable market?
- **Competitive Landscape** — Who else is doing this? What is the moat?
- **Strengths** — What gives this idea an edge?
- **Risks** — What could go wrong (market, execution, regulatory, technical)?

## Output Contract
You MUST respond with a single JSON object — no markdown fences, no preamble, no \
commentary outside the JSON. The schema is:

{
  "score": <float 0.0–10.0>,
  "summary": "<2–4 sentence executive summary>",
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "risks": ["<risk 1>", "<risk 2>", ...],
  "competitors": ["<competitor name 1>", "<competitor name 2>", ...],
  "market_notes": "<one-liner on market size/growth, or null if unknown>"
}

Rules for each field:
- **score**: 0 = fundamentally unviable, 10 = exceptional across every dimension. \
  Most ideas land between 3 and 8.
- **summary**: Plain English, no jargon. Lead with the strongest signal.
- **strengths / risks**: 2–5 items each; concise phrases, not full paragraphs.
- **competitors**: Real company or product names. Return an empty list only if the \
  space is genuinely greenfield.
- **market_notes**: A single sentence with a figure if possible (e.g. "$4.2 B TAM, \
  ~12 % CAGR"). Set to null when no credible estimate is available.
"""

# ─────────────────────────────────────────────
# Standalone format reminder — can be appended
# to any message when you need the LLM to
# re-focus on the output contract.
# ─────────────────────────────────────────────

RESPONSE_FORMAT_INSTRUCTIONS = (
    "Respond with ONLY a JSON object matching the schema: "
    '{"score": float, "summary": str, "strengths": [str], '
    '"risks": [str], "competitors": [str], "market_notes": str|null}. '
    "No markdown, no extra text."
)

# ─────────────────────────────────────────────
# User-prompt assembly
# ─────────────────────────────────────────────


def build_user_prompt(
    idea: str,
    *,
    web_results: str | None = None,
    competitor_results: str | None = None,
    market_results: str | None = None,
    memory_context: str | None = None,
) -> str:
    """Assemble the full user-turn prompt from the raw idea and optional tool outputs.

    Each tool section is only included when its data is present, keeping the
    prompt concise and the token budget predictable.
    """
    sections: list[str] = []

    sections.append(f"## Startup Idea\n{idea.strip()}")

    if memory_context:
        sections.append(
            f"## Prior Context (from memory)\n{memory_context}"
        )

    if web_results:
        sections.append(
            f"## Web Search Results\n{web_results}"
        )

    if competitor_results:
        sections.append(
            f"## Competitor Research\n{competitor_results}"
        )

    if market_results:
        sections.append(
            f"## Market Data\n{market_results}"
        )

    sections.append(
        "Based on all the information above, produce your validation assessment "
        "as the specified JSON object."
    )

    return "\n\n".join(sections)


# ─────────────────────────────────────────────
# Full message-list builders — ready to pass
# directly to LLMClient.chat()
# ─────────────────────────────────────────────


def build_validation_messages(
    idea: str,
    *,
    web_results: str | None = None,
    competitor_results: str | None = None,
    market_results: str | None = None,
    memory_context: str | None = None,
) -> list[dict[str, str]]:
    """Return the complete messages list for a single-shot validation call.

    Structure:
        [0] system  — persona + output contract
        [1] user    — idea + tool evidence + instructions

    Pass the return value straight into ``LLMClient.chat(messages=...)``.
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": build_user_prompt(
                idea,
                web_results=web_results,
                competitor_results=competitor_results,
                market_results=market_results,
                memory_context=memory_context,
            ),
        },
    ]


def build_tool_result_message(
    tool_name: str,
    result: Any,
) -> dict[str, str]:
    """Format a single tool's output as an assistant-context message.

    Useful in the multi-turn agent loop (Week 5) where tools are called
    one at a time and their results are appended to the conversation.
    """
    return {
        "role": "user",
        "content": (
            f"## Tool Result — {tool_name}\n"
            f"{_stringify(result)}"
        ),
    }


# ─────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────


def _stringify(value: Any) -> str:
    """Best-effort conversion of a tool return value to a prompt-friendly string."""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, dict)):
        import json
        return json.dumps(value, indent=2, default=str)
    return str(value)
