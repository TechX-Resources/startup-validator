"""
Validator agent — AI-powered startup idea validation using Azure OpenAI.
Week 5: Implemented with LLM reasoning and structured output.
"""

import json
from app.models.llm_client import LLMClient


VALIDATION_SYSTEM_PROMPT = """You are an expert startup validator and investor advisor. Your role is to analyze startup ideas and provide honest, actionable feedback.

When given a startup idea, you must evaluate it across multiple dimensions:
1. Market viability and demand
2. Competitive landscape and differentiation
3. Technical feasibility and execution complexity
4. Business model potential
5. Risk factors and barriers to entry

You MUST respond with valid JSON in this exact format:
{
  "score": <float between 0.0 and 10.0>,
  "summary": "<2-3 sentence executive summary>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "risks": ["<risk 1>", "<risk 2>", "<risk 3>"],
  "competitors": ["<competitor 1>", "<competitor 2>", "<competitor 3>"],
  "market_notes": "<market size, growth trends, or TAM estimate>"
}

Be direct and honest. Focus on actionable insights over generic platitudes."""


def run_validator(idea: str, context: dict = None) -> dict:
    """
    Main entry: validate a startup idea using Azure OpenAI LLM.
    Returns a structured validation result (see app/schemas/response_schema.py).
    """
    if not idea or not idea.strip():
        raise ValueError("Idea cannot be empty.")
    
    # Initialize LLM client
    client = LLMClient()
    
    # Build messages
    messages = [
        {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
        {"role": "user", "content": f"Validate this startup idea:\n\n{idea}"}
    ]
    
    # Add optional context from memory if provided
    if context:
        context_str = json.dumps(context, indent=2)
        messages.append({"role": "system", "content": f"Additional context:\n{context_str}"})
    
    # Call LLM
    try:
        response_text = client.chat(messages=messages, temperature=0.7, max_tokens=1500)
        
        # Parse JSON response
        # Try to extract JSON from markdown code blocks if present
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()
        
        result = json.loads(json_str)
        
        # Validate required fields
        required_fields = ["score", "summary", "strengths", "risks", "competitors"]
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field}")
        
        # Ensure score is within bounds
        result["score"] = max(0.0, min(10.0, float(result["score"])))
        
        # Ensure market_notes exists (optional field)
        if "market_notes" not in result:
            result["market_notes"] = None
        
        return result
        
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse LLM response as JSON: {str(e)}. Response: {response_text[:200]}")
    except Exception as e:
        raise RuntimeError(f"Validation failed: {str(e)}")
