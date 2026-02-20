# Start Now — Immediate Task List

Generated: 2026-02-20  
Project: reachy-mini-retail-assistant

## Objective
Start implementation with the smallest high-impact slice while preserving the updated specs:
1) configurable inference/embedding model selection, and
2) swappable L2/vector backend (SQLite FTS5 baseline, Qdrant optional).

---

## 0) Pre-flight (30-45 min)
- [ ] Confirm local run passes for current edge app (`reachy_edge`) and existing tests.
- [ ] Create a working branch for Story 1.3 implementation.
- [ ] Copy acceptance criteria for Story 1.3 into your working notes.

Deliverable:
- Baseline test run output saved in PR description.

---

## 1) Start Story 1.3 (Product Lookup Tool) — **NOW**
Story ID: `1-3-product-lookup-tool-with-fts5-search`

- [ ] Implement/finish product lookup behavior for exact SKU, partial name, and typo-tolerant matching.
- [ ] Ensure response contract is concise and deterministic for wayfinding responses.
- [ ] Emit structured events for hit/miss/latency.
- [ ] Add unit tests for:
  - [ ] cache hit path
  - [ ] cache miss path
  - [ ] fuzzy/partial query behavior
  - [ ] error fallback path

Exit criteria:
- [ ] Story 1.3 ACs pass.
- [ ] Tests green for tool + API integration touchpoints.

---

## 2) Immediately queue Story 1.4 + 1.5 as one vertical slice
Stories:
- `1-4-l1-cache-in-memory-lru-for-hot-products`
- `1-5-interact-endpoint-for-product-queries`

- [ ] Wire L1 cache for hot products and misses fallback to L2.
- [ ] Make `/interact` endpoint route product queries through tool chain.
- [ ] Return consistent metadata (`intent`, `tool_used`, `cache_hit`, `latency_ms`).
- [ ] Add tests validating L1→L2 fallback and endpoint behavior.

Exit criteria:
- [ ] Fast-path query returns <500ms in local benchmark.
- [ ] Cache-hit instrumentation visible in logs.

---

## 3) Apply new spec requirements early (from merged PR)
- [ ] Add config keys for inference model selection (`provider`, `model`) in edge runtime config.
- [ ] Add config keys for embedding model selection (`provider`, `model`, `dimensions`) in π planning/runtime stubs.
- [ ] Add L2 backend selector (`sqlite` default, `qdrant` optional) in config contract (even if Qdrant adapter ships later).
- [ ] Ensure logging includes prompt/model identifiers for traceability.

Exit criteria:
- [ ] No hardcoded model IDs in core runtime path.
- [ ] Startup log prints active inference/embedding/L2 backend configuration.

---

## 4) Story status updates (PM hygiene)
- [ ] Move Story 1.3 to `in-progress` when coding starts.
- [ ] Keep 1.4 and 1.5 as next queued tasks.
- [ ] Update `next_story` in sprint tracker as each story advances.

---

## Suggested order for this week
1. Day 1: Story 1.3 implementation + tests
2. Day 2: Story 1.4 cache wiring + tests
3. Day 3: Story 1.5 `/interact` integration + tests
4. Day 4: Config abstraction pass (model + embedding + backend selector)
5. Day 5: Story 1.6 health/observability enhancement

---

## Definition of “Good Start”
By end of this start cycle, you should have:
- Story 1.3 done and reviewed,
- Story 1.4/1.5 at least in review,
- config contract in place for model/embedding/backend selection,
- clean test evidence for all touched paths.
