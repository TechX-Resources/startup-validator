"""
Memory store — persist past ideas, embeddings, and context for the agent.
Week 4: Implement with Chroma or similar (placeholder); Week 5: integrate with agent.
"""


def save(idea: str, result: dict, embedding: list[float] = None) -> None:
    """
    Save a validated idea and its result (and optional embedding) to the store.
    TODO: Persist to vector DB or simple storage; ensure embeddings go to data/embeddings if file-based.
    """
    # TODO: Implement in Week 4
    raise NotImplementedError("Implement save to memory/vector store.")


def get_context(idea: str, top_k: int = 5) -> list[dict]:
    """
    Retrieve relevant past context for this idea (e.g. similar ideas + their results).
    Returns list of dicts with idea, result, and any metadata.
    TODO: Optional embedding of idea, then similarity search in vector DB.
    """
    # TODO: Implement in Week 4
    raise NotImplementedError("Implement context retrieval from memory.")
