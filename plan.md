# plan.md

## Understanding
You asked me to proceed immediately and execute in this order:
1. Finish Epic 1
2. Implement Epic 2 core flows
3. Harden Epic 3 backend
4. Implement Epic 4 sync
5. Add Epic 5 quality gates

And after execution, capture clarification requests for remaining requirements.

## Technical approach
- Epic 1: complete product lookup behavior, richer `/interact` output, cache apply endpoint, and enhanced `/health` stats.
- Epic 2 core: add interaction state machine, provider-agnostic LLM client, and STT/TTS adapter stubs.
- Epic 3 hardening: improve π backend ingestion validation, tenant/trace propagation, and cache sync shape.
- Epic 4 sync: support `since_version` in π sync and `/cache/apply` alias on edge.
- Epic 5 quality: add `pytest.ini` and CI workflow for compile+test quality gate.

## Clarifying questions (for next pass)
1. Should voice (STT/TTS) be wired to specific providers now (e.g., OpenAI/Whisper/ElevenLabs), or stay adapter-based until hardware validation?
Answer: ______________________

2. For sync protocol, do you want strict version reconciliation (reject stale applies) in this sprint, or permissive apply with warnings?
Answer: ______________________

3. Should Qdrant be enabled by default in any environment, or remain opt-in until benchmark thresholds are met?
Answer: ______________________
