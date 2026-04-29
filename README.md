# AI Team Orchestration (framework template)

This repository is a **Cursor / AI team orchestration framework**: agents, skills, rules, guardrails, and hooks under [`.cursor/`](.cursor/) define how planning, approval, parallel execution, and review phases work. **[AGENTS.md](AGENTS.md)** is the entry point for humans and tools.

The **core product of this repo is the orchestration system**, not a particular application.

---

## Reference implementation (optional)

A **full-stack sample project** used to exercise orchestration patterns (atomic tasks, parallel lanes, pipelines, ML, tests) lives in isolation here:

**[`examples/orchestration-demo/`](examples/orchestration-demo/)**

That folder contains its own backend, frontend, data jobs, ML script, analytics helper, and tests. Treat it as a **replaceable reference**—clone the layout or delete it when you adopt this framework for a real codebase.

### Run the example

All commands assume the **`examples/orchestration-demo`** directory as the working directory.

**Backend (FastAPI + SQLite)**

```bash
cd examples/orchestration-demo/backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

**Data pipeline, ML, analytics** (from `examples/orchestration-demo`, after backend deps are installed)

```bash
cd examples/orchestration-demo
export PYTHONPATH=backend
python data/pipeline/ingest_csv.py
python data/pipeline/build_dimensions.py
python data/pipeline/transform_daily.py
python ml/train_score.py
python analytics/kpi.py
```

SQLite is created at `examples/orchestration-demo/data/fitness.db`.

**Frontend (Vite + React)**

```bash
cd examples/orchestration-demo/frontend
npm install
npm run dev
```

With the API on port 8000, Vite proxies `/workouts`, `/metrics`, and `/health` to the backend.

**Tests**

```bash
cd examples/orchestration-demo
pip install -r backend/requirements.txt
python -m pytest tests/ -q
```

---

## Replace the example with your project

1. Keep [`.cursor/`](.cursor/), [AGENTS.md](AGENTS.md), and root [README.md](README.md) (adapt this file’s wording if needed).
2. Remove or stop maintaining `examples/orchestration-demo/` when you no longer need the sample.
3. Add your application in its own tree (e.g. `services/`, `apps/`, or a separate repo) and point skills/agents at your stack via `.cursor/skills/` and task plans—not via the example paths above.

---

## Orchestration documentation

- [AGENTS.md](AGENTS.md) — playbook index and workflow narrative.
- [docs/ORCHESTRATION_DEMO.md](docs/ORCHESTRATION_DEMO.md) — illustrative PLAN / EXECUTION and gate excerpts mapped to the reference app location.
