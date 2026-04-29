# Orchestration reference application

This directory is an **optional sample project** for the AI team orchestration framework in the repository root. It is **not** the core of the repo—see the root [README.md](../../README.md) and [AGENTS.md](../../AGENTS.md) for the orchestration playbook.

## Quick start

From this folder:

```bash
# Backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000

# Tests (new terminal, from this folder)
pip install -r backend/requirements.txt
python -m pytest tests/ -q

# Pipelines + ML + analytics (from this folder)
export PYTHONPATH=backend
python data/pipeline/ingest_csv.py
python data/pipeline/build_dimensions.py
python data/pipeline/transform_daily.py
python ml/train_score.py
python analytics/kpi.py

# Frontend
cd frontend && npm install && npm run dev
```

Replace this tree with your own product code when you outgrow the sample.
