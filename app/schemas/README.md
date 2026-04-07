# app/schemas

**Purpose:** Structured inputs and outputs — VERY IMPORTANT for a clean API and for the LLM to produce parseable results. Use Pydantic models for request/response and for the agent’s final validation object.

**What students will implement:**
    - **idea_schema.py:** Request shape for “validate this idea” (e.g. idea text, optional fields).
    - **response_schema.py:** Response shape: score, summary, strengths, risks, competitors, market_notes, etc. Keep it stable so the frontend and agent can rely on it.
    - Include example JSON in comments so students and the LLM know the expected format.

**Weeks:** 2 (define schemas), then use everywhere in 3–6.

## Schemas

- idea_schema.py: defines the structure of idea request data
- response_schema.py: defines the structure of API responses

## Running the Backend Locally

1.Copy `.env.example` to `.env`
2.Install dependencies:

pip install -r requirements.txt

3.Run the server:

uvicorn app.main:app --reload

4.Open the API docs in browser:

<http://127.0.0.1:8000/docs>

## Example API Usage

### Request

POST /validate-idea

```json
{
  "idea": "An AI app that summarizes PDFs for students"
}
```

### Response

```json
{
  "score": 7.5,
  "summary": "Strong idea with clear use case; market is competitive.",
  "strengths": ["Clear problem", "Scalable solution"],
  "risks": ["High competition", "Monetization unclear"],
  "competitors": ["Notion AI", "ChatPDF"],
  "market_notes": "Growing demand in EdTech tools."
}
```
