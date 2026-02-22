# Brownfield Assessment — Reachy Mini Retail Assistant

**Date:** 2026-02-21  
**Project:** reachy-mini-retail-assistant  
**Assessment Type:** Brownfield Re-baseline  
**Decision:** Strategic prune & refocus (not ground-up rewrite)  
**Integration:** [reachy_mini_karen_whisperer](https://github.com/chelleboyer/reachy_mini_karen_whisperer) (bot frontend)

---

## 1. Executive Summary

This project was originally scoped as a **"Universal Second Brain"** — a domain-agnostic classification engine spanning retail, personal, business, and research domains. That vision produced 5 epics, 39 stories, and planning artifacts graded A+ at the implementation gate.

**Reality check:** After ~6 weeks of implementation, the codebase has ~5,500 LoC across 4 components, but **no working end-to-end product**. The `/interact` endpoint never calls the LLM. Voice, movement, and classification are stubs. The backend is essentially empty. Two demo apps (demo/, brain_space/) are forked duplicates with no connection to the real system.

**Key insight (2026-02-21):** The [reachy_mini_karen_whisperer](https://github.com/chelleboyer/reachy_mini_karen_whisperer) repo — a fork of Pollen Robotics' `reachy_mini_conversation_app` — already provides the entire human interface layer: voice I/O (OpenAI Realtime API), LLM conversation, robot gestures, signal intelligence, Slack escalation, and Gradio test UI. This repo does NOT need to be a full application. It needs to be a **data microservice** that Karen Whisperer's custom tools call via HTTP.

**Decision:** Re-scope to a focused **Retail Data Service MVP** with 6 stories. Preserve the ~1,850 LoC + 776 LoC tests that are production-worthy. Discard/freeze everything else. The "Universal Second Brain" becomes the v2 roadmap, not the v1 deliverable.

---

## 2. Codebase Inventory

### 2.1 Total Lines of Code

| Component | LoC | Tests LoC |
|-----------|-----|-----------|
| `reachy_edge/` | ~2,300 | ~776 |
| `backend/` | ~190 | ~20 |
| `demo/` | ~1,930 | 0 |
| `brain_space/` | ~342 | 0 |
| **Total** | **~4,762** | **~796** |

### 2.2 Component-Level Assessment

#### `reachy_edge/` — Edge Backend (Primary Application)

| Module | LoC | Quality | Verdict |
|--------|-----|---------|---------|
| `cache/l1_cache.py` | 90 | **High** — Thread-safe, TTL, LRU eviction, stats | **KEEP** |
| `cache/l2_cache.py` | 310 | **High** — SQLite FTS5 + BM25, async facade, promo support | **KEEP** |
| `cache/vector_backends.py` | 210 | **Mixed** — SQLite keyword backend works; Qdrant uses fake embeddings | **KEEP (remove Qdrant stub)** |
| `cache/schemas.py` | 35 | **Good** — Clean Pydantic models | **KEEP** |
| `tools/base.py` | 55 | **Good** — ABC base, DI container, ToolResult model | **KEEP** |
| `tools/product_lookup.py` | 100 | **Good** — L1→L2 fallback, event emission, response formatting | **KEEP** |
| `tools/promo_manager.py` | 85 | **Good** — L1→L2 promo lookup with events | **KEEP** |
| `tools/selfie.py` | 55 | Stub — canned responses, no camera | **FREEZE** |
| `tools/movement.py` | 45 | Stub — logs intent, does nothing | **FREEZE** |
| `models/__init__.py` + files | 110 | **Good** — Pydantic v2, well-documented | **KEEP** |
| `config.py` | 57 | **Good** — Pydantic Settings, env file support | **KEEP** |
| `main.py` | 256 | **Mixed** — FastAPI skeleton good; `/interact` needs rewrite | **KEEP (rewrite /interact)** |
| `llm/inference.py` | 105 | **Partial** — OpenAI path works; local mode is TODO | **KEEP (fix model name)** |
| `llm/client.py` | 35 | **Good** — cache-only system prompt wrapper | **KEEP** |
| `llm/prompt_manager.py` | 95 | **Good** — templating, word-count validation, hallucination detection | **KEEP** |
| `brain_client/event_emitter.py` | 130 | **Good** — Async batched worker with backpressure | **KEEP** |
| `fsm/interaction_fsm.py` | 25 | Trivial — 4 states, no guards or side effects | **REWRITE later** |
| `voice/stt.py` | 8 | Pure stub | **FREEZE** |
| `voice/tts.py` | 8 | Pure stub | **FREEZE** |
| `data/sample_products.py` | 406 | **Good** — 44 realistic products, 8 categories | **KEEP (merge demo's expanded set)** |

#### `backend/` — Second Brain Backend

| Module | LoC | Quality | Verdict |
|--------|-----|---------|---------|
| `main.py` | 32 | Minimal — 3 endpoints, correct contracts | **FREEZE** |
| `config.py` | 25 | Good — Pydantic Settings | **FREEZE** |
| `models.py` | 18 | Good — basic response models | **FREEZE** |
| `cache/generator.py` | 15 | **Stub** — returns empty lists | **FREEZE** |
| `db/canonical_store.py` | 45 | Minimal — SQLite event store, stringified payloads | **FREEZE** |
| `db/knowledge_graph.py` | 25 | **Stub** — write-only, no queries | **FREEZE** |
| `db/vector_store.py` | 25 | **Stub** — only has `stats()` | **FREEZE** |

**Verdict:** Entire `backend/` is **FROZEN** for MVP. It's the "Second Brain" universal backend — out of v1 scope. Keep the code as-is for future reference; do not invest in it until edge MVP ships.

#### `demo/` — Gradio Demo Apps

| Module | LoC | Quality | Verdict |
|--------|-----|---------|---------|
| `app.py` | 357 | Functional — Gradio 6.0 + HuggingFace Llama 3 | **KEEP (as demo)** |
| `gradio_app.py` | 337 | Older duplicate — OpenAI + sys.path hacks | **DELETE** |
| `cache/l2_cache.py` | 447 | Enhanced fork — fuzzy matching, keyword expansion | **MERGE into reachy_edge** |
| `data/sample_products.py` | 776 | Expanded — 80+ products | **MERGE into reachy_edge** |
| `models/__init__.py` | 15 | Standalone copy | **DELETE (use reachy_edge models)** |

#### `brain_space/` — Classification Demo

| Module | LoC | Quality | Verdict |
|--------|-----|---------|---------|
| `app.py` | 342 | In-memory toy — keyword classifier, 5 products, no persistence | **FREEZE** |

**Verdict:** Not connected to anything. Freeze for potential future admin UI reference.

### 2.3 Test Suite

| Test File | LoC | Coverage | Verdict |
|-----------|-----|----------|---------|
| `reachy_edge/tests/test_l2_cache.py` | 531 | L2 cache comprehensive (FTS5, BM25, threading, edge cases) | **KEEP** |
| `reachy_edge/tests/test_cache.py` | 85 | L1 + L2 basic ops, async promos | **KEEP** |
| `reachy_edge/tests/test_tools.py` | 85 | ProductLookup + PromoManager tools | **KEEP** |
| `reachy_edge/tests/test_main.py` | 55 | `/health` endpoint | **KEEP** |
| `backend/tests/test_main.py` | 20 | Backend `/health` + `/events/batch` | **FREEZE** |

**Test infrastructure:** pytest + asyncio_mode=auto, Windows file-locking workarounds, temp file cleanup. Well-configured.

---

## 3. Known Issues & Tech Debt

### Critical (Blocks MVP)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| 1 | `/interact` never calls LLM — returns static tool output | `reachy_edge/main.py` `_classify_intent()` | **No conversational product** |
| 2 | Intent classification is naive keyword matching | `reachy_edge/main.py` | Wrong intents for natural language |
| 3 | Hardcoded model name `gpt-4.1-mini` (doesn't exist) | `reachy_edge/config.py` | LLM calls would fail |

### Moderate (Should fix in MVP)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| 4 | Qdrant backend uses fake embeddings (`_embed()` = char ordinals) | `cache/vector_backends.py` | Not real vector search |
| 5 | Demo cache has better fuzzy matching than reachy_edge cache | `demo/cache/l2_cache.py` | Diverged codebases |
| 6 | Sample data diverged (44 vs 80+ products) | `reachy_edge/data/` vs `demo/data/` | Inconsistent test data |
| 7 | Event payloads stored as `str(event)` not JSON | `backend/db/canonical_store.py` | Data not queryable |

### Low (Deferred to post-MVP)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| 8 | Voice STT/TTS are empty stubs | `reachy_edge/voice/` | No voice capability |
| 9 | Movement/selfie tools are stubs | `reachy_edge/tools/` | No hardware integration |
| 10 | FSM is trivial (no guards/effects) | `reachy_edge/fsm/` | Not a real state machine |
| 11 | Backend classification pipeline doesn't exist | `backend/` | "Second Brain" not built |
| 12 | No auth on any endpoint | All services | Security gap |

---

## 4. Dependencies

| File | Key Deps | Notes |
|------|----------|-------|
| `reachy_edge/requirements.txt` | `fastapi>=0.109`, `uvicorn`, `pydantic>=2.5`, `pydantic-settings>=2.1`, `httpx>=0.26`, `structlog>=24.1`, `openai>=1.12` (optional) | Solid, modern stack |
| `reachy_edge/pyproject.toml` | Python `>=3.11`, optional groups for `openai` and `test` | Well-structured |
| `backend/requirements.txt` | `fastapi>=0.109`, `uvicorn`, `pydantic>=2.5`, `pydantic-settings>=2.1` | Minimal |
| `demo/requirements.txt` | `gradio>=6.0`, `rapidfuzz>=3.0`, `huggingface-hub>=0.20` | Version conflict with brain_space (gradio >=4.0 vs >=6.0) |

**No dependency issues** for the MVP scope (reachy_edge only).

---

## 5. What We Keep (The Foundation)

**~1,850 LoC of production-quality code + ~776 LoC of tests:**

- **Cache system** (L1 + L2 + FTS5 + BM25) — core competitive advantage, well-tested
- **Tool framework** (base + product_lookup + promo_manager) — clean DI, event emission
- **Event emitter** — async batching with backpressure, ready for when backend comes online
- **Data models** — Pydantic v2, well-documented, correct contracts
- **Configuration** — env-based settings, extensible
- **FastAPI skeleton** — lifespan management, middleware, CORS, routing
- **LLM infrastructure** — inference client, prompt manager (just needs to be wired in)
- **Test suite** — comprehensive cache tests, tool tests, API tests

---

## 6. What We Cut / Freeze

### Freeze (Keep code, stop investing)

| Component | Reason |
|-----------|--------|
| `backend/` (entire) | "Second Brain" is v2 scope |
| `brain_space/` (entire) | Standalone toy, no integration |
| `reachy_edge/voice/` | Hardware integration deferred |
| `reachy_edge/tools/selfie.py` | Hardware integration deferred |
| `reachy_edge/tools/movement.py` | Hardware integration deferred |
| `reachy_edge/fsm/` | Trivial implementation, rewrite when voice added |
| Epics 2-5 (all 33 stories) | Out of MVP scope |

### Delete / Consolidate

| Action | Target |
|--------|--------|
| Delete | `demo/gradio_app.py` (older duplicate) |
| Merge into reachy_edge | `demo/cache/l2_cache.py` fuzzy matching enhancements |
| Merge into reachy_edge | `demo/data/sample_products.py` expanded product set (80+ items) |
| Delete | `demo/models/__init__.py` (duplicate of reachy_edge models) |

---

## 7. Architecture Decision: Two-Repo Integration

### System Architecture

```
Customer (voice)
    ↓
Karen Whisperer (OpenAI Realtime API + Reachy Mini robot)
    ├── Voice I/O (STT/TTS)          ── KW repo, already built
    ├── LLM conversation (gpt-realtime) ── KW repo, already built
    ├── Robot gestures (dance/emotion)   ── KW repo, already built
    ├── Signal intelligence              ── KW repo, already built
    ├── Slack escalation                 ── KW repo, already built
    │
    └── Custom Tools (OpenAI function calling)
        ├── lookup_product()  ──HTTP──→  Retail Assistant API  ──→  FTS5 Cache
        ├── get_promos()      ──HTTP──→  Retail Assistant API  ──→  Promo Cache
        └── get_store_info()  ──HTTP──→  Retail Assistant API  ──→  Config
```

| Concern | Owner | Repo |
|---|---|---|
| Voice I/O (STT/TTS) | Karen Whisperer | `reachy_mini_karen_whisperer` |
| LLM conversation | Karen Whisperer | `reachy_mini_karen_whisperer` |
| Robot gestures | Karen Whisperer | `reachy_mini_karen_whisperer` |
| Personality / system prompt | Karen Whisperer (profiles/) | `reachy_mini_karen_whisperer` |
| Tool dispatch | Karen Whisperer (OpenAI function calling) | `reachy_mini_karen_whisperer` |
| Signal tracking + Slack | Karen Whisperer | `reachy_mini_karen_whisperer` |
| **Product data + search** | **Retail Assistant API** | **This repo** |
| **Promo data** | **Retail Assistant API** | **This repo** |
| **Store configuration** | **Retail Assistant API** | **This repo** |

### What this means for this repo

This repo becomes a **pure data microservice** — FastAPI + FTS5 cache + product/promo/store endpoints. No LLM, no voice, no FSM, no gestures. Those are all Karen Whisperer's job.

The existing code that handles LLM inference, prompt management, voice stubs, FSM, and movement stubs is **unnecessary** and should be frozen.

---

## 8. Scope Decision

### Original Scope (v1 as planned)
- 5 Epics, 39 Stories
- Universal Second Brain platform
- Voice, gestures, LLM, classification pipeline, knowledge graph, multi-tenant, CI/CD
- Estimated effort: Many months

### New Scope (Retail Data Service MVP)
- 1 Epic, 6 Stories (see: `mvp-stories-2026-02-21.md`)
- Pure data service: product search, promo data, store config via REST API
- Consumed by Karen Whisperer's custom tools via HTTP
- Estimated effort: 1-2 weeks

### What Karen Whisperer Already Provides (no work needed here)
- Voice I/O via OpenAI Realtime API
- LLM-powered conversation with personality
- Robot gesture coordination
- Signal intelligence (pattern detection)
- Slack escalation for store teams
- Gradio web UI for testing

### Deferred to v2+
- Backend "Second Brain" classification pipeline
- Knowledge graph
- Multi-tenant architecture
- Edge-Brain sync / cache sync protocol
- Production hardening (full CI/CD, security, monitoring)

---

## 9. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Karen Whisperer tool interface changes | Low | Medium | Pin to known working version, follow Pollen Robotics patterns |
| Network latency between KW and retail service | Low | Low | Both run on same device or local network |
| FTS5 search quality for natural language | Low | Medium | Demo/cache fuzzy matching already solved this |
| Scope creep back to "universal" | High | High | Strict story boundaries, no backend work in v1 |
| Existing tests break during refactor | Low | Low | Run tests before and after each change |
| Karen Whisperer upstream breaking changes | Medium | Medium | Fork is independent; merge upstream selectively |

---

## 10. Recommended Immediate Actions

1. ~~**Update sprint tracker**~~ ✅ DONE — Reset to new MVP scope (7 stories incl. Mind Monitor)
2. ~~**Create MVP story files**~~ ✅ DONE — See `mvp-stories-2026-02-21.md`
3. **Merge demo enhancements** — Fuzzy matching + expanded products into reachy_edge
4. **Delete dead code** — `demo/gradio_app.py`, duplicate models
5. ~~**Add API endpoints**~~ ✅ DONE — `/api/products/search`, `/api/promos/active`, `/api/store/info` in `reachy_edge/api/routes.py`
6. ~~**Create Karen Whisperer tools**~~ ✅ DONE — `lookup_product`, `get_active_promos`, `get_store_info` + `tools.txt` + `instructions.txt` + `.env`
7. **Freeze unnecessary code** — LLM inference, voice stubs, FSM, movement (Karen Whisperer handles these)
8. ~~**Integration test**~~ ✅ DONE — 26 tests in `test_integration.py` (happy, error, load, conversation flow)
9. **Ship** — A working data service that Karen Whisperer calls to answer "where's the milk?"

---

## 11. Implementation Progress (updated 2026-02-21T23:30Z)

### New files created this session:
| File | Purpose |
|------|---------|
| `reachy_edge/mind/__init__.py` | MindBus event bus — async pub/sub, ring buffer, SSE fan-out |
| `reachy_edge/mind/routes.py` | SSE stream, state snapshot, product browser, KW signal ingestion |
| `reachy_edge/mind/dashboard.html` | Real-time HTML/JS/CSS dashboard |
| `reachy_edge/api/__init__.py` | Public API package init |
| `reachy_edge/api/routes.py` | 3 REST endpoints for Karen Whisperer tools |

### Files modified this session:
| File | Change |
|------|--------|
| `reachy_edge/main.py` | Added MindMiddleware, API router, sample data loading at startup |
| `reachy_edge/cache/l2_cache.py` | Added `get_all_products()`, `product_count()`, `clear()` methods to all cache layers; enriched `stats()` |

### Verified endpoints (all tested 2026-02-21):
| Endpoint | Status | Notes |
|----------|--------|-------|
| `GET /api/products/search?q=diesel` | ✅ 200 | Returns FTS5 results with BM25 relevance scores |
| `GET /api/promos/active` | ✅ 200 | Returns `[]` until promos are loaded |
| `GET /api/store/info` | ✅ 200 | Returns 8 categories, 44 products count |
| `GET /mind` | ✅ 200 | Dashboard loads, SSE connects |
| `GET /mind/events` | ✅ SSE | Real-time event stream |
| `POST /mind/signal` | ✅ 200 | Karen Whisperer signal ingestion |

### Test results: 35 passed, 0 failed

### Karen Whisperer integration (Story 5 — completed):
| File (in karen_whisperer repo) | Purpose |
|------|---------|
| `profiles/retail_assistant/lookup_product.py` | `LookupProductTool` — calls `GET /api/products/search` via httpx |
| `profiles/retail_assistant/get_active_promos.py` | `GetActivePromosTool` — calls `GET /api/promos/active` via httpx |
| `profiles/retail_assistant/get_store_info.py` | `GetStoreInfoTool` — calls `GET /api/store/info` via httpx |
| `profiles/retail_assistant/tools.txt` | Registered all 3 tools for profile loading |
| `profiles/retail_assistant/instructions.txt` | Added retail tool usage guidelines (search first, mention promos, <35 words) |
| `.env` | Added `RETAIL_API_URL=http://localhost:8000`, `RETAIL_API_TIMEOUT=5` |

### Next step: Story 6 — End-to-End Integration Test

### Integration test results (Story 6 — completed):
| Suite | Tests | Result |
|-------|-------|--------|
| Product Search | 10 | ✅ all pass |
| Promo Endpoint | 3 | ✅ all pass |
| Store Info | 5 | ✅ all pass |
| Conversation Flow | 2 | ✅ all pass (full tool chain + L1 cache hit) |
| Error Paths | 5 | ✅ all pass (validation, injection, edge cases) |
| Load Test (50 concurrent) | 1 | ✅ P95 <200ms, zero errors |
| **Total** | **26** | **all pass** |

### Full suite: 63 tests, 0 failures

### 🎉 MVP COMPLETE — All 7 stories done
