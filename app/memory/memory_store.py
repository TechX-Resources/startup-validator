"""
Memory store — persist past ideas, embeddings, and context for the agent.
Week 4: Implement with Chroma or similar (placeholder); Week 5: integrate with agent.
"""

import json
import uuid
import logging
import chromadb
from chromadb.config import Settings
from app.config import settings

logger = logging.getLogger(__name__)

# Initialize ChromaDB persistent client
try:
    chroma_client = chromadb.PersistentClient(path=settings.chroma_path)
    collection = chroma_client.get_or_create_collection(name="startup_ideas")
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB: {e}")
    chroma_client = None
    collection = None

def save(idea: str, result: dict, embedding: list[float] = None) -> None:
    """
    Save a validated idea and its result (and optional embedding) to the store.
    Persists to ChromaDB.
    """
    if not collection:
        logger.warning("ChromaDB collection not initialized. Cannot save memory.")
        return

    doc_id = str(uuid.uuid4())
    
    # Chroma metadata must be strings, ints, floats or bools.
    metadata = {"result_json": json.dumps(result)}
    
    try:
        if embedding:
            collection.add(
                documents=[idea],
                metadatas=[metadata],
                embeddings=[embedding],
                ids=[doc_id]
            )
        else:
            collection.add(
                documents=[idea],
                metadatas=[metadata],
                ids=[doc_id]
            )
        logger.info(f"Saved idea to memory with ID {doc_id}")
    except Exception as e:
        logger.error(f"Error saving to ChromaDB: {e}")


def get_context(idea: str, top_k: int = 5) -> list[dict]:
    """
    Retrieve relevant past context for this idea (e.g. similar ideas + their results).
    Returns list of dicts with idea and result.
    """
    if not collection:
        logger.warning("ChromaDB collection not initialized. Cannot retrieve context.")
        return []

    try:
        # Query ChromaDB (it will embed the query automatically if no embeddings provided)
        results = collection.query(
            query_texts=[idea],
            n_results=top_k
        )
        
        context_list = []
        if results and results.get("documents") and results["documents"][0]:
            docs = results["documents"][0]
            metadatas = results["metadatas"][0]
            
            for doc, meta in zip(docs, metadatas):
                try:
                    result_dict = json.loads(meta.get("result_json", "{}"))
                    context_list.append({
                        "idea": doc,
                        "result": result_dict
                    })
                except json.JSONDecodeError:
                    continue
                    
        return context_list
    except Exception as e:
        logger.error(f"Error retrieving from ChromaDB: {e}")
        return []
