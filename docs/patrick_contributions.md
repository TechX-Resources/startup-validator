# Patrick Windeit — Contributions

## What Was Built

### Task 1 — Data Pipeline (`app/services/data_loader.py`)
- ETL pipeline ingesting 923 real startup records from Kaggle CSV
- Data quality checks — validates fields, flags bad records, generates quality report
- Dual storage — SQLite database (`startup_db.py`) + JSON backup
- Schema normalization — standardizes column names across different CSV formats
- `load_processed()` query layer used by all other tools
- Schema drift detection on every run (`schema_monitor.py`)

### Task 2 — Competitor Finder (`app/tools/competitor_finder.py`)
- TF-IDF vectorization of 923 company descriptions
- Cosine similarity engine to rank competitors against any startup idea
- Auto-detects industry from top match — feeds directly into market estimator
- Domain filtering — narrows search by industry if provided

### Task 3 — Market Estimator (`app/tools/market_estimator.py`)
- Industry lookup table with real TAM/growth data (25+ industries)
- SQL queries with CTEs and aggregation logic against SQLite — avg funding, success rate, VC ratio
- Stats pulled from real dataset, not made up

### Task 4 — FastAPI Pipeline (`app/main.py`)
- `POST /validate-idea` wires all tools into one endpoint
- `POST /validate-idea/async` — submits job and returns job_id immediately
- `GET /job/{job_id}` — poll for async validation result
- `GET /anomalies` — returns funding outliers flagged by z-score detection
- `GET /scores` — returns batch re-scoring results by model version
- `POST /rescore` — triggers batch re-score of all 923 companies
- Multi-factor viability scoring — weights competition, similarity density, success rate, VC presence
- OpenAI LLM integration for AI-generated summaries (falls back to template if no key)
- Full React frontend connected

### Task 5 — Data Quality & Monitoring (`app/services/`)
- `schema_monitor.py` — detects added/removed/renamed columns on every pipeline run
- `scoring.py` — batch re-scores all startups with version-controlled model comparisons
- `scoring.py` — z-score anomaly detection flags outlier funding records on ingestion

### Task 6 — Sentence Embeddings (`app/services/embeddings.py`)
- Pre-computes semantic embeddings for all 923 company descriptions using `all-MiniLM-L6-v2`
- Stored in `data/embeddings/` for fast retrieval
- `semantic_search()` function for meaning-based competitor matching
- Upgrade path from TF-IDF keyword matching to semantic understanding

---

## How to Run

### Full pipeline (ETL + quality checks + schema drift + SQLite + batch score + anomaly detection):
```bash
python -m app.services.data_loader
```

### Build semantic embeddings:
```bash
python -m app.services.embeddings
```

### Run batch re-scoring and anomaly detection standalone:
```bash
python -m app.services.scoring
```

### Test full competitor + market pipeline:
```bash
python test_pipeline.py
```

### Start API server:
```bash
uvicorn app.main:app --reload
```

### Start frontend:
```bash
cd frontend && npm run dev
```

---

## API Endpoints Added

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/validate-idea` | Validate a startup idea (sync) |
| POST | `/validate-idea/async` | Submit validation job (async) |
| GET | `/job/{job_id}` | Poll async job result |
| GET | `/anomalies` | Get funding outlier records |
| GET | `/scores` | Get batch scoring results |
| POST | `/rescore` | Trigger batch re-score |
| GET | `/health` | Health check |

---

## Files Created/Modified

| File | Status | Description |
|------|--------|-------------|
| `app/services/data_loader.py` | Modified | ETL pipeline with quality checks |
| `app/services/startup_db.py` | Created | SQLite storage + CTE query layer |
| `app/services/schema_monitor.py` | Created | Schema drift detection |
| `app/services/scoring.py` | Created | Batch re-scoring + anomaly detection |
| `app/services/embeddings.py` | Created | Sentence embeddings pipeline |
| `app/tools/competitor_finder.py` | Created | TF-IDF + cosine similarity |
| `app/tools/market_estimator.py` | Created | Industry TAM lookup + dataset stats |
| `app/main.py` | Modified | FastAPI endpoints wired to all tools |
| `data/raw/startup data.csv` | Added | 923-company Kaggle dataset |
| `data/processed/startups.json` | Generated | Cleaned JSON output |
| `data/processed/startups.db` | Generated | SQLite database |
| `data/embeddings/startup_embeddings.npz` | Generated | Sentence embeddings |
