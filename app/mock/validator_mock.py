import json
import random
from typing import Dict, List, Union

def generate_mock_response(idea: str) -> Dict[str, Union[str, int, List[str]]]:
    """
    Gera uma resposta mock estruturada em JSON com variações baseadas no prompt.
    """
    
    # Pools de possíveis pontos fortes e riscos
    strengths_pool = [
        ["Mercado em crescimento", "Poucos concorrentes diretos"],
        ["Equipe com experiência no setor", "Tecnologia proprietária"],
        ["Modelo de negócio escalável", "Baixo custo de aquisição de clientes"],
        ["Parcerias estratégicas já alinhadas", "Demanda reprimida"],
    ]
    
    risks_pool = [
        ["Alta dependência de fornecedores", "Regulamentação futura incerta"],
        ["Concorrentes bem estabelecidos", "Tecnologia não testada"],
        ["Ciclo de vendas muito longo", "Alta taxa de churn prevista"],
        ["Mercado muito nichado", "Dificuldade de contratar talentos"],
    ]
    
    scores = [65, 72, 78, 81, 85, 90, 68, 74, 88]
    
    # Usa o hash da ideia para ser determinístico
    seed = hash(idea) % 10000
    random.seed(seed)
    
    strengths = random.choice(strengths_pool)
    risks = random.choice(risks_pool)
    score = random.choice(scores)
    
    # Define outlook baseado na pontuação
    if score >= 80:
        outlook = "positive"
    elif score >= 65:
        outlook = "neutral"
    else:
        outlook = "challenging"
    
    # Resumo automático
    summary = f"A ideia tem {strengths[0].lower()} e {strengths[1].lower()}, mas requer atenção a {risks[0].lower()} e {risks[1].lower()}."
    
    return {
        "idea": idea,
        "validation_score": score,
        "strengths": strengths,
        "risks": risks,
        "market_outlook": outlook,
        "summary": summary
    }

# Teste rápido
if __name__ == "__main__":
    ideia_teste = "Plataforma de delivery para pequenos restaurantes"
    resultado = generate_mock_response(ideia_teste)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))