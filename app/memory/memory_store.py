import os
import json
import uuid
import logging
from app.config import settings
from app.models.llm_client import LLMClient

logger = logging.getLogger(__name__)

# Lazy singleton references for Chroma
_chroma_client = None
_collection = None

def _get_collection():
    """
    Lazily initialize the persistent ChromaDB client and get/create the collection.
    """
    global _chroma_client, _collection
    if _collection is None:
        import chromadb
        logger.info(f"Initializing persistent ChromaDB client at {settings.vector_db_path}")
        # Ensure directories exist
        os.makedirs(settings.vector_db_path, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=settings.vector_db_path)
        _collection = _chroma_client.get_or_create_collection("validated_ideas")
    return _collection

def save(idea: str, result: dict, embedding: list[float] = None) -> None:
    """
    Save a validated idea and its result (and optional embedding) to the store.
    """
    try:
        collection = _get_collection()
        
        # Generate embedding if not provided
        if not embedding:
            llm = LLMClient()
            embedding = llm.embed(idea)
            
        # Serialize the result dict as a JSON string under metadata
        # Chroma metadatas only support simple types (str, int, float, bool)
        metadata = {
            "result_json": json.dumps(result),
            "idea": idea
        }
        
        doc_id = str(uuid.uuid4())
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[idea],
            metadatas=[metadata]
        )
        logger.info(f"Successfully saved idea memory: {idea[:30]}...")
    except Exception as e:
        logger.error(f"Failed to save idea memory: {e}")

def get_context(idea: str, top_k: int = 3, threshold: float = None) -> list[dict]:
    """
    Retrieve relevant past context for this idea (e.g. similar ideas + their results).
    Applies vector-threshold context pruning to return only highly similar validations.
    """
    try:
        collection = _get_collection()
        
        # Generate query embedding
        llm = LLMClient()
        embedding = llm.embed(idea)
        
        # If the embedding generation failed or is mock (all zeros), return empty context
        if all(v == 0.0 for v in embedding):
            logger.warning("Zero vector generated for query. Skipping memory context lookup.")
            return []
            
        # Query ChromaDB
        results = collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
        
        if not results or not results['ids'] or not results['ids'][0]:
            return []
            
        # Default similarity threshold from settings if not specified
        if threshold is None:
            threshold = getattr(settings, 'similarity_threshold', 0.7)
            
        context_list = []
        
        # Parse matches and apply vector-threshold context pruning
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i]
            metadata = results['metadatas'][0][i]
            doc = results['documents'][0][i]
            
            # Map distance metric to similarity score:
            # L2 distance range: 0 to infinity (0 is identical).
            # Similarity = 1 / (1 + distance) maps it between 0.0 and 1.0.
            similarity = 1.0 / (1.0 + distance)
            
            if similarity >= threshold:
                try:
                    result_dict = json.loads(metadata.get("result_json", "{}"))
                    context_list.append({
                        "idea": doc,
                        "result": result_dict,
                        "similarity": similarity
                    })
                    logger.info(f"Found similar validation context: {doc[:30]}... (similarity: {similarity:.2f})")
                except Exception as json_err:
                    logger.warning(f"Failed to parse metadata result_json: {json_err}")
                    continue
                    
        return context_list
    except Exception as e:
        logger.error(f"Failed to retrieve context from memory: {e}")
        return []
