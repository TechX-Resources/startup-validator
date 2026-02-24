"""
Validation service — connects API to validator agent and memory.
Week 5–6: Implement; use schemas for input/output.
"""


def run_validation(idea: str, user_id: str = None, session_id: str = None) -> dict:
    """
    Run full validation pipeline: optional context from memory → agent → optional save to memory → response.
    idea: Raw text of the startup idea.
    user_id / session_id: Optional, for memory lookup and storage.
    Returns: Dict matching response_schema (see app/schemas/response_schema.py).
    TODO: Call memory_store.get_context() if needed; call run_validator(); optionally memory_store.save(); return.
    """
    # TODO: Implement in Week 5–6
    raise NotImplementedError("Implement validation service: agent + memory glue.")
