# Startup Idea Validator — Developer Guide
---

 Overview
AI-powered FastAPI app that validates startup ideas using an LLM (Groq/OpenAI).
Returns a score, strengths, risks, competitors, and market notes.

---

 Setup

# 1. Clone the repo

git clone https://github.com/TechX-Resources/startup-validator
cd startup-validator


# 2. Create virtual environment

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux


# 3. Install dependencies

pip install -r requirements.txt
pip install slowapi pydantic-settings


# 4. Set up environment variables

cp .env.example .env

Add your API key to `.env`:

GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=
VECTOR_DB_PATH=./data/embeddings


# 5. Run the app
uvicorn app.main:app


# 6. Open API docs

http://localhost:8000/docs


---

 API Endpoints

# GET /health
Returns service status and version.

Response:
json
{"status": "ok", "service": "startup-idea-validator-agent", "version": "0.3.0"}


# POST /validate-idea
Validates a startup idea using LLM analysis.

Request:
json
{"idea": "Your startup idea here (10-1000 characters)"}


Response:
json
{
  "score": 7.5,
  "summary": "Strong idea with clear use case",
  "strengths": ["Clear pain point", "Scalable"],
  "risks": ["Crowded market", "Monetization unclear"],
  "competitors": ["LinkedIn", "Handshake"],
  "market_notes": "EdTech growing 12% CAGR"
}


---

 Security Features (Task 2)
- Input sanitization — strips dangerous characters (`<>{}`) from all inputs
- Length validation — rejects ideas under 10 or over 1000 characters
- Rate limiting — max 10 requests per minute per IP (via slowapi)
- CORS middleware — enabled for frontend access

---

 Input Validation (app/utils/validators.py)
python
sanitize_idea(idea)         # removes dangerous characters, strips whitespace
validate_idea_length(idea)  # enforces 10-1000 character limit


---

 Running Tests (Tasks 3 & 4)
C:\Users\quest\OneDrive\Desktop\TechX\startup-validator
python -m pytest tests/test_api.py -v


11 tests covering:
- Health endpoint (3 tests)
- Input validation — empty, short, too long, missing field, valid (5 tests)
- Security — XSS input, special characters, invalid endpoint (3 tests)

---

 Project Structure

app/
  main.py              - FastAPI entry point, rate limiting, CORS
  models/llm_client.py - LLM client 
  services/            - Validation pipeline
  schemas/             - Request/response models
  utils/validators.py  - Input sanitization and length validation
  utils/logger.py      - Shared logger
  config/settings.py   - Environment settings
tests/
  test_api.py          - 11 API tests (Quest Bokwe)
docs/
  developer_guide.md   - This file
