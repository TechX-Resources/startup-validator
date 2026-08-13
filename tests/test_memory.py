import os
import pytest
from unittest.mock import patch, MagicMock
from app.config import settings
from app.memory import memory_store

# Use a temporary directory for vector database testing
TEST_DB_PATH = "./data/test_embeddings"

@pytest.fixture(autouse=True)
def setup_test_db():
    # Set settings vector_db_path to test directory
    original_path = settings.vector_db_path
    settings.vector_db_path = TEST_DB_PATH
    
    # Reset lazy singletons in memory_store
    memory_store._chroma_client = None
    memory_store._collection = None
    
    # Clear the database collection before the test
    try:
        collection = memory_store._get_collection()
        all_docs = collection.get()
        if all_docs and 'ids' in all_docs and all_docs['ids']:
            collection.delete(ids=all_docs['ids'])
    except Exception:
        pass
        
    yield
    
    # Clear the collection after the test
    try:
        if memory_store._collection is not None:
            all_docs = memory_store._collection.get()
            if all_docs and 'ids' in all_docs and all_docs['ids']:
                memory_store._collection.delete(ids=all_docs['ids'])
    except Exception:
        pass
        
    # Restore original path
    settings.vector_db_path = original_path
    memory_store._chroma_client = None
    memory_store._collection = None

def test_save_and_retrieve_memory():
    # Setup mock vectors of size 3
    mock_vector = [1.0, 0.0, 0.0]
    
    with patch('app.models.llm_client.LLMClient.embed', return_value=mock_vector):
        idea = "A mobile app for pet sitting"
        result = {"score": 8.0, "summary": "Great market potential."}
        
        # Save validation to store
        memory_store.save(idea, result)
        
        # Retrieve context
        context = memory_store.get_context(idea, top_k=1, threshold=0.1)
        
        assert len(context) == 1
        assert context[0]["idea"] == idea
        assert context[0]["result"] == result
        assert context[0]["similarity"] > 0.9  # Almost identical match

def test_vector_threshold_pruning():
    # Setup mock embeddings representing:
    # 1. Base Idea: [1.0, 0.0, 0.0]
    # 2. Similar Idea: [0.95, 0.05, 0.0] (Very close L2 distance)
    # 3. Dissimilar Idea: [0.0, 0.0, 1.0] (Far L2 distance)
    
    with patch('app.models.llm_client.LLMClient.embed') as mock_embed:
        # Save Similar Idea (embedding: [0.95, 0.05, 0.0])
        mock_embed.return_value = [0.95, 0.05, 0.0]
        memory_store.save(
            "Pet sitting app", 
            {"score": 8.0, "summary": "Good."}
        )
        
        # Save Dissimilar Idea (embedding: [0.0, 0.0, 1.0])
        mock_embed.return_value = [0.0, 0.0, 1.0]
        memory_store.save(
            "Crypto exchange for carbon credits", 
            {"score": 5.0, "summary": "Highly risky."}
        )
        
        # Query with Base Idea (embedding: [1.0, 0.0, 0.0])
        mock_embed.return_value = [1.0, 0.0, 0.0]
        
        # Case A: High similarity threshold (0.8) - should return ONLY the similar pet sitting app
        context_high_threshold = memory_store.get_context("Dog walker app", top_k=5, threshold=0.8)
        assert len(context_high_threshold) == 1
        assert context_high_threshold[0]["idea"] == "Pet sitting app"
        
        # Case B: Very low similarity threshold (0.1) - should return BOTH ideas
        context_low_threshold = memory_store.get_context("Dog walker app", top_k=5, threshold=0.1)
        assert len(context_low_threshold) == 2
        
        ideas_returned = [c["idea"] for c in context_low_threshold]
        assert "Pet sitting app" in ideas_returned
        assert "Crypto exchange for carbon credits" in ideas_returned
