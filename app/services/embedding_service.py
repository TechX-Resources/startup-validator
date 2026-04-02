

"""
Embedding Service

Responsible for generating embeddings for ideas or documents.

Design goals:
- Single model instance (avoid reloading model)
- Support batch embeddings
- Configurable model via environment variables
- Fast and thread-safe for API usage
"""

import os
import logging
from typing import List, Optional

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")

_model: Optional[SentenceTransformer] = None


def _load_model() -> SentenceTransformer:
    """
    Load embedding model lazily.
    """
    global _model

    if _model is None:
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL, device=EMBEDDING_DEVICE)

    return _model


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text input.
    """

    if not text.strip():
        raise ValueError("Cannot generate embedding for empty text")

    model = _load_model()

    vector = model.encode(text, normalize_embeddings=True)

    return vector.tolist()


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts (batch).
    Much faster than embedding individually.
    """

    if not texts:
        return []

    model = _load_model()

    vectors = model.encode(texts, normalize_embeddings=True)

    return [v.tolist() for v in vectors]