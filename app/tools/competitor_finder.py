"""
Competitor finder — TF-IDF + cosine similarity against processed startup dataset.
Finds top matching companies for a given startup idea and detects its industry.
Detected industry feeds directly into market_estimator().

Future: swap TF-IDF for sentence embeddings for semantic understanding.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.data_loader import load_processed


def competitor_finder(idea_summary: str, domain: str = None) -> list[dict]:
    """
    Given a short idea summary (and optional domain), return a list of potential competitors.
    Uses TF-IDF + cosine similarity against the processed startup dataset.

    domain: optional industry filter (e.g. "music", "fintech") — narrows the search
    Returns: [{"name": "...", "description": "...", "url": "...", "industry": "...", "similarity_score": ...}, ...]
    """
    startups = load_processed()

    # Filter by domain if provided
    pool = [s for s in startups if s["industry"].lower() == domain.lower()] if domain else startups
    if not pool:
        pool = startups  # fallback to full dataset if domain filter returns nothing

    # Build corpus: industry + description for richer matching
    corpus = [f"{s['industry']} {s['description'] or ''}" for s in pool]

    # TF-IDF vectorize corpus + idea query together
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus + [idea_summary])

    # Cosine similarity between the idea and every company
    scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    # Return top 5 matches
    top_indices = scores.argsort()[::-1][:5]
    results = []
    for i in top_indices:
        s = pool[i]
        results.append({
            "name":             s["company_name"],
            "description":      s["description"],
            "url":              None,  # dataset has no URLs — future: enrich via search
            "industry":         s["industry"],
            "status":           s.get("status"),
            "similarity_score": round(float(scores[i]), 4),
        })

    return results


if __name__ == "__main__":
    idea = "An online marketplace for booking music venues and artists"
    competitors = competitor_finder(idea)
    print(f"Top competitors:")
    for c in competitors:
        print(f"  {c['name']} ({c['industry']}) - score: {c['similarity_score']}")
