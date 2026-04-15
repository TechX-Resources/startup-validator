"""
Sentence embeddings pipeline using sentence-transformers.
Pre-computes and stores embeddings for all startup descriptions.
Used by competitor_finder as a semantic upgrade over TF-IDF.

Future: swap load_tfidf() for load_embeddings() in competitor_finder.py
"""

import json
import numpy as np
from pathlib import Path
from app.services.data_loader import load_processed

EMBEDDINGS_FILE = Path("data/embeddings/startup_embeddings.npz")
METADATA_FILE   = Path("data/embeddings/startup_metadata.json")
MODEL_NAME      = "all-MiniLM-L6-v2"  # fast, lightweight, 384-dim


def build_embeddings():
    """
    Load all startup descriptions, encode them with sentence-transformers,
    and save to data/embeddings/ for fast retrieval.
    """
    from sentence_transformers import SentenceTransformer

    startups = load_processed()
    model = SentenceTransformer(MODEL_NAME)

    corpus = [f"{s['industry']} {s.get('description') or ''}" for s in startups]
    metadata = [{"company_name": s["company_name"], "industry": s["industry"]} for s in startups]

    print(f"Encoding {len(corpus)} startup descriptions...")
    embeddings = model.encode(corpus, show_progress_bar=True)

    EMBEDDINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    np.savez(EMBEDDINGS_FILE, embeddings=embeddings)
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f)

    print(f"Saved embeddings to {EMBEDDINGS_FILE}")
    return embeddings, metadata


def load_embeddings() -> tuple[np.ndarray, list[dict]]:
    """Load pre-computed embeddings and metadata from disk."""
    if not EMBEDDINGS_FILE.exists():
        raise FileNotFoundError("Embeddings not found. Run embeddings.py first.")
    data = np.load(EMBEDDINGS_FILE)
    with open(METADATA_FILE) as f:
        metadata = json.load(f)
    return data["embeddings"], metadata


def semantic_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Find top_k most similar startups to query using cosine similarity on embeddings.
    Falls back to TF-IDF competitor_finder if embeddings are not built yet.
    """
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    embeddings, metadata = load_embeddings()
    model = SentenceTransformer(MODEL_NAME)

    query_vec = model.encode([query])
    scores = cosine_similarity(query_vec, embeddings).flatten()

    top_indices = scores.argsort()[::-1][:top_k]
    return [
        {**metadata[i], "similarity_score": round(float(scores[i]), 4)}
        for i in top_indices
    ]


if __name__ == "__main__":
    build_embeddings()
    results = semantic_search("An app for booking live music venues")
    for r in results:
        print(r)
