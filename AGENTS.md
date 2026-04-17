# AI Team Orchestration

This repository uses a **lean simulated engineering team** for planning, execution, and delivery. The assistant should follow this playbook when work spans multiple steps or roles.

---

## Team structure

| Role | Responsibility |
|------|----------------|
| **planner-agent** | Break work into small tasks; for each task list **required skills** first, then **resolve** the best-fit worker from the [Skill registry](#skill-registry-mandatory-for-routing); one agent per task; list dependencies |
| **orchestrator-agent** | Read the plan, group parallel vs sequential work, dispatch execution |
| **backend-developer** | Backend implementation (see skill registry) |
| **frontend-developer** | Frontend implementation (see skill registry) |
| **data-engineer** | Data / pipeline implementation (see skill registry) |
| **qa-engineer** | Test design and automation (see skill registry) |
| **pr-writer-agent** | Summarize implementation, list changed areas, explain how to test |
| **reviewer-agent** | Code review: bugs, practices, missing tests, improvements |

---

## Skill registry (mandatory for routing)

The planner **must** treat this table as the **source of truth** for which skills each worker covers. **Do not** use fixed “task type → agent” shortcuts; derive the agent from skills every time.

| Agent | Skills covered (non-exhaustive; add rows/columns as the team evolves) |
|-------|------------------------------------------------------------------------|
| **backend-developer** | Python; Java/Kotlin; REST APIs; services; clean code / SOLID |
| **frontend-developer** | React; TypeScript; UI/UX basics; client-side integration |
| **data-engineer** | PySpark; Databricks; SQL; batch/stream data pipelines |
| **qa-engineer** | Unit tests; integration tests; pytest; JUnit; quality gates |

**Future extensibility:** When a new role is introduced (e.g. **data-analyst** with Power BI, SQL, dashboards), **append** a row to this registry with that agent’s skills. The planner then matches task-required skills against the **updated** registry at planning time. Maintain **one** registry (here)—not a separate hardcoded routing map keyed by task names.

---

## Skill-based agent routing (mandatory)

### Rules

1. Each task **must** start from **required skills** (capabilities), not from a pre-picked agent.
2. The planner **must** map those skills to the **single best-fit** agent using the skill registry and the selection logic below.
3. Every planned task **must** show **both**:
   - **Required skills** (explicit list), and  
   - **Assigned agent** (resolved from skills, with brief rationale if helpful).

### Agent selection logic

For each task:

1. **Inspect** the skill registry and the task’s required skills.
2. **Match** task requirements to agents whose skills cover the needs.
3. **Choose** the **best fit**:
   - If **multiple** agents match → pick the **most specialized** agent (the narrowest role that still covers the requirement).
   - If **no** agent is an exact match → pick the **closest** agent and record a **`Skill gap:`** line (what is missing or assumed).

### Invalid planning (failure conditions)

Planning is **invalid** if it:

- Assigns agents **without** listing required skills first.
- **Hardcodes** agent choice by task label (e.g. “API task = backend-developer”) **without** a skill match justification tied to the registry.
- **Ignores** a clearly better-matching agent when that agent appears in the registry and covers more of the required skills.

### Example

**Task:** “Build ETL pipeline using Databricks”

**Step 1 — required skills:** Databricks; PySpark; batch data pipelines  

**Step 2 — agent resolution:** **data-engineer** (registry: Databricks, PySpark, pipelines)

**In plan output:** include the task title, the skill list, and `Assigned agent: data-engineer`.

---

## Step 1 — Planning

When a project or task is given, the **planner** must:

- Break the work into **small** tasks.
- For **each** task: enumerate **required skills**, then **assigned agent** (from the registry + selection logic above—never the reverse order).
- Identify **dependencies** between tasks.

**Output format** (every task includes skills **and** agent):

```text
PLAN:
- Task 1: <short title>
  - Required skills: <skill>, <skill>, …
  - Assigned agent: <agent>   (match: <one-line why, tied to registry>)
  - Dependencies: [no dependencies]

- Task 2: <short title>
  - Required skills: …
  - Assigned agent: …
  - Dependencies: [no dependencies]

- Task 3: <short title>
  - Required skills: …
  - Assigned agent: …
  - Dependencies: [depends on Task 1, Task 2]
```

If there is a skill gap: add `Skill gap: <what is not covered or assumed>` under that task.

Keep tasks **small** and **independent** when possible.

---

## Step 2 — Orchestration

The **orchestrator** must:

1. Read the plan.
2. Group tasks:

```text
PARALLEL:
- (list tasks with no unmet dependencies)

SEQUENTIAL:
- (list tasks that depend on others; order by dependency chain)
```

3. **Execution rules**
   - Each task **must** be executed using a **separate subagent** (see [Cursor mapping](#cursor-mapping) below).
   - If tasks are **independent** → run them **in parallel** (multiple subagents in one turn).
   - If tasks **depend** on others → run them **after** dependencies complete.

---

## Step 3 — Execution (worker agents)

Each worker must:

- **Only** perform its assigned task.
- **Not** modify unrelated files.
- Produce **clean, minimal** output (small diffs, clear changes).

---

## Step 4 — PR creation

The **pr-writer** must:

- Summarize what was implemented.
- List changed components / files / areas.
- Explain **how to test** (commands, scenarios, edge cases).

---

## Step 5 — Review

The **reviewer** must:

- Review the code and behavior against the task.
- Flag issues: bugs, bad practices, missing tests, security or reliability concerns.
- Suggest **concrete** improvements.

---

## Guardrails (strict)

- **Never** merge multiple tasks into one worker run when they could be separate.
- **Never** run independent tasks **sequentially** if they can run in parallel.
- **Never** let agents modify the same file **unless** the task truly requires it.
- **Always** keep tasks small and isolated.
- **Do not** invent libraries or APIs; use what exists in the repo or document assumptions.
- **Do not** expand scope beyond the assigned task.
- **Do not** skip **skill-first** routing: required skills must appear before the assigned agent in the plan.

---

## Simplicity rule

**Prefer:** fewer agents where possible, smaller tasks, parallel execution.

**Avoid:** deep hierarchies, unnecessary roles, over-engineering.

---

## Goal

A simple, reliable flow: **planner** splits work clearly and assigns workers **from required skills** → **orchestrator** runs independent work in parallel → **workers** ship minimal diffs → **pr-writer** and **reviewer** close the loop.

---

## Cursor mapping

In Cursor, a **subagent** is the **`Task` tool** (specialized agent with its own context).

- **Parallel independent tasks:** issue **multiple `Task` calls in the same assistant message** so they run concurrently.
- **Dependent tasks:** wait for dependency `Task` results, then spawn the next `Task`(s) with the needed context (files, decisions, outputs).
- **Same session:** planner → orchestrator → workers can be the same product with **role prompts**; what matters is **dispatch discipline** (one task per subagent, parallel when allowed).

When a user request is **trivial** (single file, one obvious change), you may skip full multi-role ceremony and still respect **guardrails** and **minimal diffs**.
