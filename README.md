# Retail Assistant

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **retail assistant** with fast product lookup and promotion delivery. Customers query via text (or voice when integrated); the system replies with product locations and active promotions in under one second.

Designed as a foundation for a **Universal Second Brain** — a domain-agnostic classification and memory engine that can be reused across retail, personal productivity, business automation, and research contexts.

> Deployment-agnostic: runs on any machine — cloud, local workstation, edge device. Hardware integration (robot gestures, camera, etc.) is pluggable via the tool system.

---

## Intent

### Problem

Retail customers ask basic "where is X?" and "what is on sale?" questions that pull staff away from higher-value work. Static digital signage cannot answer queries. Robotic alternatives have historically been slow, scripted, or expensive.

### Solution

An always-on kiosk that:

1. Listens for a customer query (voice  text).
2. Classifies intent with a rule-based classifier (MVP) or LLM.
3. Looks up the answer from a warm local cache in <100 ms.
4. Returns the response (with optional TTS / gesture integration).
5. Emits a structured event to the backend for analytics and learning.

### Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Fast-first** | 2-tier cache; LLM only as fallback |
| **Offline-capable** | Full functionality with no network; backend sync is opportunistic |
| **Short responses** | `max_response_words=35` keeps TTS natural |
| **Explainable** | Every response records `intent`, `tool_used`, `cache_hit`, `latency_ms` |
| **Domain-agnostic core** | Backend classification pipeline works for any structured knowledge domain |

---

## Architecture

```

                    Reachy Mini (Pi 5)                      
                                                            
  Microphone  STT  /interact  ProductLookupTool      
                                                           
                                 PromoManagerTool        
                                                           
                                 SelfieTool / Movement   
                                                            
   Tool reads:  L1Cache (RAM)  L2Cache (SQLite FTS5)    
                                                            
   Tool writes: EventEmitter  p Backend (HTTP batch)    
                                                            
  Response  PromptManager  LLMInference  TTS  Speaker  

                            async batch (optional)
                          
          
                p Backend (cloud)    
            /events/batch              receives telemetry
            /cache/sync                pushes product/promo updates
            CanonicalStore (SQLite)  
            KnowledgeGraph           
          
```

### Request Flow

```
Customer query
      
      
_classify_intent()        rule-based keyword match (MVP)
                          returns: product_lookup | promo | selfie
      
InteractionStateMachine   IDLE  LISTEN  PROCESS  RESPOND  IDLE
      
      
tool.execute(query, deps)
        L1 hit?   return immediately
        L1 miss?  search L2 (SQLite FTS5)  cache top result in L1
      
EventEmitter.emit()       async; batched; no-op if p disabled
      
      
InteractionResponse       response text, intent, tool, latency_ms, cache_hit
```

---

## Repository Layout

```
reachy_mini_retail_assistant/

 reachy_edge/              # Edge service — runs anywhere (cloud, local, edge device)
    main.py               # FastAPI app: lifespan, /health, /interact, /cache/sync
    config.py             # Pydantic Settings (env vars / .env)
    models/
       events.py         # EventType enum + event payload schemas
       interaction.py    # InteractionRequest / InteractionResponse
    cache/
       l1_cache.py       # In-memory LRU with TTL + thread-safe locking
       l2_cache.py       # SQLite FTS5 ProductCache + async L2Cache facade
       schemas.py        # Product, Promo, CacheSyncPayload schemas
    fsm/
       interaction_fsm.py  # 4-state FSM: IDLE / LISTEN / PROCESS / RESPOND
    llm/
       inference.py      # LLMInference: OpenAI wrapper (local GGUF planned)
       client.py         # Low-level HTTP helpers
       prompt_manager.py # Prompt templates + word-count enforcement
    tools/
       base.py           # Tool ABC, ToolDependencies dataclass, ToolResult
       product_lookup.py # FTS5 search; L1L2 fallback; emits events
       promo_manager.py  # Active promotions lookup
       movement.py       # Stub: gestures/direction to MovementManager
       selfie.py         # Camera capture engagement feature
    brain_client/
       event_emitter.py  # Async batched HTTP POST to Second Brain backend
    voice/
       stt.py            # Speech-to-text
       tts.py            # Text-to-speech
    data/
       sample_products.py  # 44 truck-stop product definitions
    scripts/
       load_products.py  # CLI: seed SQLite DB from sample data
    tests/
        test_main.py      # Health endpoint, app startup
        test_cache.py     # L1 cache unit tests
        test_l2_cache.py  # FTS5 tests (17 tests, 97% coverage)
        test_tools.py     # Tool integration tests

 backend/                  # Second Brain Cloud Backend
    main.py               # FastAPI: /health, /events/batch, /cache/sync
    config.py             # Backend service settings
    models.py             # BatchEventsRequest / BatchEventsResponse
    db/
       canonical_store.py  # save_event()  SQLite
       knowledge_graph.py  # Entity relationship graph
       vector_store.py     # Embedding storage (stub)
    cache/
        generator.py      # Builds CacheSyncPayload for edge pull

 demo/                     # Standalone Gradio demo (no hardware needed)
    gradio_app.py
    requirements.txt

 docs/                     # Reference documentation
     PRD.md
     UNIVERSAL-ARCHITECTURE.md
     success-metrics.md
```

