from app.tools.competitor_finder import competitor_finder
from app.tools.market_estimator import market_estimator

idea = "An online marketplace for booking music venues and artists"
competitors = competitor_finder(idea)
industry = competitors[0]["industry"]
market = market_estimator(industry)

print("=== COMPETITORS ===")
for c in competitors:
    print(f"  {c['name']} ({c['industry']}) - {c['similarity_score']}")

print(f"\n=== MARKET: {industry} ===")
print(f"  TAM: {market['tam']}  Growth: {market['growth']}  Competition: {market['competition']}")
print(f"  Dataset: {market['dataset_insights']}")
