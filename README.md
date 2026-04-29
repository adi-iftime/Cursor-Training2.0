# Cursor-Training2.0

Cursor training and **AI team orchestration** configuration — see [AGENTS.md](AGENTS.md).

## Personal Fitness Tracker (reference app)

A small full-stack demo: **FastAPI** + **SQLite**, **React (Vite)** UI, **pandas/SQLAlchemy** pipelines, **scikit-learn** scoring, and **analytics** KPI export. The layout matches the orchestration demo in [docs/ORCHESTRATION_DEMO.md](docs/ORCHESTRATION_DEMO.md).

### Prerequisites

- Python 3.11+
- Node 18+ (for frontend)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Data pipeline (from repository root)

```bash
export PYTHONPATH=backend
python data/pipeline/build_dimensions.py
python data/pipeline/ingest_csv.py
python data/pipeline/transform_daily.py
python ml/train_score.py
python analytics/kpi.py
```

SQLite database file: `data/fitness.db` (created automatically).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

With the API on port 8000, Vite proxies `/workouts`, `/metrics`, and `/health` to the backend.

### Tests

From repository root:

```bash
pip install -r backend/requirements.txt
python -m pytest tests/ -q
```

### Orchestration reference

- [docs/ORCHESTRATION_DEMO.md](docs/ORCHESTRATION_DEMO.md) — canonical PLAN / EXECUTION excerpt and sample gate outputs.

