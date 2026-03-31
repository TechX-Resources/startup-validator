import sys
import os
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()

from app.tools.web_search import web_search
from app.tools.competitor_finder import competitor_finder
from app.tools.market_estimator import market_estimator

def test_web_search():
    print("Testing web_search...")
    results = web_search("AI startup trends 2025")
    print(f"Results found: {len(results)}")
    for res in results[:2]:
        print(f"- {res['title']} ({res['link']})")
    print("Done.\n")

def test_competitor_finder():
    print("Testing competitor_finder...")
    idea = "A mobile app that uses AI to help users manage their personal finances by analyzing their spending patterns and providing personalized tips."
    competitors = competitor_finder(idea, "FinTech")
    print(f"Competitors found: {len(competitors)}")
    for comp in competitors:
        print(f"- {comp['name']}: {comp['description']} ({comp['url']})")
    print("Done.\n")

def test_market_estimator():
    print("Testing market_estimator...")
    market = "Personal Finance Management Software"
    estimate = market_estimator(market)
    print(f"Market Estimate for '{market}':")
    print(f"- TAM: {estimate.get('tam')}")
    print(f"- Growth: {estimate.get('growth')}")
    print(f"- Source: {estimate.get('source_summary')}")
    print("Done.\n")

if __name__ == "__main__":
    test_web_search()
    test_competitor_finder()
    test_market_estimator()
