"""
Competitor finder — semantic search using sentence embeddings with TF-IDF fallback.
Finds top matching companies for a given startup idea and detects its industry.
Detected industry feeds directly into market_estimator().
"""

from sklearn.metrics.pairwise import cosine_similarity
from app.services.data_loader import load_processed


def _semantic_search(idea: str, pool: list[dict]) -> list[tuple[int, float]]:
    """Use sentence embeddings for semantic similarity — understands meaning not just keywords."""
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from pathlib import Path

    EMBEDDINGS_FILE = Path("data/embeddings/startup_embeddings.npz")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_vec = model.encode([idea])

    # Use pre-built embeddings if available and pool is full dataset
    all_startups = load_processed()
    if len(pool) == len(all_startups) and EMBEDDINGS_FILE.exists():
        data = np.load(EMBEDDINGS_FILE)
        embeddings = data["embeddings"]
    else:
        corpus = [f"{s['industry']} {s.get('description') or ''}" for s in pool]
        embeddings = model.encode(corpus)

    scores = cosine_similarity(query_vec, embeddings).flatten()
    return list(enumerate(scores))


def _tfidf_search(idea: str, pool: list[dict]) -> list[tuple[int, float]]:
    """TF-IDF keyword fallback."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    corpus = [f"{s['industry']} {s.get('description') or ''}" for s in pool]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus + [idea])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    return list(enumerate(scores))


def competitor_finder(idea_summary: str, domain: str = None) -> list[dict]:
    """
    Given a short idea summary (and optional domain), return a list of potential competitors.
    Uses sentence embeddings for semantic matching, falls back to TF-IDF if unavailable.

    domain: optional industry filter — narrows the search
    Returns: [{"name": "...", "description": "...", "url": "...", "industry": "...", "similarity_score": ...}, ...]
    """
    startups = load_processed()
    pool = [s for s in startups if s["industry"].lower() == domain.lower()] if domain else startups
    if not pool:
        pool = startups

    # Try semantic search first, fall back to TF-IDF
    try:
        scored = _semantic_search(idea_summary, pool)
    except Exception:
        scored = _tfidf_search(idea_summary, pool)

    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:5]

    return [
        {
            "name":             pool[i]["company_name"],
            "description":      pool[i]["description"],
            "url":              None,
            "industry":         pool[i]["industry"],
            "status":           pool[i].get("status"),
            "similarity_score": round(float(score), 4),
        }
        for i, score in top
    ]


if __name__ == "__main__":
    idea = "A subscription app that uses AI to create personalized workout and meal plans"
    competitors = competitor_finder(idea)
    print("Top competitors:")
    for c in competitors:
        print(f"  {c['name']} ({c['industry']}) - score: {c['similarity_score']}")
