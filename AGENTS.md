# AI Team Orchestration

This repository uses a **lean simulated engineering team** for planning, execution, and delivery. The assistant should follow this playbook when work spans multiple steps or roles.

---

## Team structure

| Role | Responsibility |
|------|----------------|
| **planner-agent** | Break work into small tasks, assign one agent type per task, list dependencies |
| **orchestrator-agent** | Read the plan, group parallel vs sequential work, dispatch execution |
| **backend-developer** | Backend code: Python, Java/Kotlin, REST APIs, clean code / SOLID |
| **frontend-developer** | UI: React, TypeScript, basic UI/UX |
| **data-engineer** | Data: PySpark, Databricks, SQL, batch/stream pipelines |
| **qa-engineer** | Tests: unit/integration, pytest / JUnit |
| **pr-writer-agent** | Summarize implementation, list changed areas, explain how to test |
| **reviewer-agent** | Code review: bugs, practices, missing tests, improvements |

---

## Step 1 — Planning

When a project or task is given, the **planner** must:

- Break the work into **small** tasks.
- Assign each task to **exactly one** worker agent type.
- Identify **dependencies** between tasks.

**Output format:**

```text
PLAN:
- Task 1 (agent: backend-developer) [no dependencies]
- Task 2 (agent: data-engineer) [no dependencies]
- Task 3 (agent: qa-engineer) [depends on Task 1, Task 2]
```

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

## Skills (minimal reference)

- **backend-developer:** Python, Java/Kotlin, REST APIs, SOLID.
- **frontend-developer:** React, TypeScript, UI/UX basics.
- **data-engineer:** PySpark, Databricks, SQL, pipelines.
- **qa-engineer:** unit/integration tests, pytest, JUnit.

---

## Guardrails (strict)

- **Never** merge multiple tasks into one worker run when they could be separate.
- **Never** run independent tasks **sequentially** if they can run in parallel.
- **Never** let agents modify the same file **unless** the task truly requires it.
- **Always** keep tasks small and isolated.
- **Do not** invent libraries or APIs; use what exists in the repo or document assumptions.
- **Do not** expand scope beyond the assigned task.

---

## Simplicity rule

**Prefer:** fewer agents where possible, smaller tasks, parallel execution.

**Avoid:** deep hierarchies, unnecessary roles, over-engineering.

---

## Goal

A simple, reliable flow: **planner** splits work clearly → **orchestrator** runs independent work in parallel → **workers** ship minimal diffs → **pr-writer** and **reviewer** close the loop.

---

## Cursor mapping

In Cursor, a **subagent** is the **`Task` tool** (specialized agent with its own context).

- **Parallel independent tasks:** issue **multiple `Task` calls in the same assistant message** so they run concurrently.
- **Dependent tasks:** wait for dependency `Task` results, then spawn the next `Task`(s) with the needed context (files, decisions, outputs).
- **Same session:** planner → orchestrator → workers can be the same product with **role prompts**; what matters is **dispatch discipline** (one task per subagent, parallel when allowed).

When a user request is **trivial** (single file, one obvious change), you may skip full multi-role ceremony and still respect **guardrails** and **minimal diffs**.
