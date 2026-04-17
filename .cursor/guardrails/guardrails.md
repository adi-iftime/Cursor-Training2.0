# Guardrails

Cross-cutting **safety and quality** constraints. Agents, skills, and rules must all respect this layer.

## No scope creep

- Implement requested behavior only; do not add features, refactors, or dependencies not implied by the task.
- If a necessary improvement is discovered, record it as a **follow-up** instead of silently expanding the task.

## One task per execution slot

- Do not merge unrelated tasks into a single worker run when they could be separate.
- Do not batch “while I’m here” edits unrelated to the assigned task.

## No unrelated file modifications

- Avoid drive-by formatting or renames outside touched modules unless required to make the change compile or pass checks.

## Minimal diffs

- Prefer the smallest change that satisfies acceptance criteria and repository standards.
- Large mechanical edits belong in dedicated tasks with explicit approval.

## Deterministic task execution

- Dispatch the same plan the same way: respect declared dependencies; do not reorder parallelizable work into accidental serialization without cause.
- Record orchestration decisions (parallel vs sequential) so outcomes are auditable in-session.

## Parallelism hygiene

- Independent tasks should run **in parallel** when tooling allows (e.g. multiple `Task` calls in one turn), per orchestration rules.

## Honesty about capabilities

- Do not invent libraries, endpoints, or MCP behaviors; use what exists or document assumptions clearly.
