# plan.md

## Understanding
You asked for three concrete outcomes in this pass:
1. Add the missing custom workflow prerequisite files (`agents.local.md` and `skills/setup-environment.md`).
2. Move implementation beyond planning by shipping cross-epic runtime foundations.
3. Implement a Qdrant runtime adapter at the right integration point.

Given scope (5 epics), I will deliver a practical vertical implementation that unlocks the remaining epics instead of only documentation:
- environment/workflow prerequisites,
- configurable model selection (inference + embedding),
- pluggable L2/vector backend with Qdrant runtime adapter,
- π backend scaffolding for ingestion/storage/cache sync,
- sprint/task updates pointing to concrete next executable work.

## Technical approach
1. Create `agents.local.md` and `skills/setup-environment.md`.
2. Extend edge config for inference/embedding/backend selectors.
3. Add vector backend abstraction with SQLite-compatible and Qdrant adapters.
4. Wire `L2Cache` to use selected backend (`sqlite` default, `qdrant` optional).
5. Add `pi_backend/` service scaffold with health + event ingestion + minimal storage integration.
6. Validate by static checks (`compileall`) and targeted lightweight tests where possible.

## Clarifying questions
1. Should Qdrant be mandatory in dev, or optional with graceful fallback when dependency/server is unavailable?
Answer: ______________________

2. Do you want me to prioritize finishing Epic 1 end-to-end before deepening π backend features in the next PR?
Answer: ______________________
