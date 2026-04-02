"""
Memory store — persist past ideas, embeddings, and context for the agent.
Week 4: Implement with Chroma or similar (placeholder); Week 5: integrate with agent.
"""

import os
import uuid
from typing import List, Dict, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/embeddings")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


# Initialize embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)


# Initialize Chroma client
client = chromadb.Client(
    Settings(
        persist_directory=VECTOR_DB_PATH,
        anonymized_telemetry=False,
    )
)

collection = client.get_or_create_collection(
    name="startup_memory"
)


def _embed(text: str) -> List[float]:
    """Generate embedding for text."""
    return embedding_model.encode(text).tolist()


def save(idea: str, result: Dict, embedding: Optional[List[float]] = None) -> None:
    """
    Save a validated idea and its result (and optional embedding) to the store.
    """

    if embedding is None:
        embedding = _embed(idea)

    idea_id = str(uuid.uuid4())

    collection.add(
        ids=[idea_id],
        documents=[idea],
        embeddings=[embedding],
        metadatas=[{"result": str(result)}],
    )

    client.persist()


def get_context(idea: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieve relevant past context for this idea (similar ideas + their results).
    """

    embedding = _embed(idea)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
    )

    contexts = []

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        contexts.append(
            {
                "idea": doc,
                "result": meta.get("result"),
            }
        )

    return contexts