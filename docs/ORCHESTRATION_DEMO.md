# Orchestration demo — Personal Fitness Tracker

This document is a **reference** for how the [AGENTS.md](../AGENTS.md) multi-agent workflow maps onto this repository. It records a canonical **PLAN**, **EXECUTION**, and sample **gate outputs** (not live chat transcripts).

## 1. Planner output (illustrative)

```text
PLAN:
- Task B1: Workouts REST router (CRUD + list)
  - Required skills: backend.md
  - Dependencies: [no dependencies]
- Task B2: Metrics REST router (aggregated stats endpoints)
  - Required skills: backend.md
  - Dependencies: [no dependencies]
- Task B3: Health + root info router
  - Required skills: backend.md
  - Dependencies: [no dependencies]
- Task F1: Workout list UI
  - Required skills: frontend.md
  - Dependencies: [no dependencies]
- Task F2: Metrics dashboard UI
  - Required skills: frontend.md
  - Dependencies: [no dependencies]
- Task D1: Raw CSV ingestion job
  - Required skills: data-engineering.md
  - Dependencies: [no dependencies]
- Task D2: Activity type dimension seed
  - Required skills: data-engineering.md
  - Dependencies: [no dependencies]
- Task B4: Wire FastAPI app + CORS + mount routers
  - Required skills: backend.md
  - Dependencies: [depends on B1, B2, B3]
- Task D3: Daily aggregation job
  - Required skills: data-engineering.md
  - Dependencies: [depends on D1, D2]
- Task DS1: Train simple calorie model
  - Required skills: machine-learning.md
  - Dependencies: [depends on D3, B4]
- Task A1: KPI module + JSON export
  - Required skills: business-intelligence.md
  - Dependencies: [depends on D3, B4]
- Task F3: API client + shell wiring
  - Required skills: frontend.md
  - Dependencies: [depends on B4, F1, F2]
- Task T1: Automated API tests
  - Required skills: testing.md
  - Dependencies: [depends on B4]

STATUS: WAITING_FOR_APPROVAL
INSTRUCTION:
- Approve → explicit approval to run execution (e.g. "approved", "go ahead", "run")
- Request changes → revise plan only where asked; re-output full PLAN
- Reject → new PLAN from scratch
```

## 2. Orchestrator output (after approval)

**Same agent role, multiple parallel `Task` calls** in wave 1:

```text
EXECUTION:
SEQUENTIAL:
  Wave_impl:
    PARALLEL:
      - B1 → Assigned agent: backend-developer
      - B2 → Assigned agent: backend-developer
      - B3 → Assigned agent: backend-developer
      - F1 → Assigned agent: frontend-developer
      - F2 → Assigned agent: frontend-developer
      - D1 → Assigned agent: data-engineer
      - D2 → Assigned agent: data-engineer
    SEQUENTIAL:
      - B4 → Assigned agent: backend-developer
      - D3 → Assigned agent: data-engineer
    PARALLEL:
      - DS1 → Assigned agent: data-scientist
      - A1 → Assigned agent: data-analyst
    SEQUENTIAL:
      - F3 → Assigned agent: frontend-developer
      - T1 → Assigned agent: qa-engineer
SEQUENTIAL:
  - SEC1 → Assigned agent: security-engineer
  - QA1 → Assigned agent: qa-engineer
  - PR1 → Assigned agent: pr-writer-agent
  - RV1 → Assigned agent: reviewer-agent
```

Notes:

- **T1** uses `testing.md` (maps to **qa-engineer** in routing); for **automation tests** authored during implementation, teams may assign **backend-developer** instead—this demo uses **qa-engineer** for the formal test task before the security gate for simplicity in documentation. The **mandatory** rule is: **security-engineer** before **qa-engineer** verification gate **QA1** in the phase sense ([orchestration-rules](../.cursor/rules/orchestration-rules.md)). Adjust if your controller treats “write tests” as implementation work.

## 3. Security gate (sample)

```text
SECURITY REVIEW (illustrative):
- Gate: CLEAR
- Notes: SQLite file under data/; CORS allow_origins=["*"] suitable for local demo only — tighten for production.
- Recommendations: Restrict CORS; add auth if exposing beyond localhost.
```

## 4. QA gate (sample)

```text
QA VERIFICATION (illustrative):
- pytest tests/: PASS
- Manual: API /docs smoke, UI loads with proxy
- Gate: CLEAR for merge to feature branch
```

## 5. PR writer (lean body per pr-writer-agent)

Template:

```markdown
**Feature:** `fitness-tracker-demo`

## 🔍 Flow Impact Summary
- Adds a full-stack fitness reference app with parallel-friendly module boundaries
- API serves workouts and metrics; pipeline ingests CSV, builds dims, rolls up daily stats
- UI consumes API via Vite proxy

## 🧪 How to Test
- Backend: see root README
- Frontend: npm run dev with API running

## 📝 Notes
- Demo only; not production-hardened
```

## 6. Reviewer (sample `REVIEW RESULT`)

```text
REVIEW RESULT:
- status: APPROVED

ISSUES:
- None blocking for reference scope

RECOMMENDED ACTION:
- end workflow
```

(GitHub PR comment would mirror the lean template per [reviewer-agent](../.cursor/agents/reviewer-agent.md).)

## 7. Repo layout (implemented)

- `backend/` — FastAPI app, routers, models
- `frontend/` — React + Vite
- `data/pipeline/` — ingest, dimensions, transform
- `ml/` — simple sklearn export
- `analytics/` — KPI export script
- `tests/` — pytest + in-memory SQLite
