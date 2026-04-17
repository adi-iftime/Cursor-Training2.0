# Orchestration rules

Configuration for **orchestrator-agent** behavior: ordering, parallelism, and **dynamic agent selection**.

## Inputs

- Planner output (`PLAN:`) with **required skills** and dependencies only.
- `.cursor/skills/*.md` for capability nuance when disambiguating.
- `.cursor/agents/*.md` for **role boundaries** (what a worker may/may not do)—not for embedded skill lists.

## Parallel vs sequential

- **PARALLEL:** tasks whose dependencies are satisfied and which do not require exclusive access to the same mutable artifacts (see guardrails for file ownership).
- **SEQUENTIAL:** tasks in dependency order; never run a task before all listed upstream tasks complete successfully.

## Agent selection (dynamic)

1. For each task, collect its **required skill references** (skill modules).
2. Map skill modules to **default executing roles** using the routing table below (extend by adding rows—**do not** hardcode mappings inside agent files).
3. If multiple roles could satisfy the task, choose the **most specialized** role whose responsibilities in `.cursor/agents/<role>.md` best match the **primary deliverable** of the task.
4. If no role fits, assign the **closest** role and record **`Skill gap:`** in the execution brief.
5. Emit an **execution plan** that adds `Assigned agent:` per task (this is the system-of-record for who runs the task).

### Default routing table (skill module → role)

| Skill module file | Default executing agent |
|-------------------|-------------------------|
| `backend.md` | `backend-developer` |
| `frontend.md` | `frontend-developer` |
| `data-engineering.md` | `data-engineer` |
| `testing.md` | `qa-engineer` |

**Multi-skill tasks:** pick the agent responsible for the **largest** or **riskiest** slice (primary deliverable). If the task truly spans equal-weight slices, **split the task** in planning rather than overloading one worker.

## Cursor execution mapping

- One runnable task → one **`Task` tool** invocation (subagent) unless guardrails forbid splitting.
- **Parallel** lane: multiple `Task` calls **in the same assistant turn** when tasks are independent.
- **Sequential** lane: await results, pass condensed context forward, then dispatch the next `Task`(s).

## Execution plan shape

```text
EXECUTION:
PARALLEL:
- Task A → Assigned agent: …
SEQUENTIAL:
- Task B → Assigned agent: …
```
