import json
import random
from typing import Dict, List, Union

def generate_mock_response(idea: str) -> Dict[str, Union[str, int, List[str]]]:
    """
    Generates a structured mock JSON response with variations based on the prompt.
    """
    
    strengths_pool = [
        ["Growing market", "Few direct competitors"],
        ["Experienced team in the sector", "Proprietary technology"],
        ["Scalable business model", "Low customer acquisition cost"],
        ["Strategic partnerships already aligned", "Pent-up demand"],
    ]
    
    risks_pool = [
        ["High dependency on suppliers", "Uncertain future regulation"],
        ["Well-established competitors", "Untested technology"],
        ["Very long sales cycle", "High expected churn rate"],
        ["Niche market too small", "Difficulty hiring talent"],
    ]
    
    scores = [65, 72, 78, 81, 85, 90, 68, 74, 88]
    
    seed = hash(idea) % 10000
    random.seed(seed)
    
    strengths = random.choice(strengths_pool)
    risks = random.choice(risks_pool)
    score = random.choice(scores)
    
    if score >= 80:
        outlook = "positive"
    elif score >= 65:
        outlook = "neutral"
    else:
        outlook = "challenging"
    
    summary = f"The idea has {strengths[0].lower()} and {strengths[1].lower()}, but requires attention to {risks[0].lower()} and {risks[1].lower()}."
    
    return {
        "idea": idea,
        "validation_score": score,
        "strengths": strengths,
        "risks": risks,
        "market_outlook": outlook,
        "summary": summary
    }

if __name__ == "__main__":
    test_idea = "Drone delivery app for small restaurants"
    result = generate_mock_response(test_idea)
    print(json.dumps(result, indent=2))"" 
