"""
Validator agent — MCP-style orchestration: reason → choose tool → execute → repeat.
Week 5: Implement the loop and wire to LLM + tools + memory.
"""


def run_validator(idea: str, context: dict = None) -> dict:
    """
    Main entry: validate a startup idea using LLM + tools + optional context.
    Returns a structured validation result (see app/schemas/response_schema.py).

    Flow (TODO implement in Week 5):
    1. Build initial messages (system prompt + user idea + optional context from memory).
    2. Loop:
       a. Call LLM (model layer) with current messages.
       b. If LLM says "call tool X with args Y" → call tool, append result to messages, repeat.
       c. If LLM says "final answer" → parse into response_schema, return.
    3. Optional: store idea + result in memory (Week 4/5).
    """
    # TODO: Load LLM client from app.models, tools from app.tools.
    # TODO: Implement loop; return dict matching response_schema.
    raise NotImplementedError("Implement validator loop in Week 5.")
