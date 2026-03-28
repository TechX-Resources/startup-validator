import os
import pytest
import json
from app.memory.memory_store import save, get_context
from app.tools.web_search import web_search
from app.tools.competitor_finder import competitor_finder
from app.tools.market_estimator import market_estimator
from app.config import settings

@pytest.fixture
def cleanup_data():
    """Fixture to clean up newly created data files after tests."""
    initial_raw = set(os.listdir("data/raw"))
    initial_processed = set(os.listdir("data/processed"))
    yield
    # We don't actually delete for this overall test so you can see the results,
    # but in a CI environment, you would.
    pass

def test_memory_integration():
    """Test Saving and retrieving from ChromaDB (Week 4)."""
    idea = "AI-powered coffee roasted by robots"
    result = {"score": 9.0, "summary": "Robot baritas are the future."}
    
    # Save to memory
    save(idea, result)
    
    # Retrieve context
    context = get_context("robotic coffee")
    assert len(context) > 0
    assert any(idea in c["idea"] for c in context)
    print(f"\n✅ Memory Store: Successfully retrieved context for '{idea}'")

def test_tool_persistence_integration():
    """Test tool execution and file persistence (Week 3)."""
    
    # 1. Test Web Search
    query = "current trends in robotic automation 2024"
    web_search(query, max_results=1)
    
    raw_files = [f for f in os.listdir("data/raw") if f.startswith("web_search_")]
    assert len(raw_files) > 0
    print(f"✅ Web Search: Saved raw data to data/raw ({raw_files[-1]})")

    # 2. Test Competitor Finder
    idea = "Autonomous delivery drones for pizza"
    competitor_finder(idea)
    
    processed_files = [f for f in os.listdir("data/processed") if f.startswith("competitors_")]
    assert len(processed_files) > 0
    print(f"✅ Competitor Finder: Saved processed data to data/processed ({processed_files[-1]})")

    # 3. Test Market Estimator
    industry = "Commercial Drone Delivery"
    market_estimator(industry)
    
    market_files = [f for f in os.listdir("data/processed") if f.startswith("market_estimate_")]
    assert len(market_files) > 0
    print(f"✅ Market Estimator: Saved processed data to data/processed ({market_files[-1]})")

def test_settings_and_models():
    """Ensure settings and models are correctly configured."""
    assert settings.app_name == "startup-idea-validator-agent"
    assert settings.llm_provider is not None
    # Check if serper key was added correctly (it should be since tools worked above)
    assert hasattr(settings, "serper_api_key")
    print("✅ Infrastructure: Settings and Model structure validated.")

if __name__ == "__main__":
    # Manual run support
    try:
        test_memory_integration()
        test_tool_persistence_integration()
        test_settings_and_models()
        print("\n✨ ALL INTEGRATION TESTS PASSED ✨")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
