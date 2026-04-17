# Cursor-Training2.0

Cursor training and AI team orchestration configuration (see [AGENTS.md](AGENTS.md)).

## Task Tracker API (demo)

Small FastAPI + SQLite service under `task_tracker/`.

```bash
pip install -r requirements.txt
uvicorn task_tracker.main:app --reload
```

- `POST /tasks` — create task (`{"title": "..."}`)
- `GET /tasks` — list tasks
- `GET /tasks/{id}` — get one
- `PATCH /tasks/{id}` — update `done`

Run tests: `python -m pytest tests/ -q`