---

## Key Modules

### `reachy_edge/main.py`  FastAPI Application

Uses FastAPI's `lifespan` context manager for clean init/teardown.

**Startup:** creates L2Cache  L1Cache  EventEmitter  LLMInference  PromptManager  FSM  tools dict. Then preloads L1 from L2 and starts the event emitter background task.

**Endpoints:**

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Service identity (reachy_id, store_id, zone_id) |
| GET | `/health` | Liveness + L1/L2/LLM stats |
| POST | `/interact` | Main customer interaction |
| POST | `/cache/sync` | Receive product/promo updates from backend |

**Rule-based intent classifier:**
```python
# Keywords  intent
"where" / "find" / "looking for" / "location"    product_lookup
"deal"  / "sale" / "promo" / "discount"           promo
"selfie"/ "picture"/ "photo"                      selfie
# fallback                                         product_lookup
```

---

### `reachy_edge/cache/l1_cache.py`  In-Memory LRU Cache

Thread-safe dict with per-entry TTL and LRU eviction via `threading.Lock`.

- **`get(key)`**  returns `None` on miss or expiry; updates `last_access`.
- **`set(key, value)`**  evicts LRU entry when at `max_size`.
- **`invalidate(key=None)`** → clears one key or entire cache (called after backend sync).
- **`stats()`**  returns `{size, max_size, hits, misses, hit_rate_pct}`.

Defaults: `max_size=1000`, `ttl_seconds=300`.

---

### `reachy_edge/cache/l2_cache.py`  SQLite FTS5 Persistent Cache

`ProductCache` wraps a SQLite FTS5 virtual table:

```sql
CREATE VIRTUAL TABLE products_fts USING fts5(
    sku, name, category, location,
    price UNINDEXED,          -- not searched
    description,
    tokenize='porter unicode61'   -- stemming + Unicode
);
```

Searches use BM25 ranking via FTS5's built-in `rank` column.

`L2Cache` is an async facade used by the app:
- `search_products(query, max_results)`  FTS5 MATCH + BM25 sort.
- `preload_hot_data(l1_cache)`  warms L1 on boot.
- `update_products(products)` / `update_promos(promos)`  applied on sync.
- `stats()`  exposes counts and cache version for `/health`.

---

### `reachy_edge/fsm/interaction_fsm.py`  Interaction State Machine

```
IDLE begin() LISTEN processing() PROCESS responding() RESPOND
                                                                        
  reset() 
```

FSM state appears in every `InteractionResponse.metadata.state` for debugging.

---

### `reachy_edge/tools/`  Tool System

All tools inherit from `Tool` (ABC in `base.py`) and receive `ToolDependencies`:

```python
@dataclass
class ToolDependencies:
    l1_cache: L1Cache
    l2_cache: L2Cache
    event_emitter: EventEmitter
    movement_manager: Any | None   # None until Epic 2 hardware SDK integration
    reachy_id: str
    store_id: str
    zone_id: str
```

**`ProductLookupTool`**
1. L1 hit  return immediately.
2. L1 miss  `l2_cache.search_products()`  cache top result in L1.
3. Exact SKU matches sorted first regardless of BM25 score.
4. Emits `CACHE_HIT` or `PRODUCT_QUERY` event.

**`MovementTool`**  Stub: logs gesture/direction. Will delegate to hardware SDK in Epic 2.

**`SelfieTool`**  Camera capture for engagement photos.

---

### `reachy_edge/llm/inference.py`  LLM Integration

`LLMInference` supports two modes (configured via `Settings.llm_mode`):

| Mode | Backend |
|------|---------|
| `"openai"` | `openai.OpenAI`  `gpt-4.1-mini` by default |
| `"local"` | TODO  llama.cpp / GGUF planned |

`PromptManager` caps system prompts to `max_response_words=35` for short TTS output.

Latency exceeding `timeout_s` logs a warning but does **not** abort  the caller decides whether to use a cached fallback.

---

### `reachy_edge/brain_client/event_emitter.py` — Async Event Pipeline

Background `worker()` coroutine drains an `asyncio.Queue`:

- Batches up to `batch_size` events (default 50) or `batch_interval_s` seconds (default 5).
- POSTs to `{backend_url}/events/batch` with `x-api-key` header.
- `backend_enabled=False` (default in development) is a zero-overhead no-op.
- `flush()` called on shutdown drains any remaining events.
- `stats()` reports `events_sent` / `events_failed` to `/health`.

---

### `backend/main.py` — Second Brain Cloud Service

Three endpoints:

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Liveness check |
| `POST /events/batch` | Persists each event to `CanonicalStore` (SQLite) |
| `GET /cache/sync` | Returns `CacheSyncPayload` (products + promos) for edge |

`KnowledgeGraph` and `vector_store` are stubs for Epic 3.

---

## Quick Start

