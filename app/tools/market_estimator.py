"""
Market estimator — keyword-based industry lookup + real dataset stats.
Takes an industry name (detected by competitor_finder) and returns
TAM, growth rate, competition level, and dataset-backed insights.
"""

from app.services.data_loader import load_processed


# Industry lookup table: TAM and growth rate estimates
INDUSTRY_DATA = {
    "software":    {"tam": "$650B",  "growth_rate": "11%", "competition": "High"},
    "web":         {"tam": "$100B",  "growth_rate": "15%", "competition": "High"},
    "mobile":      {"tam": "$935B",  "growth_rate": "14%", "competition": "High"},
    "enterprise":  {"tam": "$500B",  "growth_rate": "10%", "competition": "Medium"},
    "ecommerce":   {"tam": "$6.3T",  "growth_rate": "9%",  "competition": "High"},
    "biotech":     {"tam": "$497B",  "growth_rate": "13%", "competition": "Medium"},
    "advertising": {"tam": "$740B",  "growth_rate": "6%",  "competition": "High"},
    "gamesvideo":  {"tam": "$282B",  "growth_rate": "12%", "competition": "High"},
    "consulting":  {"tam": "$250B",  "growth_rate": "5%",  "competition": "Medium"},
    "music":       {"tam": "$26B",   "growth_rate": "7%",  "competition": "Medium"},
    "travel":      {"tam": "$1.5T",  "growth_rate": "8%",  "competition": "High"},
    "health":      {"tam": "$665B",  "growth_rate": "18%", "competition": "Medium"},
    "education":   {"tam": "$7.3T",  "growth_rate": "16%", "competition": "Medium"},
    "cleantech":   {"tam": "$380B",  "growth_rate": "22%", "competition": "Low"},
}

_DEFAULT = {"tam": "Unknown", "growth_rate": "Unknown", "competition": "Unknown"}


def _dataset_stats(industry: str) -> dict:
    """Pull real stats from the processed dataset for this industry."""
    startups = load_processed()
    sector = [s for s in startups if s.get("industry", "").lower() == industry.lower()]
    if not sector:
        return {"total_companies": 0}

    funded = [s for s in sector if s.get("funding_total")]
    avg_funding = sum(s["funding_total"] for s in funded) / len(funded) if funded else 0

    statuses = [s.get("status") for s in sector if s.get("status")]
    success = sum(1 for st in statuses if st in ("acquired", "ipo"))
    success_rate = round(success / len(statuses) * 100, 1) if statuses else 0

    return {
        "total_companies": len(sector),
        "avg_funding_usd": round(avg_funding),
        "success_rate_pct": success_rate,
        "vc_backed": sum(1 for s in sector if s.get("has_VC")),
    }


def market_estimator(market_or_industry: str) -> dict:
    """
    Given a market or industry name, return TAM, growth rate, competition level,
    and real stats pulled from the startup dataset.

    industry is typically detected and passed in by competitor_finder().
    """
    key = market_or_industry.lower()
    lookup = INDUSTRY_DATA.get(key, _DEFAULT)
    stats = _dataset_stats(market_or_industry)

    return {
        "market":    market_or_industry,
        "tam":       lookup["tam"],
        "growth":    lookup["growth_rate"],
        "competition": lookup["competition"],
        "dataset_insights": stats,
        "source": "TechX Startup Validator — internal dataset + industry estimates",
    }


if __name__ == "__main__":
    import json
    result = market_estimator("music")
    print(json.dumps(result, indent=2))