```bash
cd reachy_edge
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

# Seed the SQLite product database (44 truck-stop products)
python scripts/load_products.py

# Start the edge server
uvicorn reachy_edge.main:app --reload
```

Verify:
```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/interact \
  -H "Content-Type: application/json" \
  -d '{"query":"where is the diesel?","session_id":"test-1"}'
```

### Tests

```bash
python -m pytest tests/ -v
```

Coverage: health endpoint, L1 cache, L2 FTS5 (97%), tool integration.

---

## Configuration Reference

Settings live in `reachy_edge/config.py` and are read from environment variables or `.env`.

| Variable | Default | Description |
|----------|---------|-------------|
| `REACHY_ID` | `RCH-DEV-001` | Instance identifier |
| `STORE_ID` | `STORE-DEV` | Store identifier |
| `ZONE_ID` | `ENTRANCE` | Zone within store |
| `LLM_MODE` | `openai` | `openai` or `local` |
| `OPENAI_API_KEY` | *(none)* | Required when `LLM_MODE=openai` |
| `INFERENCE_MODEL` | `gpt-4.1-mini` | Chat completion model |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model (Epic 3) |
| `L2_BACKEND` | `sqlite` | `sqlite` or `qdrant` (Qdrant: Epic 3) |
| `L2_DB_PATH` | `./data/cache.db` | SQLite file path |
| `L1_TTL_SECONDS` | `300` | L1 entry lifetime in seconds |
| `L1_MAX_SIZE` | `1000` | Max number of L1 entries |
| `MAX_RESPONSE_WORDS` | `35` | Caps TTS response length |
| `TIMEOUT_S` | `1.0` | LLM latency warning threshold |
| `BACKEND_ENABLED` | `false` | Enable Second Brain backend emission |
| `BACKEND_URL` | `https://brain.example.com` | Second Brain backend base URL |
| `EVENT_BATCH_SIZE` | `50` | Events per HTTP POST to backend |
| `EVENT_BATCH_INTERVAL_S` | `5` | Max seconds between flushes |

---

## Development Status

| Epic | Focus | Status |
|------|-------|--------|
| **Epic 1  Core Edge Engine** | FastAPI + 2-tier cache + tool skeleton |  In Progress |
| Epic 2  Human Interface | STT/TTS + robot gesture SDK integration |  Planned |
| Epic 3  Second Brain Intelligence Layer | Classification pipeline + embeddings + Qdrant |  Planned |
| Epic 4  Integration & Deployment | Sync protocol + monitoring + deploy |  Planned |
| Epic 5  Enhancement & Scale | Analytics + multi-store + domain plugins |  Planned |

**Non-Functional Requirements:**

| NFR | Target | Notes |
|-----|--------|-------|
| End-to-end voice response | < 2 s | Epic 2 |
| LLM response | < 500 ms | |
| L2 cache search | < 100 ms | FTS5 BM25; target met in tests |
| L1 cache lookup | < 10 ms | In-memory |
| L1 cache hit rate |  99.9% | After warm-up |
| Edge uptime |  99.5% | Epic 4 |

---

## Sample Product Dataset (Truck Stop)

44 products across 8 categories in `reachy_edge/data/sample_products.py`, loaded with `scripts/load_products.py`:

| Category | Examples |
|----------|---------|
| Fuel & Fluids | Premium Diesel, BlueDEF, Shell Rotella |
| Trucker Supplies | Logbooks, load straps, bungee cords, mud flaps |
| Electronics | Cobra CB radio, Garmin GPS, dash cam |
| Energy & Snacks | Coffee, energy drinks, beef jerky |
| Hot Food | Pizza, burgers, chicken tenders |
| Services | Shower credits, truck wash, reserved parking |
| Safety & Lighting | LED flares, safety vests, emergency kit |
| Convenience | Sunglasses, OTC meds, hygiene products |

---

## Documentation

| File | Content |
|------|---------|
| [docs/PRD.md](docs/PRD.md) | Full product vision, goals, non-goals |
| [docs/UNIVERSAL-ARCHITECTURE.md](docs/UNIVERSAL-ARCHITECTURE.md) | System design, multi-domain vision |
| [docs/success-metrics.md](docs/success-metrics.md) | KPIs and measurement approach |
| [_bmad-output/planning-artifacts/epics.md](_bmad-output/planning-artifacts/epics.md) | 5 epics, 39 stories with acceptance criteria |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Web framework | FastAPI 0.109+ / Pydantic v2 |
| Persistent search | SQLite FTS5 (BM25, Porter stemming) |
| In-memory cache | Python dict + `threading.Lock` |
| LLM | OpenAI `gpt-4.1-mini` / local GGUF (planned) |
| Embeddings | `text-embedding-3-small` (Epic 3) |
| Vector store | Qdrant (Epic 3); SQLite FTS5 for MVP |
| Logging | structlog  JSON, ISO timestamps |
| Settings | pydantic-settings  env vars + `.env` |
| Testing | pytest + pytest-asyncio |
| Robot SDK | Pluggable hardware integration (Epic 2) |

---

## License

MIT  see [LICENSE](LICENSE).
