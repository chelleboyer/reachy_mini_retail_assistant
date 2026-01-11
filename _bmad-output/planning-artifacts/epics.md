---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics]
inputDocuments:
  - docs/PRD.md
  - docs/UNIVERSAL-ARCHITECTURE.md
  - docs/deployment-architecture..md
---

# π Universal Second Brain - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for π Universal Second Brain, decomposing the requirements from the PRD and Architecture into implementable stories. Initial implementation focuses on Phase 1: Retail MVP with Reachy Mini robot.

## Requirements Inventory

### Functional Requirements (FRs)

**Universal π Platform:**

FR1: Multi-stage classification pipeline (Domain → Intent → Entity → Canonical → Response)
FR2: Universal canonical storage (entities, events, knowledge, tasks, content)
FR3: Domain plugin system with YAML-based configurations
FR4: Context and reasoning engine with session tracking
FR5: Cache generation engine with domain-filtered snapshots
FR6: Event ingestion API for all edge devices
FR7: Classification explainability with confidence scoring
FR8: Entity deduplication and resolution
FR9: Knowledge graph with relationships
FR10: Evaluation and replay system for classifier testing
FR11: External data feed ingestion and normalization
FR12: Multi-tenant support with isolation

**Retail Edge (Reachy Mini):**

FR13: Voice input and output (STT/TTS)
FR14: Natural language conversation with ≤35 word responses
FR15: Gesture coordination (head, arm pointing)
FR16: Single-question clarification support
FR17: L1 cache (RAM, hot, ≤1MB) for active promos and frequent products
FR18: L2 cache (SQLite FTS5, ≤100MB) for all products, promos, store config
FR19: Product lookup tool (by SKU or name → location)
FR20: Promo manager tool (active deals query)
FR21: Selfie coordination tool (optional engagement)
FR22: Movement/gesture tool (point, wave, nod)
FR23: Fast LLM integration with cache-only prompts
FR24: Async event emission to π backend
FR25: Cache sync protocol with incremental updates
FR26: Health and observability endpoints

**User Flows (Retail):**

FR27: Deal promotion flow (greet + share 1-3 promos + offer location)
FR28: Wayfinding flow (query → cache lookup → gesture + directions)
FR29: Clarification flow (detect ambiguity → ask once → answer or fallback)
FR30: Selfie flow (offer → pose → countdown → capture, no storage)

### Non-Functional Requirements (NFRs)

**Performance:**

NFR1: P95 interaction latency <1s (retail edge full interaction)
NFR2: Fast path responses <500ms (cache-only queries)
NFR3: L1 cache hit <10ms
NFR4: L2 cache query <100ms
NFR5: π classification <200ms for cached patterns
NFR6: Cache sync latency <5s
NFR7: Knowledge graph query <100ms
NFR8: Sub-100ms classification for cached patterns

**Reliability:**

NFR9: ≥99% crash-free interactions
NFR10: <1% unhandled errors
NFR11: Zero data corruption events
NFR12: System uptime ≥99.5%
NFR13: Must degrade gracefully under network issues
NFR14: Must support offline cache usage

**Quality & Accuracy:**

NFR15: ≥95% domain detection accuracy
NFR16: ≥90% intent classification accuracy
NFR17: ≥85% entity extraction F1 score
NFR18: <2% ambiguous classifications requiring clarification
NFR19: Cache hit rate ≥90% for product queries

**Usability (Retail):**

NFR20: ≥30% customer wayfinding engagement
NFR21: ≥60% promo information recall
NFR22: ≥80% of queries answered without escalation
NFR23: 10-20% selfie acceptance rate
NFR24: Observable social engagement (positive body language)

**Security & Privacy:**

NFR25: No PII storage in retail MVP
NFR26: No image storage (privacy)
NFR27: Append-only event logs
NFR28: Must be auditable with full trace logging
NFR29: Multi-tenant isolation (store/user)

**Scalability:**

NFR30: Design for horizontal scaling from day 1
NFR31: Support multiple edge devices per π instance
NFR32: Efficient domain-filtered cache generation

**Code Quality (CRITICAL):**

NFR33: Exceptional code quality - production-grade, not prototype
NFR34: Comprehensive type hints (Python 3.11+)
NFR35: Full docstrings for all public APIs
NFR36: Clean architecture with clear separation of concerns
NFR37: SOLID principles throughout
NFR38: Comprehensive error handling (no silent failures)
NFR39: Unit test coverage ≥80% for core logic
NFR40: Integration tests for all API endpoints
NFR41: Idiomatic code following language best practices
NFR42: No code smells (duplications, god objects, etc.)
NFR43: Proper logging (structured, leveled, contextual)
NFR44: Security best practices (input validation, sanitization)
NFR45: Performance optimizations where critical
NFR46: Code reviews required for all changes
NFR47: CI/CD pipeline with quality gates

### Additional Requirements

**From Architecture:**

- **Technology Stack:**
  - π Backend: FastAPI for REST API
  - Edge Backend: FastAPI on Pi 5
  - Storage: SQLite (edge/local), PostgreSQL (cloud/production)
  - Cache: In-memory LRU (L1) + SQLite FTS5 (L2)
  - LLM: OpenAI API (initial), Llama 3.2 3B (planned)
  - Demo UI: Gradio for Hugging Face Spaces

- **Deployment Models:**
  - Cloud deployment: Hugging Face Spaces (demo/SaaS)
  - Edge deployment: Pi 5 local (privacy/offline)
  - Hybrid deployment: Local + cloud sync (planned Phase 2)

- **Domain Plugin Structure:**
  - YAML configuration files per domain
  - Intent definitions with examples
  - Entity schemas with fields
  - Canonical type mappings
  - Tool registry per domain

- **Infrastructure:**
  - π event ingestion API endpoint
  - Edge /interact, /cache/sync, /health endpoints
  - Async event emitter with batching
  - WebSocket support (planned Phase 2)

- **Observability:**
  - Structured logging with trace IDs
  - Latency metrics (P50/P95/P99)
  - Cache hit/miss tracking
  - Classification confidence tracking
  - Prompt versioning
  - Debug mode (logs cache slices, LLM I/O, classifier decisions)

**From Current Implementation:**

- Active code exists: `reachy_edge/` (Pi 5 backend) and `pi_space/` (demo UI)
- Edge backend already running on http://127.0.0.1:8000
- Demo UI ready for Hugging Face deployment
- Basic keyword-based classifier implemented (needs LLM upgrade)

**Phase 1 Scope:**

- Focus: Retail domain only
- Exclude: Personalization, checkout, facial recognition, autonomous learning
- MVP: Prove second brain architecture works
- Demo-ready for investors/customers

### FR Coverage Map

**Epic 1 - Core Edge Engine:**
- FR17: L1 cache (RAM, hot, ≤1MB) for active promos and frequent products
- FR18: L2 cache (SQLite FTS5, ≤100MB) for all products, promos, store config
- FR19: Product lookup tool (by SKU or name → location)
- FR26: Health and observability endpoints

**Epic 2 - Human Interface Layer:**
- FR13: Voice input and output (STT/TTS)
- FR14: Natural language conversation with ≤35 word responses
- FR15: Gesture coordination (head, arm pointing)
- FR16: Single-question clarification support
- FR20: Promo manager tool (active deals query)
- FR21: Selfie coordination tool (optional engagement)
- FR22: Movement/gesture tool (point, wave, nod)
- FR23: Fast LLM integration with cache-only prompts
- FR27: Deal promotion flow (greet + share 1-3 promos + offer location)
- FR28: Wayfinding flow (query → cache lookup → gesture + directions)
- FR29: Clarification flow (detect ambiguity → ask once → answer or fallback)
- FR30: Selfie flow (offer → pose → countdown → capture, no storage)

**Epic 3 - π Intelligence Layer:**
- FR1: Multi-stage classification pipeline (Domain → Intent → Entity → Canonical → Response)
- FR2: Universal canonical storage (entities, events, knowledge, tasks, content)
- FR3: Domain plugin system with YAML-based configurations
- FR4: Context and reasoning engine with session tracking
- FR7: Classification explainability with confidence scoring
- FR8: Entity deduplication and resolution
- FR9: Knowledge graph with relationships
- FR10: Evaluation and replay system for classifier testing
- FR11: External data feed ingestion and normalization
- FR24: Async event emission to π backend

**Epic 4 - Edge-π Sync:**
- FR5: Cache generation engine with domain-filtered snapshots
- FR6: Event ingestion API for all edge devices
- FR12: Multi-tenant support with isolation
- FR25: Cache sync protocol with incremental updates

**Epic 5 - Production Readiness:**
- All NFRs (NFR1-NFR47): Performance, reliability, quality, usability, security, scalability, code quality

## Epic List

### Epic 1: Core Edge Engine - Minimal Viable Edge
Store customers can query product locations through a REST API with fast, accurate responses from cached data.

**User Outcome:** Prove the edge architecture works with HTTP + JSON. Testable with curl/Postman before adding complexity.

**FRs covered:** FR17, FR18, FR19, FR26 (4 FRs)

**Implementation Notes:**
- FastAPI backend on Pi 5
- SQLite FTS5 for product search (L2)
- In-memory LRU cache for hot data (L1)
- REST endpoint: POST /interact (query → product location)
- GET /health (system stats)
- JSON request/response (no voice, no LLM yet)
- 100% testable via HTTP clients
- Standalone functionality

**Why First:** Smallest possible edge that delivers value. Proves architecture before adding human interface complexity.

---

### Epic 2: Human Interface Layer - Voice + Personality
Reachy robot can have natural voice conversations with customers, using gestures and LLM-powered responses for engaging retail assistance.

**User Outcome:** Customers interact naturally with Reachy through voice, getting helpful responses with personality and physical engagement.

**FRs covered:** FR13, FR14, FR15, FR16, FR20, FR21, FR22, FR23, FR27, FR28, FR29, FR30 (12 FRs)

**Implementation Notes:**
- Voice I/O (STT/TTS integration)
- Natural language processing (≤35 word responses)
- Gesture coordination (head, arm pointing)
- FSM for interaction flows (greeting, wayfinding, clarification, selfie)
- LLM integration (OpenAI API initially)
- Strict prompt contracts (cache-only)
- Promo manager tool
- Movement/gesture tool
- Builds on Epic 1's foundation

**Why Second:** Adds the human layer to working API. Each piece (voice, gestures, LLM, flows) can be implemented and tested incrementally.

---

### Epic 3: π Intelligence Layer - Classification + Memory
π backend classifies any interaction into structured knowledge, builds knowledge graphs, and continuously learns from all edge devices.

**User Outcome:** π transforms unstructured conversations into searchable knowledge, enabling context-aware responses and cross-domain reasoning.

**FRs covered:** FR1, FR2, FR3, FR4, FR7, FR8, FR9, FR10, FR11, FR24 (10 FRs)

**Implementation Notes:**
- FastAPI backend for π
- Multi-stage classification pipeline (5 stages)
- Universal canonical storage (entities, events, knowledge, tasks, content)
- SQLite for development, PostgreSQL for production
- YAML-based domain plugin system (retail domain first)
- Context and reasoning engine (session tracking, entity resolution)
- Knowledge graph implementation
- Confidence scoring and explainability
- Event replay system for evaluation
- External feed adapters (price feeds, promos)
- Event ingestion from edge devices
- Standalone π service (edge works without π initially)

**Why Third:** Core intelligence. Classification needs memory context, memory needs classification to populate. They're one cohesive system, not two separate pieces.

---

### Epic 4: Edge-π Sync - Distributed Architecture
π generates optimized caches for edge devices and syncs incrementally, supporting multiple stores/devices from one π instance.

**User Outcome:** Edge devices stay fast with local cache while π continuously learns and improves classification across all interactions.

**FRs covered:** FR5, FR6, FR12, FR25 (4 FRs)

**Implementation Notes:**
- Cache generation pipeline (domain-filtered snapshots)
- Incremental sync protocol (only changed data)
- Multi-tenant architecture (store/user isolation)
- Event ingestion endpoints (async, batched)
- Cache versioning and rollback
- Connects Epic 1-2 (edge) with Epic 3 (π)

**Why Fourth:** Completes the second brain architecture. Edge runs fast locally, π learns globally.

---

### Epic 5: Production Readiness - Quality & Observability
System meets all performance, reliability, and quality standards with full observability for debugging and optimization.

**User Outcome:** Production-grade system with exceptional code quality, comprehensive testing, and full visibility into system behavior.

**FRs covered:** All NFRs (NFR1-NFR47)

**Implementation Notes:**
- Comprehensive testing (unit ≥80%, integration, load)
- Full type hints (Python 3.11+) and docstrings
- Clean architecture + SOLID principles
- Structured logging with trace IDs
- Metrics collection (Prometheus/Grafana)
- Performance profiling and optimization
- Security hardening (input validation, sanitization)
- CI/CD pipeline with quality gates
- Error handling (no silent failures)
- Code reviews and quality standards
- Applies to all previous epics

**Why Last:** Quality and observability woven throughout, but final epic ensures everything meets production standards before launch.

---

## Stories

### Epic 1: Core Edge Engine - Minimal Viable Edge

#### Story 1.1: FastAPI Project Setup with Basic Health Endpoint

**As a** developer  
**I want** a FastAPI project with proper structure and a health endpoint  
**So that** we have a solid foundation and can verify the service is running

**Acceptance Criteria:**

**Given** I am setting up the retail edge backend  
**When** I initialize the FastAPI project  
**Then** the following structure exists:
- `reachy_edge/main.py` with FastAPI app instance
- `reachy_edge/config.py` with environment-based configuration
- `reachy_edge/models.py` with Pydantic models
- `reachy_edge/requirements.txt` with dependencies (fastapi, uvicorn, sqlite3, pydantic)
- `reachy_edge/README.md` with setup instructions

**Given** the FastAPI app is running on localhost:8000  
**When** I call GET /health  
**Then** I receive a 200 response with JSON:
```json
{
  "status": "healthy",
  "timestamp": "<ISO 8601>",
  "version": "0.1.0"
}
```

**Given** the health endpoint implementation  
**When** I review the code  
**Then** it includes:
- Type hints on all functions
- Docstrings for the health endpoint
- Structured logging (INFO level)
- Clean, idiomatic Python 3.11+

**Definition of Done:**
- [ ] Project structure created with all required files
- [ ] FastAPI app starts successfully
- [ ] GET /health returns 200 with correct JSON schema
- [ ] Code follows NFR33-NFR47 (type hints, docstrings, clean code)
- [ ] README has clear setup and run instructions
- [ ] Committed to version control

**FR Coverage:** FR26 (basic health endpoint)  
**Estimated Effort:** 2-4 hours

---

#### Story 1.2: L2 Cache - SQLite FTS5 Product Storage

**As a** retail edge backend  
**I want** a SQLite FTS5-indexed product database  
**So that** I can quickly search products by name, SKU, or category

**Acceptance Criteria:**

**Given** I am implementing persistent product storage  
**When** I create the database module  
**Then** the following exists:
- `reachy_edge/db/products.py` with FTS5 setup
- SQLite database with `products_fts` virtual table
- Schema: `sku TEXT, name TEXT, category TEXT, location TEXT, price REAL, description TEXT`
- FTS5 index on: name, category, description

**Given** the database is initialized  
**When** I load sample product data (20-50 products)  
**Then** the products are inserted successfully  
**And** I can query using FTS5 syntax (`SELECT * FROM products_fts WHERE products_fts MATCH 'query'`)

**Given** a product search query "organic apple"  
**When** I execute FTS5 search  
**Then** results are returned in <100ms (NFR4)  
**And** results are ranked by BM25 relevance  
**And** each result includes: sku, name, location, price

**Given** the database module code  
**When** I review implementation  
**Then** it includes:
- Full type hints and docstrings
- Proper connection management (context managers)
- SQL injection protection (parameterized queries)
- Error handling for all database operations
- Database file stored in `data/products.db`

**Definition of Done:**
- [ ] SQLite FTS5 database created with proper schema
- [ ] Sample product data loaded (20-50 products)
- [ ] Search queries return results <100ms
- [ ] Unit tests for database operations (≥80% coverage)
- [ ] Code meets quality standards (NFR33-NFR47)
- [ ] Documentation in docstrings and README

**FR Coverage:** FR18 (L2 cache with FTS5)  
**Estimated Effort:** 4-6 hours

---

#### Story 1.3: Product Lookup Tool with FTS5 Search

**As a** retail edge service  
**I want** a product lookup function that searches the FTS5 cache  
**So that** I can find products by name, SKU, or description

**Acceptance Criteria:**

**Given** I am implementing the product lookup tool  
**When** I create the tool module  
**Then** the following exists:
- `reachy_edge/tools/product_lookup.py` with `lookup_product()` function
- Function signature: `lookup_product(query: str, max_results: int = 5) -> list[Product]`
- Product model with fields: sku, name, category, location, price, relevance_score

**Given** a query "organic apple"  
**When** I call `lookup_product("organic apple")`  
**Then** it returns ranked results from FTS5  
**And** results include relevance scores  
**And** query completes in <100ms (NFR4)

**Given** a query with no matches "xyzabc123"  
**When** I call `lookup_product("xyzabc123")`  
**Then** it returns an empty list  
**And** no exceptions are raised

**Given** a SKU-based query "SKU-12345"  
**When** I call `lookup_product("SKU-12345")`  
**Then** it returns the exact product match first  
**And** other results (if any) are ranked by relevance

**Given** the product lookup code  
**When** I review implementation  
**Then** it includes:
- Full type hints with Pydantic models
- Comprehensive docstrings
- Error handling (malformed queries, database errors)
- Logging (query, result count, latency)
- Unit tests with mocked database

**Definition of Done:**
- [ ] `lookup_product()` function implemented
- [ ] Returns ranked results from FTS5 in <100ms
- [ ] Handles edge cases (no results, exact SKU match)
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with real database
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR19 (Product lookup tool)  
**Estimated Effort:** 3-5 hours

---

#### Story 1.4: L1 Cache - In-Memory LRU for Hot Products

**As a** retail edge service  
**I want** an in-memory LRU cache for frequently accessed products  
**So that** hot queries return in <10ms without hitting the database

**Acceptance Criteria:**

**Given** I am implementing the L1 cache  
**When** I create the cache module  
**Then** the following exists:
- `reachy_edge/cache/lru_cache.py` with `ProductCache` class
- Uses Python's `functools.lru_cache` or custom LRU implementation
- Max size: 100 entries (~1MB as per FR17)
- TTL: 300 seconds (5 minutes)

**Given** a product query "apple"  
**When** I query for the first time  
**Then** it hits L2 (SQLite FTS5)  
**And** result is cached in L1  
**And** query takes ~100ms

**Given** the same query "apple" is repeated  
**When** I query within TTL  
**Then** it hits L1 cache  
**And** query takes <10ms (NFR3)  
**And** L2 is not accessed

**Given** the cache reaches max size (100 entries)  
**When** a new query arrives  
**Then** the least recently used entry is evicted  
**And** new result is cached

**Given** cache statistics tracking  
**When** I access cache stats  
**Then** it reports: total_requests, l1_hits, l1_misses, hit_rate, evictions

**Given** the cache code  
**When** I review implementation  
**Then** it includes:
- Type hints and docstrings
- Thread-safe operations (if multi-threaded)
- Cache metrics tracking
- TTL enforcement
- Unit tests with time mocking

**Definition of Done:**
- [ ] LRU cache implemented with max size 100
- [ ] Cache hits return in <10ms
- [ ] TTL enforcement (5 minutes)
- [ ] Statistics tracking (hits, misses, evictions)
- [ ] Unit tests ≥80% coverage
- [ ] Integration test showing L1→L2 fallback
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR17 (L1 cache)  
**Estimated Effort:** 4-6 hours

---

#### Story 1.5: /interact Endpoint for Product Queries

**As a** customer (via HTTP client)  
**I want** to query product locations through POST /interact  
**So that** I can get fast, accurate product information

**Acceptance Criteria:**

**Given** I am implementing the /interact endpoint  
**When** I create the route  
**Then** it exists at POST /interact  
**And** accepts JSON: `{"query": "where are the apples?"}`  
**And** returns JSON: `{"response": "Apples are in Aisle 3, Produce Section", "products": [...], "latency_ms": 45}`

**Given** a product query "where are organic apples"  
**When** I POST to /interact  
**Then** it:
1. Checks L1 cache first
2. Falls back to L2 (FTS5) on cache miss
3. Caches result in L1
4. Returns response in <500ms for cache-only queries (NFR2)

**Given** a query with multiple matching products  
**When** I POST to /interact  
**Then** the response includes:
- Top 3 products ranked by relevance
- Each product: sku, name, location, price
- Total latency in milliseconds

**Given** a query with no results "xyzabc"  
**When** I POST to /interact  
**Then** it returns 200 with: `{"response": "I couldn't find any products matching that query.", "products": []}`

**Given** an invalid request (missing "query" field)  
**When** I POST to /interact  
**Then** it returns 422 with validation error details

**Given** the endpoint implementation  
**When** I review the code  
**Then** it includes:
- Pydantic request/response models
- Full type hints and docstrings
- Structured logging (query, result count, latency, cache hit/miss)
- Error handling (database errors, timeouts)
- Request ID generation for tracing

**Definition of Done:**
- [ ] POST /interact endpoint implemented
- [ ] Uses L1→L2 cache hierarchy
- [ ] Returns responses in <500ms (NFR2)
- [ ] Handles edge cases (no results, invalid input)
- [ ] Integration tests for all scenarios
- [ ] Logging with structured data
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR19 (Product lookup via API)  
**Estimated Effort:** 4-6 hours

---

#### Story 1.6: Enhanced Health Endpoint with Cache Stats

**As a** system operator  
**I want** detailed health metrics including cache statistics  
**So that** I can monitor system performance and diagnose issues

**Acceptance Criteria:**

**Given** the health endpoint is implemented  
**When** I call GET /health  
**Then** it returns comprehensive stats:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-10T12:34:56Z",
  "version": "0.1.0",
  "uptime_seconds": 3600,
  "cache": {
    "l1_size": 45,
    "l1_max_size": 100,
    "l1_hit_rate": 0.89,
    "l1_hits": 890,
    "l1_misses": 110,
    "l2_query_count": 110
  },
  "database": {
    "product_count": 42,
    "connection_status": "healthy"
  }
}
```

**Given** the database is unreachable  
**When** I call GET /health  
**Then** it returns 503 with: `{"status": "unhealthy", "database": {"connection_status": "error", "error": "..."}}`

**Given** cache hit rate is <90% (below NFR19 threshold)  
**When** I call GET /health  
**Then** the response includes warning: `{"warnings": ["Cache hit rate below target (89% < 90%)"]}`

**Given** the health endpoint code  
**When** I review implementation  
**Then** it includes:
- Non-blocking health checks (timeouts)
- Comprehensive error handling
- Structured logging on health check failures
- Type hints and docstrings

**Definition of Done:**
- [ ] Enhanced /health endpoint with full stats
- [ ] Returns 200 (healthy) or 503 (unhealthy)
- [ ] Includes cache, database, and system metrics
- [ ] Warnings for degraded performance
- [ ] Unit and integration tests
- [ ] Code meets quality standards (NFR33-NFR47)
- [ ] Documentation updated

**FR Coverage:** FR26 (Health and observability)  
**Estimated Effort:** 3-4 hours

---

**Epic 1 Total Estimated Effort:** 20-31 hours  
**Epic 1 Total FRs Covered:** 4 (FR17, FR18, FR19, FR26)

---

### Epic 2: Human Interface Layer - Voice + Personality

#### Story 2.1: Voice Input Integration (STT)

**As a** customer  
**I want** to speak to Reachy naturally  
**So that** I can ask questions without using keyboards or screens

**Acceptance Criteria:**

**Given** I am implementing voice input  
**When** I create the STT module  
**Then** the following exists:
- `reachy_edge/voice/stt.py` with `SpeechToText` class
- Integration with speech recognition service (e.g., Google Speech API, Whisper)
- Configurable via environment variables (API keys, model selection)

**Given** a customer speaks "where are the apples"  
**When** the audio is captured and processed  
**Then** it returns transcribed text: "where are the apples"  
**And** transcription completes in <2 seconds

**Given** background noise or unclear speech  
**When** audio is processed  
**Then** confidence score is returned with transcription  
**And** low confidence (<0.6) triggers clarification flow (FR16)

**Given** audio capture fails (no microphone, permissions)  
**When** STT is invoked  
**Then** it raises descriptive exception  
**And** error is logged with context

**Given** the STT code  
**When** I review implementation  
**Then** it includes:
- Full type hints and docstrings
- Async/await for non-blocking audio processing
- Retry logic for transient API failures
- Audio format validation
- Unit tests with mocked audio/API

**Definition of Done:**
- [ ] STT module implemented with configurable service
- [ ] Transcribes speech in <2 seconds
- [ ] Returns confidence scores
- [ ] Error handling for all failure modes
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with real audio samples
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR13 (Voice input)  
**Estimated Effort:** 6-8 hours

---

#### Story 2.2: Voice Output Integration (TTS)

**As a** Reachy robot  
**I want** to speak responses naturally  
**So that** customers receive information in a friendly, human-like way

**Acceptance Criteria:**

**Given** I am implementing voice output  
**When** I create the TTS module  
**Then** the following exists:
- `reachy_edge/voice/tts.py` with `TextToSpeech` class
- Integration with TTS service (e.g., Google TTS, ElevenLabs, pyttsx3)
- Configurable voice parameters (pitch, speed, voice model)

**Given** a response text "Apples are in Aisle 3"  
**When** TTS is invoked  
**Then** it generates audio output  
**And** audio plays through speakers  
**And** generation + playback starts in <1 second

**Given** a long response (>35 words, violates FR14)  
**When** TTS is invoked  
**Then** it truncates or raises warning  
**And** logs the violation

**Given** TTS service is unavailable  
**When** TTS is invoked  
**Then** it falls back to text display (if available)  
**Or** raises exception with clear error message

**Given** the TTS code  
**When** I review implementation  
**Then** it includes:
- Full type hints and docstrings
- Async/await for non-blocking audio generation
- Audio caching for common phrases
- Volume and speed controls
- Unit tests with mocked TTS service

**Definition of Done:**
- [ ] TTS module implemented with configurable voice
- [ ] Generates and plays audio in <1 second
- [ ] Handles long responses appropriately
- [ ] Error handling and fallback mechanisms
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with real TTS service
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR13 (Voice output)  
**Estimated Effort:** 6-8 hours

---

#### Story 2.3: Gesture Control System

**As a** Reachy robot  
**I want** to coordinate head and arm movements  
**So that** I can point to locations and express engagement through body language

**Acceptance Criteria:**

**Given** I am implementing gesture control  
**When** I create the gesture module  
**Then** the following exists:
- `reachy_edge/gestures/controller.py` with `GestureController` class
- Support for gestures: point (arm), wave (arm), nod (head), look (head)
- Integration with Reachy SDK for motor control

**Given** a direction "Aisle 3, left side"  
**When** I call `gesture_controller.point(direction="left")`  
**Then** Reachy's arm extends and points left  
**And** head turns toward the direction  
**And** gesture completes in <2 seconds

**Given** a greeting interaction  
**When** I call `gesture_controller.wave()`  
**Then** Reachy waves with arm  
**And** gesture is smooth and natural

**Given** an affirmative response  
**When** I call `gesture_controller.nod()`  
**Then** Reachy's head nods once  
**And** motion is subtle and human-like

**Given** multiple gestures queued  
**When** gestures are executed  
**Then** they run sequentially without overlap  
**And** queue is non-blocking (async)

**Given** motor control fails (hardware issue)  
**When** gesture is invoked  
**Then** exception is raised with diagnostic info  
**And** error is logged with motor state

**Given** the gesture code  
**When** I review implementation  
**Then** it includes:
- Full type hints and docstrings
- Async/await for non-blocking execution
- Gesture queue management
- Safety limits (range of motion)
- Unit tests with mocked Reachy SDK

**Definition of Done:**
- [ ] GestureController with 4+ gestures (point, wave, nod, look)
- [ ] Gestures execute smoothly in <2 seconds
- [ ] Queue management for sequential execution
- [ ] Error handling for hardware failures
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with real/simulated Reachy
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR15 (Gesture coordination), FR22 (Movement/gesture tool)  
**Estimated Effort:** 8-10 hours

---

#### Story 2.4: LLM Integration with Cache-Only Prompts

**As a** retail edge service  
**I want** to generate natural language responses using LLM with strict cache-only prompts  
**So that** responses are helpful, personable, and stay within cached knowledge

**Acceptance Criteria:**

**Given** I am implementing LLM integration  
**When** I create the LLM module  
**Then** the following exists:
- `reachy_edge/llm/client.py` with `LLMClient` class
- Integration with OpenAI API (configurable model: gpt-4o-mini initially)
- System prompt enforces cache-only responses
- Max tokens: 150 (ensures ≤35 words per FR14)

**Given** a product query result [Product("Apples", "Aisle 3")]  
**When** I call `llm_client.generate_response(query="where are apples", products=[...])`  
**Then** it returns: "Apples are in Aisle 3 in the Produce section. Would you like directions?"  
**And** response is ≤35 words (FR14)  
**And** response generation takes <500ms (NFR2 total)

**Given** a system prompt template  
**When** I review the prompt  
**Then** it includes:
- "You are Reachy, a helpful retail assistant"
- "Only use information from the provided product cache"
- "Never make up product locations or prices"
- "Keep responses under 35 words"
- "Be friendly and conversational"

**Given** the LLM API is unavailable  
**When** response generation is attempted  
**Then** it falls back to template-based response  
**And** degradation is logged

**Given** LLM response exceeds 35 words  
**When** response is generated  
**Then** it is truncated at sentence boundary  
**And** warning is logged

**Given** the LLM code  
**When** I review implementation  
**Then** it includes:
- Full type hints and docstrings
- Async/await for non-blocking API calls
- Retry logic with exponential backoff
- Response caching for identical queries
- Token usage tracking and logging
- Unit tests with mocked OpenAI API

**Definition of Done:**
- [ ] LLMClient with OpenAI integration
- [ ] Generates responses ≤35 words in <500ms
- [ ] Strict cache-only system prompt
- [ ] Fallback for API failures
- [ ] Response caching
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with real OpenAI API
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR14 (Natural language conversation), FR23 (Fast LLM with cache-only prompts)  
**Estimated Effort:** 6-8 hours

---

#### Story 2.5: Promo Manager Tool

**As a** retail edge service  
**I want** a tool to query active promotions  
**So that** Reachy can inform customers about current deals

**Acceptance Criteria:**

**Given** I am implementing the promo manager  
**When** I create the promo module  
**Then** the following exists:
- `reachy_edge/tools/promo_manager.py` with `PromoManager` class
- Promo data stored in SQLite (from L2 cache)
- Schema: `promo_id, product_sku, discount_pct, start_date, end_date, description`

**Given** sample promo data (10-15 active promos)  
**When** I call `promo_manager.get_active_promos(limit=3)`  
**Then** it returns top 3 active promos sorted by discount percentage  
**And** each promo includes: product name, discount, description

**Given** a product query "apples"  
**When** I call `promo_manager.get_promos_for_product("apples")`  
**Then** it returns promos matching product name  
**And** expired promos are excluded

**Given** no active promos  
**When** I query active promos  
**Then** it returns empty list  
**And** no exceptions are raised

**Given** the promo manager code  
**When** I review implementation  
**Then** it includes:
- Full type hints with Pydantic models
- Date/time handling for promo expiry
- SQL queries with proper indexing
- Error handling for database issues
- Unit tests with time mocking

**Definition of Done:**
- [ ] PromoManager with active promo queries
- [ ] Returns promos sorted by relevance/discount
- [ ] Handles expired promos correctly
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with sample promo data
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR20 (Promo manager tool)  
**Estimated Effort:** 4-6 hours

---

#### Story 2.6: Interaction State Machine - Core Flows

**As a** Reachy robot  
**I want** a finite state machine to manage interaction flows  
**So that** conversations follow logical patterns (greeting → query → response → farewell)

**Acceptance Criteria:**

**Given** I am implementing the FSM  
**When** I create the state machine module  
**Then** the following exists:
- `reachy_edge/fsm/interaction_fsm.py` with `InteractionFSM` class
- States: IDLE, GREETING, LISTENING, PROCESSING, RESPONDING, CLARIFYING, FAREWELL
- Transitions defined with guards and actions

**Given** a customer approaches (triggered externally)  
**When** FSM transitions to GREETING  
**Then** Reachy waves and says "Hi! How can I help you today?"  
**And** state transitions to LISTENING

**Given** FSM is in LISTENING state  
**When** customer speaks a query  
**Then** state transitions to PROCESSING  
**And** query is sent to /interact logic  
**And** state transitions to RESPONDING

**Given** FSM is in RESPONDING state  
**When** response is delivered (TTS complete)  
**Then** state transitions to LISTENING (awaiting follow-up)  
**Or** transitions to FAREWELL after 30s timeout

**Given** ambiguous query detected (multiple products, unclear intent)  
**When** FSM is in PROCESSING  
**Then** state transitions to CLARIFYING  
**And** Reachy asks one clarification question (FR16)  
**And** state transitions back to LISTENING

**Given** customer leaves or says "goodbye"  
**When** FSM is in any state  
**Then** state transitions to FAREWELL  
**And** Reachy says "Have a great day!" and waves  
**And** state resets to IDLE

**Given** the FSM code  
**When** I review implementation  
**Then** it includes:
- Full type hints and docstrings
- State transition logging (structured)
- Timeout handling for stuck states
- Event-driven architecture (async)
- Unit tests for all transitions

**Definition of Done:**
- [ ] InteractionFSM with 7+ states
- [ ] All state transitions tested
- [ ] Timeout handling (30s inactivity → FAREWELL)
- [ ] Clarification flow integrated (FR16)
- [ ] Unit tests ≥80% coverage
- [ ] Integration test simulating full interaction
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR16 (Clarification support), FR27 (Deal promotion flow), FR28 (Wayfinding flow), FR29 (Clarification flow)  
**Estimated Effort:** 8-10 hours

---

#### Story 2.7: Deal Promotion Flow

**As a** customer  
**I want** Reachy to proactively share current deals  
**So that** I can discover savings and special offers

**Acceptance Criteria:**

**Given** I am implementing the deal promotion flow  
**When** I integrate with FSM and PromoManager  
**Then** the flow works as follows:
1. GREETING: "Hi! We have some great deals today."
2. Fetch top 3 promos from PromoManager
3. RESPONDING: "We have 20% off organic apples, buy-one-get-one on cereal, and $2 off rotisserie chicken."
4. RESPONDING: "Would you like to know where any of these are?"
5. LISTENING: Await customer response

**Given** customer asks "where are the apples"  
**When** in LISTENING state after promo pitch  
**Then** FSM transitions to PROCESSING → RESPONDING  
**And** Reachy points toward Aisle 3  
**And** says location with gesture (FR15)

**Given** no active promos available  
**When** deal promotion flow is triggered  
**Then** Reachy skips promo pitch  
**And** proceeds directly to "How can I help you today?"

**Given** customer shows no interest (silence or "no thanks")  
**When** 10 seconds pass after promo pitch  
**Then** FSM transitions to standard wayfinding mode  
**And** awaits product queries

**Given** the deal promotion code  
**When** I review implementation  
**Then** it includes:
- Integration with PromoManager and LLM
- Natural language promo descriptions (≤35 words total)
- Gesture coordination during promo pitch
- Logging of customer engagement (accepts promo info vs ignores)

**Definition of Done:**
- [ ] Deal promotion flow integrated into FSM
- [ ] Fetches and presents top 3 promos
- [ ] Handles no-promo scenario gracefully
- [ ] Tracks customer engagement (NFR21)
- [ ] Integration test covering full flow
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR27 (Deal promotion flow)  
**Estimated Effort:** 4-6 hours

---

#### Story 2.8: Wayfinding Flow with Gestures

**As a** customer  
**I want** to ask where products are and receive spoken + gestural directions  
**So that** I can easily navigate the store

**Acceptance Criteria:**

**Given** I am implementing the wayfinding flow  
**When** customer asks "where are the apples"  
**Then** the flow executes:
1. PROCESSING: Query product cache (L1→L2)
2. RESPONDING: Generate response via LLM: "Apples are in Aisle 3 on the left side."
3. Gesture: Point toward Aisle 3 with arm + head turn
4. TTS: Deliver response while pointing
5. LISTENING: Await follow-up

**Given** a product not in cache  
**When** wayfinding flow processes query  
**Then** response is: "I'm sorry, I don't have that product in my database. Would you like help finding something else?"  
**And** no gesture is performed

**Given** multiple product matches (e.g., "apples" → 5 SKUs)  
**When** wayfinding flow processes query  
**Then** FSM transitions to CLARIFYING  
**And** Reachy asks: "We have Granny Smith, Fuji, and Honeycrisp apples. Which would you like?"  
**And** state returns to LISTENING for clarification

**Given** product location includes aisle and section  
**When** response is generated  
**Then** gesture direction is determined from location metadata  
**And** pointing accuracy is logged (for future calibration)

**Given** the wayfinding code  
**When** I review implementation  
**Then** it includes:
- Coordination between product lookup, LLM, TTS, and gestures
- Timing: gesture starts before TTS, holds during speech
- Error handling if gestures fail (speech continues)
- Logging of full interaction (query → products → response → gesture)

**Definition of Done:**
- [ ] Wayfinding flow with synchronized speech + gesture
- [ ] Handles no results and ambiguous queries
- [ ] Clarification flow triggers on multiple matches
- [ ] Full interaction completes in <3 seconds (NFR1)
- [ ] Integration test covering all scenarios
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR28 (Wayfinding flow), FR29 (Clarification flow)  
**Estimated Effort:** 6-8 hours

---

#### Story 2.9: Selfie Flow (Optional Engagement)

**As a** customer  
**I want** the option to take a selfie with Reachy  
**So that** I can share the experience on social media

**Acceptance Criteria:**

**Given** I am implementing the selfie flow  
**When** I integrate with FSM  
**Then** the flow works as:
1. After successful interaction, Reachy offers: "Would you like a selfie before you go?"
2. If customer agrees (detects "yes" or nod), FSM transitions to SELFIE state
3. Reachy says "Great! Let me get in position. Say cheese in 3... 2... 1..."
4. Countdown gesture: Reachy holds up fingers (3, 2, 1) or nods
5. Camera triggers, displays image on screen
6. No image storage (FR26, privacy)
7. FSM transitions to FAREWELL

**Given** customer declines selfie  
**When** offer is made  
**Then** Reachy says "No problem! Have a great day!"  
**And** FSM transitions to FAREWELL

**Given** camera is unavailable  
**When** selfie flow is triggered  
**Then** Reachy apologizes: "Sorry, the camera isn't working right now."  
**And** FSM transitions to FAREWELL

**Given** image capture succeeds  
**When** selfie is taken  
**Then** image is displayed for 5 seconds  
**And** image is discarded (not saved)  
**And** event is logged (selfie accepted, NFR23)

**Given** the selfie code  
**When** I review implementation  
**Then** it includes:
- Camera integration (OpenCV or Reachy SDK)
- Countdown coordination (TTS + gesture)
- Privacy enforcement (no storage, no transmission)
- Engagement tracking (acceptance rate for NFR23)

**Definition of Done:**
- [ ] Selfie flow integrated into FSM
- [ ] Countdown with gesture + speech
- [ ] Image capture and display (no storage)
- [ ] Tracks acceptance rate (NFR23 target: 10-20%)
- [ ] Privacy compliance (NFR26)
- [ ] Integration test (with camera mocking)
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR21 (Selfie coordination tool), FR30 (Selfie flow)  
**Estimated Effort:** 6-8 hours

---

**Epic 2 Total Estimated Effort:** 54-72 hours  
**Epic 2 Total FRs Covered:** 12 (FR13, FR14, FR15, FR16, FR20, FR21, FR22, FR23, FR27, FR28, FR29, FR30)

---

### Epic 3: π Intelligence Layer - Classification + Memory

#### Story 3.1: FastAPI Backend for π Service

**As a** π backend developer  
**I want** a FastAPI service structure for the universal intelligence layer  
**So that** edge devices can send events and receive classifications

**Acceptance Criteria:**

**Given** I am setting up π backend  
**When** I initialize the project  
**Then** the following structure exists:
- `pi_backend/main.py` with FastAPI app
- `pi_backend/config.py` with environment configuration
- `pi_backend/models/` for Pydantic models
- `pi_backend/db/` for database modules
- `pi_backend/classifier/` for classification pipeline
- `pi_backend/requirements.txt` (fastapi, uvicorn, sqlalchemy, pydantic, pyyaml)

**Given** the FastAPI app is running on localhost:8001  
**When** I call GET /health  
**Then** I receive 200 with:
```json
{
  "status": "healthy",
  "service": "pi-backend",
  "version": "0.1.0",
  "classifier_status": "ready",
  "database_status": "connected"
}
```

**Given** the project structure  
**When** I review the code  
**Then** it includes:
- Clean architecture (routes, services, repositories)
- Type hints throughout
- Comprehensive docstrings
- Structured logging setup
- Database connection management

**Definition of Done:**
- [ ] π backend project structure created
- [ ] FastAPI app starts successfully
- [ ] GET /health returns proper status
- [ ] Clean architecture with separation of concerns
- [ ] Code meets quality standards (NFR33-NFR47)
- [ ] README with setup instructions

**FR Coverage:** Foundation for FR1-FR11, FR24  
**Estimated Effort:** 3-4 hours

---

#### Story 3.2: Domain Plugin System with YAML Configuration

**As a** π backend  
**I want** a domain plugin system that loads configurations from YAML files  
**So that** new domains can be added without code changes

**Acceptance Criteria:**

**Given** I am implementing the domain plugin system  
**When** I create the plugin module  
**Then** the following exists:
- `pi_backend/plugins/` directory
- `pi_backend/plugins/loader.py` with `PluginLoader` class
- `pi_backend/plugins/domains/retail.yaml` (retail domain config)
- Domain config schema: name, intents[], entities[], tools[], canonical_types[]

**Given** retail domain YAML configuration  
**When** I load the domain  
**Then** it contains:
- Intents: product_location, promo_query, store_info, greeting, farewell
- Entities: product_name, product_sku, aisle, category, price
- Tools: product_lookup, promo_manager
- Canonical types: retail.entity.product, retail.event.query

**Given** I call `plugin_loader.load_domain("retail")`  
**When** YAML is parsed  
**Then** it returns a `DomainPlugin` object with:
- Parsed intent definitions (name, description, examples)
- Entity schemas with field types
- Tool registry
- Canonical type mappings

**Given** invalid YAML (missing required fields)  
**When** domain is loaded  
**Then** it raises `PluginValidationError` with details  
**And** error is logged

**Given** multiple domains in plugins/domains/  
**When** I call `plugin_loader.load_all_domains()`  
**Then** all valid domains are loaded  
**And** invalid domains are skipped with warnings

**Given** the plugin code  
**When** I review implementation  
**Then** it includes:
- Pydantic models for domain config validation
- Full type hints and docstrings
- YAML schema validation
- Unit tests with sample YAML files

**Definition of Done:**
- [ ] PluginLoader with YAML parsing
- [ ] retail.yaml domain configuration
- [ ] Domain config validation with Pydantic
- [ ] Unit tests ≥80% coverage
- [ ] Documentation for creating new domains
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR3 (Domain plugin system)  
**Estimated Effort:** 6-8 hours

---

#### Story 3.3: Multi-Stage Classification Pipeline (Stages 1-3)

**As a** π backend  
**I want** the first 3 stages of classification (Domain → Intent → Entity)  
**So that** I can transform raw queries into structured data

**Acceptance Criteria:**

**Given** I am implementing classification pipeline  
**When** I create the classifier module  
**Then** the following exists:
- `pi_backend/classifier/pipeline.py` with `ClassificationPipeline` class
- `pi_backend/classifier/stages/` with `DomainClassifier`, `IntentClassifier`, `EntityExtractor`
- LLM integration for classification (OpenAI API)

**Given** a query "where are the apples"  
**When** Stage 1 (Domain) classifies  
**Then** it returns: `{"domain": "retail", "confidence": 0.95}`  
**And** classification completes in <200ms (NFR5)

**Given** domain="retail" and query="where are the apples"  
**When** Stage 2 (Intent) classifies  
**Then** it returns: `{"intent": "product_location", "confidence": 0.92}`  
**And** uses retail domain's intent definitions

**Given** intent="product_location" and query="where are the apples"  
**When** Stage 3 (Entity) extracts  
**Then** it returns: `{"entities": [{"type": "product_name", "value": "apples", "span": [14, 20]}]}`  
**And** entity extraction uses retail domain's entity schema

**Given** ambiguous query "what's on sale"  
**When** classification pipeline runs  
**Then** confidence scores are returned for all stages  
**And** low confidence (<0.7) is flagged for potential clarification

**Given** unsupported domain detected (e.g., "medical")  
**When** Stage 1 classifies  
**Then** it returns: `{"domain": "unknown", "confidence": 0.3}`  
**And** pipeline gracefully handles unknown domains

**Given** the classifier code  
**When** I review implementation  
**Then** it includes:
- LLM prompts optimized for each stage
- Caching for repeated classifications (NFR8)
- Full type hints with Pydantic models
- Comprehensive error handling
- Unit tests with mocked LLM responses

**Definition of Done:**
- [ ] 3-stage pipeline (Domain → Intent → Entity)
- [ ] Classifications complete in <200ms for cached patterns (NFR5, NFR8)
- [ ] Confidence scoring at each stage
- [ ] Handles unknown domains gracefully
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with real LLM
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR1 (Multi-stage pipeline - stages 1-3), FR7 (Confidence scoring)  
**Estimated Effort:** 10-12 hours

---

#### Story 3.4: Multi-Stage Classification Pipeline (Stages 4-5)

**As a** π backend  
**I want** the final 2 stages of classification (Canonical → Response)  
**So that** events are stored in universal format and responses are generated

**Acceptance Criteria:**

**Given** I am completing the classification pipeline  
**When** I implement stages 4-5  
**Then** the following exists:
- `pi_backend/classifier/stages/canonical_mapper.py`
- `pi_backend/classifier/stages/response_generator.py`

**Given** entities extracted: `[{"type": "product_name", "value": "apples"}]`  
**When** Stage 4 (Canonical Mapping) runs  
**Then** it returns canonical event:
```json
{
  "event_type": "retail.event.query",
  "canonical_entities": [
    {"type": "retail.entity.product", "name": "apples"}
  ],
  "metadata": {"domain": "retail", "intent": "product_location"}
}
```

**Given** canonical event created  
**When** Stage 5 (Response) generates  
**Then** it returns suggested response structure:
```json
{
  "response_type": "location_info",
  "requires_cache": ["product_lookup"],
  "suggested_tools": ["product_lookup", "gesture_point"]
}
```

**Given** the full 5-stage pipeline  
**When** I process "where are the apples"  
**Then** output includes:
- Domain, intent, entities (stages 1-3)
- Canonical event (stage 4)
- Response plan (stage 5)
- Confidence scores for each stage
- Total latency <300ms (including all stages)

**Given** classification pipeline code  
**When** I review implementation  
**Then** it includes:
- Canonical type mappings from domain configs
- Response templates per intent type
- Explainability logging (FR7)
- Full type hints and docstrings

**Definition of Done:**
- [ ] Stages 4-5 complete (Canonical → Response)
- [ ] Full 5-stage pipeline functional
- [ ] Total classification <300ms
- [ ] Explainability with confidence scores (FR7)
- [ ] Unit tests ≥80% coverage
- [ ] Integration test end-to-end
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR1 (Multi-stage pipeline - stages 4-5), FR7 (Explainability)  
**Estimated Effort:** 8-10 hours

---

#### Story 3.5: Universal Canonical Storage (Events + Entities)

**As a** π backend  
**I want** universal storage for canonical events and entities  
**So that** all interactions are stored in queryable format

**Acceptance Criteria:**

**Given** I am implementing canonical storage  
**When** I create the storage module  
**Then** the following exists:
- `pi_backend/db/canonical_store.py` with `CanonicalStore` class
- SQLite tables: `events`, `entities`, `relationships`
- Schema for events: `event_id, event_type, domain, timestamp, payload (JSON), confidence`
- Schema for entities: `entity_id, entity_type, name, properties (JSON), created_at, updated_at`

**Given** a canonical event from classification  
**When** I call `canonical_store.save_event(event)`  
**Then** event is inserted into events table  
**And** event_id is returned  
**And** operation completes in <50ms

**Given** entities extracted from event  
**When** I call `canonical_store.save_entity(entity)`  
**Then** entity is checked for duplicates (FR8)  
**And** if duplicate exists, entity is merged  
**And** if new, entity is inserted  
**And** entity_id is returned

**Given** multiple events referencing same entity ("apples")  
**When** events are saved  
**Then** entity deduplication occurs (FR8)  
**And** all events reference the same entity_id  
**And** entity has updated properties from all events

**Given** query for entity history  
**When** I call `canonical_store.get_entity_events(entity_id)`  
**Then** all events referencing the entity are returned  
**And** events are sorted by timestamp

**Given** the canonical storage code  
**When** I review implementation  
**Then** it includes:
- SQLAlchemy ORM models
- Deduplication logic with fuzzy matching
- Indexing for fast queries (entity_type, event_type, timestamp)
- Full type hints and docstrings
- Unit tests with SQLite in-memory database

**Definition of Done:**
- [ ] CanonicalStore with events + entities tables
- [ ] Entity deduplication (FR8)
- [ ] Fast insertion (<50ms) and querying (<100ms)
- [ ] Unit tests ≥80% coverage
- [ ] Integration tests for deduplication scenarios
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR2 (Universal canonical storage), FR8 (Entity deduplication)  
**Estimated Effort:** 8-10 hours

---

#### Story 3.6: Knowledge Graph with Relationships

**As a** π backend  
**I want** a knowledge graph that captures relationships between entities  
**So that** I can answer complex queries with context

**Acceptance Criteria:**

**Given** I am implementing the knowledge graph  
**When** I create the graph module  
**Then** the following exists:
- `pi_backend/db/knowledge_graph.py` with `KnowledgeGraph` class
- SQLite table: `relationships` (subject_id, predicate, object_id, weight, created_at)
- Relationship types: located_in, part_of, associated_with, related_to

**Given** entities: Product("apples"), Location("Aisle 3")  
**When** relationship is inferred from event  
**Then** relationship is created: `apples --[located_in]--> Aisle 3`  
**And** relationship weight is 1.0 (initial)

**Given** repeated queries about same relationship  
**When** relationships are updated  
**Then** weight increases (relationship strength)  
**And** stronger relationships influence future classifications

**Given** a query "what else is in Aisle 3"  
**When** I call `knowledge_graph.query_related(entity="Aisle 3", predicate="located_in", direction="incoming")`  
**Then** it returns all products located in Aisle 3  
**And** query completes in <100ms (NFR7)

**Given** entity "apples" with multiple relationships  
**When** I call `knowledge_graph.get_entity_context(entity_id)`  
**Then** it returns:
- Direct relationships (1-hop)
- Relationship types and weights
- Related entities with metadata

**Given** the knowledge graph code  
**When** I review implementation  
**Then** it includes:
- Graph query optimizations (indexing on subject/object)
- Relationship weight decay over time (optional)
- Full type hints and docstrings
- Unit tests with graph scenarios

**Definition of Done:**
- [ ] KnowledgeGraph with relationships table
- [ ] Relationship creation and querying
- [ ] Weight tracking for relationship strength
- [ ] Queries complete in <100ms (NFR7)
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with multi-hop queries
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR9 (Knowledge graph with relationships)  
**Estimated Effort:** 8-10 hours

---

#### Story 3.7: Context and Reasoning Engine

**As a** π backend  
**I want** a context engine that tracks sessions and uses knowledge graph  
**So that** multi-turn conversations maintain context

**Acceptance Criteria:**

**Given** I am implementing the context engine  
**When** I create the module  
**Then** the following exists:
- `pi_backend/context/reasoning_engine.py` with `ReasoningEngine` class
- Session storage: `sessions` table (session_id, user_id, store_id, started_at, context (JSON))
- Integration with KnowledgeGraph

**Given** a new interaction from edge device  
**When** context engine processes event  
**Then** session is created or resumed  
**And** previous context is loaded (last 5 interactions)

**Given** query "where are the apples" followed by "how much are they"  
**When** second query is processed  
**Then** reasoning engine:
1. Loads session context (previous query about apples)
2. Resolves "they" → "apples" via entity resolution
3. Adds context to classification pipeline
4. Returns response with price for apples

**Given** session context with knowledge graph  
**When** ambiguous query is processed  
**Then** reasoning engine queries graph for related entities  
**And** uses graph context to improve classification confidence

**Given** session expires (30 minutes inactivity)  
**When** new interaction arrives  
**Then** new session is created  
**And** old session is archived

**Given** the context engine code  
**When** I review implementation  
**Then** it includes:
- Session management with TTL
- Entity resolution (pronouns → entities)
- Context window management (sliding window)
- Full type hints and docstrings
- Unit tests with session scenarios

**Definition of Done:**
- [ ] ReasoningEngine with session tracking
- [ ] Multi-turn context resolution
- [ ] Integration with KnowledgeGraph
- [ ] Session TTL and cleanup
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with multi-turn conversation
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR4 (Context and reasoning engine)  
**Estimated Effort:** 10-12 hours

---

#### Story 3.8: Event Ingestion API from Edge Devices

**As an** edge device  
**I want** to send interaction events to π asynchronously  
**So that** π learns from all edge interactions

**Acceptance Criteria:**

**Given** I am implementing event ingestion  
**When** I create the API endpoint  
**Then** the following exists:
- POST /events/ingest endpoint
- Request schema: `{"events": [{"event_type", "domain", "payload", "timestamp", "device_id"}]}`
- Batch processing support (up to 100 events per request)

**Given** edge device sends interaction event  
**When** POST /events/ingest is called  
**Then** events are:
1. Validated (schema, required fields)
2. Queued for async processing
3. Response returned immediately (202 Accepted)
4. Background worker processes events (classification + storage)

**Given** batch of 50 events  
**When** ingestion processes batch  
**Then** all events are classified via pipeline  
**And** canonical events are stored  
**And** knowledge graph is updated  
**And** processing completes in <5 seconds

**Given** duplicate events (same event_id)  
**When** ingestion detects duplicates  
**Then** duplicates are skipped  
**And** warning is logged

**Given** invalid event (malformed JSON, missing fields)  
**When** ingestion validates  
**Then** 400 error is returned with details  
**And** valid events in batch are still processed

**Given** the event ingestion code  
**When** I review implementation  
**Then** it includes:
- Async task queue (e.g., Celery, background tasks)
- Batch processing optimizations
- Idempotency (duplicate detection)
- Full type hints and docstrings
- Unit tests with batch scenarios

**Definition of Done:**
- [ ] POST /events/ingest endpoint
- [ ] Async batch processing (up to 100 events)
- [ ] Returns 202 immediately, processes in background
- [ ] Duplicate detection
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with edge device simulation
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR6 (Event ingestion API), FR24 (Async event emission)  
**Estimated Effort:** 8-10 hours

---

#### Story 3.9: External Data Feed Ingestion

**As a** π backend  
**I want** to ingest external data feeds (price updates, promo schedules)  
**So that** edge caches stay current without manual updates

**Acceptance Criteria:**

**Given** I am implementing feed ingestion  
**When** I create the feed adapters  
**Then** the following exists:
- `pi_backend/feeds/` directory
- `pi_backend/feeds/adapters/product_feed.py` for product catalogs
- `pi_backend/feeds/adapters/promo_feed.py` for promotional data
- `pi_backend/feeds/scheduler.py` for periodic ingestion

**Given** a CSV product feed (SKU, name, price, location)  
**When** product feed adapter runs  
**Then** it:
1. Downloads/reads CSV
2. Validates schema
3. Transforms to canonical product entities
4. Updates canonical storage
5. Triggers cache regeneration

**Given** a JSON promo feed (promo_id, product_sku, discount, dates)  
**When** promo feed adapter runs  
**Then** it:
1. Fetches JSON from API/file
2. Validates schema
3. Creates promo entities
4. Links to products via SKU
5. Updates knowledge graph (product --[has_promo]--> promo)

**Given** feed ingestion is scheduled (cron: daily at 2 AM)  
**When** scheduler runs  
**Then** all feed adapters execute  
**And** logs report success/failure for each feed  
**And** errors trigger alerts (logged at ERROR level)

**Given** feed data conflicts with existing entities  
**When** normalization occurs  
**Then** entities are merged with deduplication logic  
**And** conflicts are logged for review

**Given** the feed ingestion code  
**When** I review implementation  
**Then** it includes:
- Adapter pattern for extensibility
- Schema validation (Pydantic)
- Error handling and retries
- Full type hints and docstrings
- Unit tests with sample feeds

**Definition of Done:**
- [ ] Feed adapters for products and promos
- [ ] Scheduled ingestion (configurable)
- [ ] Schema validation and normalization
- [ ] Error handling with logging
- [ ] Unit tests ≥80% coverage
- [ ] Integration test with sample feeds
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR11 (External data feed ingestion)  
**Estimated Effort:** 8-10 hours

---

#### Story 3.10: Evaluation and Replay System

**As a** π developer  
**I want** to replay historical events and evaluate classification accuracy  
**So that** I can test and improve the classifier

**Acceptance Criteria:**

**Given** I am implementing the evaluation system  
**When** I create the evaluation module  
**Then** the following exists:
- `pi_backend/eval/replay.py` with `ReplayEngine` class
- `pi_backend/eval/metrics.py` for accuracy tracking
- CLI tool: `python -m pi_backend.eval.replay --since "2026-01-01"`

**Given** historical events in canonical storage  
**When** I run replay with date range  
**Then** events are re-classified with current pipeline  
**And** results are compared to original classifications  
**And** accuracy metrics are reported

**Given** replay results  
**When** evaluation completes  
**Then** metrics include:
- Domain accuracy (FR15: ≥95%)
- Intent accuracy (FR16: ≥90%)
- Entity F1 score (FR17: ≥85%)
- Confidence distribution
- Misclassified events (for review)

**Given** ground truth labels (manually labeled events)  
**When** evaluation runs with ground truth  
**Then** precision, recall, F1 scores are calculated  
**And** confusion matrix is generated per stage

**Given** A/B test scenario (two classifier versions)  
**When** replay runs with both versions  
**Then** comparative metrics are generated  
**And** better-performing version is identified

**Given** the evaluation code  
**When** I review implementation  
**Then** it includes:
- Batch replay processing (efficient)
- Metrics tracking and reporting
- Export to JSON/CSV for analysis
- Full type hints and docstrings

**Definition of Done:**
- [ ] ReplayEngine with date-range replay
- [ ] Metrics tracking (accuracy, precision, recall, F1)
- [ ] CLI tool for evaluation
- [ ] Ground truth comparison support
- [ ] Unit tests ≥80% coverage
- [ ] Documentation for running evaluations
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR10 (Evaluation and replay system)  
**Estimated Effort:** 8-10 hours

---

**Epic 3 Total Estimated Effort:** 77-96 hours  
**Epic 3 Total FRs Covered:** 10 (FR1, FR2, FR3, FR4, FR6, FR7, FR8, FR9, FR10, FR11, FR24)

---

### Epic 4: Edge-π Sync - Distributed Architecture

#### Story 4.1: Cache Generation Engine

**As a** π backend  
**I want** to generate domain-filtered cache snapshots for edge devices  
**So that** edges have optimized, up-to-date data

**Acceptance Criteria:**

**Given** I am implementing cache generation  
**When** I create the cache generator  
**Then** the following exists:
- `pi_backend/cache/generator.py` with `CacheGenerator` class
- Function: `generate_cache(domain: str, store_id: str) -> CacheSnapshot`
- Output format: JSON with products, promos, config

**Given** retail domain with 1000 products in canonical storage  
**When** I call `generate_cache(domain="retail", store_id="store-001")`  
**Then** it:
1. Filters products by store_id (multi-tenant, FR12)
2. Includes active promos for store
3. Generates FTS5-optimized product data
4. Creates L1 cache seed (top 100 hot products)
5. Returns CacheSnapshot with metadata

**Given** cache generation for store-001  
**When** snapshot is created  
**Then** it includes:
```json
{
  "cache_version": "v1.0.0-20260110",
  "domain": "retail",
  "store_id": "store-001",
  "generated_at": "2026-01-10T12:00:00Z",
  "products": [...],
  "promos": [...],
  "l1_seed": [...],
  "config": {"cache_ttl": 86400}
}
```

**Given** knowledge graph with product relationships  
**When** cache is generated  
**Then** frequently co-queried products are prioritized in L1 seed  
**And** relationship metadata is included

**Given** cache generation completes  
**When** I measure performance  
**Then** generation takes <10 seconds for 1000 products  
**And** output size is <100MB (meets FR18)

**Given** the cache generator code  
**When** I review implementation  
**Then** it includes:
- Multi-tenant filtering (store-specific data)
- Domain plugin integration (configurable fields)
- Compression options (gzip)
- Full type hints and docstrings
- Unit tests with canonical storage mock

**Definition of Done:**
- [ ] CacheGenerator with domain filtering
- [ ] Multi-tenant support (store_id filtering)
- [ ] L1 seed optimization (top 100 hot items)
- [ ] Cache version tracking
- [ ] Generation <10 seconds for 1000 products
- [ ] Output ≤100MB (FR18)
- [ ] Unit tests ≥80% coverage
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR5 (Cache generation engine), FR12 (Multi-tenant support)  
**Estimated Effort:** 8-10 hours

---

#### Story 4.2: Incremental Cache Sync Protocol

**As an** edge device  
**I want** to sync cache incrementally (only changed data)  
**So that** sync is fast and bandwidth-efficient

**Acceptance Criteria:**

**Given** I am implementing cache sync  
**When** I create the sync protocol  
**Then** the following exists:
- π endpoint: GET /cache/sync?domain=retail&store_id=store-001&since_version=v1.0.0-20260109
- Edge endpoint: POST /cache/apply (receives cache diff)
- Diff format: added, updated, deleted items

**Given** edge has cache version v1.0.0-20260109  
**When** edge requests sync from π  
**Then** π:
1. Compares current cache with edge version
2. Generates diff (added/updated/deleted products/promos)
3. Returns diff with new version tag
4. Diff size is minimal (only changes)

**Given** diff: 5 products updated, 2 promos added, 1 product deleted  
**When** edge applies diff  
**Then** edge:
1. Updates L2 (SQLite) with changes
2. Invalidates L1 cache entries for updated items
3. Updates cache version to new tag
4. Logs sync completion

**Given** sync latency requirement (NFR6: <5s)  
**When** sync executes  
**Then** full sync (fetch diff + apply) completes in <5 seconds  
**And** edge remains operational during sync

**Given** network failure during sync  
**When** sync is interrupted  
**Then** edge retries with exponential backoff  
**And** partial changes are rolled back (atomic sync)

**Given** edge and π out of sync (version mismatch)  
**When** edge requests sync  
**Then** π detects large gap and triggers full cache refresh  
**And** edge receives complete snapshot

**Given** the sync protocol code  
**When** I review implementation  
**Then** it includes:
- Versioning (semantic versioning)
- Diff algorithm (efficient comparison)
- Atomic sync (all-or-nothing)
- Retry logic with backoff
- Full type hints and docstrings

**Definition of Done:**
- [ ] Incremental sync protocol (diff-based)
- [ ] GET /cache/sync endpoint on π
- [ ] POST /cache/apply endpoint on edge
- [ ] Sync latency <5s (NFR6)
- [ ] Atomic sync with rollback
- [ ] Unit tests ≥80% coverage
- [ ] Integration test (π ↔ edge)
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR25 (Cache sync protocol with incremental updates), FR12 (Multi-tenant in sync)  
**Estimated Effort:** 10-12 hours

---

#### Story 4.3: Multi-Tenant Architecture

**As a** π backend  
**I want** strict data isolation per store/user  
**So that** multi-tenant deployment is secure and correct

**Acceptance Criteria:**

**Given** I am implementing multi-tenancy  
**When** I create the tenant module  
**Then** the following exists:
- `pi_backend/tenancy/tenant_context.py` with `TenantContext` class
- Middleware: `TenantMiddleware` (extracts tenant from headers/tokens)
- Database: All tables have `tenant_id` column (store_id or user_id)

**Given** an API request with header `X-Tenant-ID: store-001`  
**When** request is processed  
**Then** TenantMiddleware:
1. Extracts tenant_id from header
2. Sets TenantContext for request scope
3. All database queries auto-filter by tenant_id

**Given** cache generation for store-001  
**When** query retrieves products  
**Then** only products with tenant_id=store-001 are returned  
**And** no data leakage from other stores

**Given** event ingestion from edge device  
**When** events are saved  
**Then** all events, entities, relationships include tenant_id  
**And** tenant_id is validated against allowed tenants

**Given** query without tenant_id (missing header)  
**When** request is processed  
**Then** 400 error is returned: "Missing tenant ID"  
**And** no database access occurs

**Given** malicious request with different tenant_id  
**When** edge device attempts to access another store's data  
**Then** 403 Forbidden is returned  
**And** security event is logged

**Given** the multi-tenancy code  
**When** I review implementation  
**Then** it includes:
- Row-level security (tenant_id filtering)
- Tenant validation on all mutations
- Audit logging for tenant access
- Full type hints and docstrings
- Unit tests with multi-tenant scenarios

**Definition of Done:**
- [ ] TenantContext and TenantMiddleware
- [ ] All tables with tenant_id column
- [ ] Auto-filtering queries by tenant
- [ ] Tenant validation on all API endpoints
- [ ] Security tests (cross-tenant access attempts)
- [ ] Unit tests ≥80% coverage
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR12 (Multi-tenant support with isolation)  
**Estimated Effort:** 8-10 hours

---

#### Story 4.4: Event Emission from Edge (Async Batching)

**As an** edge device  
**I want** to emit events to π asynchronously in batches  
**So that** π learns without blocking edge interactions

**Acceptance Criteria:**

**Given** I am implementing event emission on edge  
**When** I create the emitter module  
**Then** the following exists:
- `reachy_edge/events/emitter.py` with `EventEmitter` class
- In-memory event queue (max size: 1000)
- Background worker (async task)
- Batch size: 50 events per POST

**Given** customer interaction completes on edge  
**When** interaction event is created  
**Then** event is:
1. Added to in-memory queue (non-blocking)
2. Edge interaction continues immediately
3. Background worker batches events
4. Batch sent to π when queue reaches 50 or 30s timeout

**Given** event queue with 50 events  
**When** batch is sent to π  
**Then** POST /events/ingest is called  
**And** π returns 202 Accepted  
**And** events are removed from queue  
**And** retry on failure (3 attempts)

**Given** network is unavailable  
**When** events are queued  
**Then** queue accumulates up to 1000 events  
**And** oldest events are persisted to disk if queue overflows  
**And** events sync when network recovers

**Given** π is down  
**When** batch send fails after retries  
**Then** events are persisted to local storage  
**And** ERROR is logged with retry schedule

**Given** edge restarts  
**When** emitter initializes  
**Then** persisted events are loaded from disk  
**And** resume sending to π

**Given** the event emitter code  
**When** I review implementation  
**Then** it includes:
- Async task queue (threading or asyncio)
- Retry logic with exponential backoff
- Disk persistence for durability
- Full type hints and docstrings
- Unit tests with π mocked

**Definition of Done:**
- [ ] EventEmitter with async batching
- [ ] Batch size: 50 events or 30s timeout
- [ ] Retry logic (3 attempts)
- [ ] Disk persistence on overflow/failure
- [ ] Non-blocking (edge interactions unaffected)
- [ ] Unit tests ≥80% coverage
- [ ] Integration test (edge → π)
- [ ] Code meets quality standards (NFR33-NFR47)

**FR Coverage:** FR24 (Async event emission to π)  
**Estimated Effort:** 8-10 hours

---

**Epic 4 Total Estimated Effort:** 34-42 hours  
**Epic 4 Total FRs Covered:** 4 (FR5, FR6, FR12, FR25) + FR24 (from Epic 3)

---

### Epic 5: Production Readiness - Quality & Observability

#### Story 5.1: Comprehensive Unit Testing (≥80% Coverage)

**As a** developer  
**I want** comprehensive unit tests for all modules  
**So that** code quality meets production standards (NFR39)

**Acceptance Criteria:**

**Given** I am implementing unit tests  
**When** I set up testing infrastructure  
**Then** the following exists:
- `pytest` configured for both edge and π backends
- `tests/` directories mirroring source structure
- `pytest.ini` with coverage configuration (target: 80%)
- `requirements-dev.txt` with test dependencies

**Given** all core modules (cache, database, tools, FSM, classifier)  
**When** unit tests are written  
**Then** each module has:
- Test file with ≥80% line coverage
- Tests for happy path and edge cases
- Mocked external dependencies (APIs, databases)
- Parameterized tests for multiple scenarios

**Given** pytest runs  
**When** I execute `pytest --cov`  
**Then** coverage report shows:
- Edge backend: ≥80% coverage
- π backend: ≥80% coverage
- Failing tests cause CI to fail
- Coverage report generated (HTML + terminal)

**Given** time-dependent code (TTL, caching)  
**When** tests are written  
**Then** time is mocked (freezegun, unittest.mock)  
**And** tests are deterministic (no flaky tests)

**Given** async code (event emitter, API calls)  
**When** tests are written  
**Then** pytest-asyncio is used  
**And** async functions are properly awaited

**Definition of Done:**
- [ ] Unit tests for all modules (edge + π)
- [ ] ≥80% line coverage (NFR39)
- [ ] Tests run in CI pipeline
- [ ] No flaky tests (deterministic)
- [ ] Coverage report generated
- [ ] Documentation for running tests

**NFR Coverage:** NFR39 (Unit test coverage ≥80%)  
**Estimated Effort:** 20-24 hours (distributed across all epics)

---

#### Story 5.2: Integration Testing (API + Database)

**As a** developer  
**I want** integration tests for all API endpoints and database operations  
**So that** components work correctly together (NFR40)

**Acceptance Criteria:**

**Given** I am implementing integration tests  
**When** I create test suites  
**Then** the following exists:
- `tests/integration/` directories for edge and π
- TestClient (FastAPI) for API testing
- Docker Compose for test databases (SQLite/PostgreSQL)

**Given** edge backend endpoints (/interact, /health, /cache/apply)  
**When** integration tests run  
**Then** each endpoint is tested with:
- Real database (SQLite in-memory or temp file)
- Multiple request scenarios (valid, invalid, edge cases)
- Response validation (status, schema, data)
- Latency assertions (NFR1, NFR2)

**Given** π backend endpoints (/events/ingest, /cache/sync, /health)  
**When** integration tests run  
**Then** each endpoint is tested with:
- Real database and classification pipeline
- Multi-tenant scenarios
- Batch processing validation
- Error handling verification

**Given** edge → π sync flow  
**When** integration test runs  
**Then** it:
1. Generates cache on π
2. Edge fetches cache
3. Edge applies cache
4. Edge emits events to π
5. π ingests and classifies events
6. Verifies end-to-end flow

**Given** integration tests complete  
**When** CI runs  
**Then** all tests pass  
**And** test database is cleaned up  
**And** test duration is <5 minutes

**Definition of Done:**
- [ ] Integration tests for all API endpoints (NFR40)
- [ ] End-to-end sync flow tested
- [ ] Real database usage (test isolation)
- [ ] Tests run in CI pipeline
- [ ] Test duration <5 minutes
- [ ] Documentation for running integration tests

**NFR Coverage:** NFR40 (Integration tests for all API endpoints)  
**Estimated Effort:** 16-20 hours

---

#### Story 5.3: Structured Logging with Trace IDs

**As a** system operator  
**I want** structured, contextual logging with trace IDs  
**So that** I can debug issues efficiently (NFR43)

**Acceptance Criteria:**

**Given** I am implementing structured logging  
**When** I configure logging  
**Then** the following exists:
- `structlog` or similar library configured
- Log format: JSON with timestamp, level, message, context
- Trace ID generation for all requests
- Context propagation (edge → π)

**Given** an API request to edge  
**When** request is processed  
**Then** trace_id is:
1. Generated (UUID) at request start
2. Added to all log entries for that request
3. Included in response headers (X-Trace-ID)
4. Propagated to π in event payloads

**Given** a log entry  
**When** logged  
**Then** it includes:
```json
{
  "timestamp": "2026-01-10T12:34:56.789Z",
  "level": "INFO",
  "message": "Product query processed",
  "trace_id": "abc-123-def",
  "module": "reachy_edge.api.interact",
  "query": "apples",
  "cache_hit": true,
  "latency_ms": 45
}
```

**Given** multi-service interaction (edge + π)  
**When** trace is logged  
**Then** trace_id connects logs across services  
**And** full request flow is traceable

**Given** error occurs  
**When** exception is raised  
**Then** log includes:
- ERROR level
- Stack trace
- Request context (query, user, store)
- Trace ID for debugging

**Given** log levels  
**When** configured  
**Then** production uses INFO  
**And** debug mode uses DEBUG with additional context

**Definition of Done:**
- [ ] Structured logging (JSON format)
- [ ] Trace ID generation and propagation
- [ ] Context included in all logs
- [ ] Log levels configurable (env var)
- [ ] Error logging with stack traces
- [ ] Documentation for log analysis

**NFR Coverage:** NFR43 (Proper logging: structured, leveled, contextual)  
**Estimated Effort:** 6-8 hours

---

#### Story 5.4: Metrics Collection and Monitoring

**As a** system operator  
**I want** metrics for latency, cache hits, and system health  
**So that** I can monitor performance and diagnose issues

**Acceptance Criteria:**

**Given** I am implementing metrics  
**When** I set up metrics collection  
**Then** the following exists:
- `prometheus_client` library integrated
- Metrics endpoint: GET /metrics (Prometheus format)
- Key metrics defined (counters, histograms, gauges)

**Given** edge backend metrics  
**When** collected  
**Then** they include:
- `edge_requests_total` (counter: endpoint, status)
- `edge_request_duration_seconds` (histogram: P50/P95/P99)
- `cache_hits_total` (counter: cache_level=l1/l2)
- `cache_misses_total` (counter)
- `cache_size` (gauge: l1_size, l2_size)
- `llm_requests_total` (counter: model)
- `llm_tokens_total` (counter: type=input/output)

**Given** π backend metrics  
**When** collected  
**Then** they include:
- `pi_events_ingested_total` (counter: domain, event_type)
- `pi_classification_duration_seconds` (histogram: stage)
- `pi_classification_confidence` (histogram: stage)
- `pi_cache_generation_duration_seconds` (histogram)
- `pi_knowledge_graph_size` (gauge: entities, relationships)

**Given** metrics endpoint  
**When** Prometheus scrapes GET /metrics  
**Then** metrics are returned in Prometheus format  
**And** scrape completes in <100ms

**Given** Grafana dashboard (optional but recommended)  
**When** configured  
**Then** it displays:
- Request latency (P95, target: <1s per NFR1)
- Cache hit rate (target: ≥90% per NFR19)
- Classification accuracy trends
- System health (uptime, error rate)

**Definition of Done:**
- [ ] Prometheus metrics for edge and π
- [ ] Key performance metrics (latency, cache, accuracy)
- [ ] GET /metrics endpoint
- [ ] Grafana dashboard (optional)
- [ ] Documentation for metrics and alerts

**NFR Coverage:** NFR1-NFR8 (Performance metrics), NFR19 (Cache hit rate tracking)  
**Estimated Effort:** 8-10 hours

---

#### Story 5.5: Performance Profiling and Optimization

**As a** developer  
**I want** to profile and optimize critical paths  
**So that** system meets all performance requirements (NFR1-NFR8, NFR45)

**Acceptance Criteria:**

**Given** I am profiling the system  
**When** I run performance tests  
**Then** the following is validated:
- P95 interaction latency <1s (NFR1)
- Fast path (cache-only) <500ms (NFR2)
- L1 cache hit <10ms (NFR3)
- L2 cache query <100ms (NFR4)
- π classification <200ms for cached patterns (NFR5)
- Cache sync <5s (NFR6)
- Knowledge graph query <100ms (NFR7)

**Given** profiling tools (cProfile, py-spy)  
**When** critical paths are profiled  
**Then** bottlenecks are identified:
- Database query optimization (indexing)
- FTS5 query tuning
- LLM call optimization (caching, prompt size)
- JSON serialization (use orjson if needed)

**Given** optimization opportunities  
**When** implemented  
**Then** performance improvements are measured  
**And** regressions are prevented (performance tests in CI)

**Given** load testing (locust, k6)  
**When** system is tested under load  
**Then** it handles:
- 100 concurrent edge requests (NFR30 scalability)
- Cache sync for 10 edge devices simultaneously
- Event ingestion at 1000 events/min

**Given** performance benchmarks  
**When** documented  
**Then** baseline metrics are recorded  
**And** future changes are compared to baseline

**Definition of Done:**
- [ ] All NFR latency targets validated
- [ ] Profiling conducted, bottlenecks addressed
- [ ] Load testing passed (100 concurrent requests)
- [ ] Performance tests in CI
- [ ] Optimization documentation

**NFR Coverage:** NFR1-NFR8 (Performance), NFR45 (Performance optimizations)  
**Estimated Effort:** 12-16 hours

---

#### Story 5.6: Security Hardening

**As a** security engineer  
**I want** comprehensive input validation and sanitization  
**So that** system is secure against attacks (NFR44)

**Acceptance Criteria:**

**Given** I am hardening security  
**When** I review all inputs  
**Then** the following is implemented:
- Pydantic models for all API inputs (automatic validation)
- SQL parameterized queries (no SQL injection)
- Input sanitization for user queries (XSS prevention)
- Rate limiting on API endpoints
- Authentication/authorization (token-based for π)

**Given** user query input "'; DROP TABLE products; --"  
**When** processed  
**Then** query is safely parameterized  
**And** no SQL injection occurs  
**And** malicious attempt is logged

**Given** API without rate limiting  
**When** rate limiter is added  
**Then** requests are limited to:
- Edge: 100 requests/minute per device
- π: 1000 requests/minute per tenant
- Excess requests return 429 (Too Many Requests)

**Given** sensitive data (tenant IDs, session tokens)  
**When** logged  
**Then** sensitive fields are redacted  
**And** logs don't expose PII

**Given** API authentication  
**When** π endpoints are accessed  
**Then** valid API key or JWT is required  
**And** invalid auth returns 401 Unauthorized

**Given** security scan (bandit, safety)  
**When** run on codebase  
**Then** no high/critical vulnerabilities detected  
**And** scan runs in CI pipeline

**Definition of Done:**
- [ ] Input validation with Pydantic (NFR44)
- [ ] SQL injection prevention (parameterized queries)
- [ ] Rate limiting on all endpoints
- [ ] Authentication for π API
- [ ] Security scanning in CI
- [ ] No PII in logs (NFR25, NFR26)

**NFR Coverage:** NFR25-NFR29 (Security & Privacy), NFR44 (Security best practices)  
**Estimated Effort:** 10-12 hours

---

#### Story 5.7: Error Handling and Resilience

**As a** developer  
**I want** comprehensive error handling with no silent failures  
**So that** system is reliable and debuggable (NFR38, NFR9, NFR10)

**Acceptance Criteria:**

**Given** I am implementing error handling  
**When** I review all code paths  
**Then** the following exists:
- Try-except blocks for all external calls (DB, API, LLM)
- Descriptive exceptions (custom exception classes)
- Error responses with proper HTTP status codes
- No bare `except:` clauses (specific exceptions only)

**Given** database connection fails  
**When** edge attempts query  
**Then** it:
1. Logs ERROR with context
2. Returns 503 Service Unavailable
3. Retries with exponential backoff (3 attempts)
4. Degrades gracefully (returns cached response if available)

**Given** LLM API is down  
**When** response generation is attempted  
**Then** it:
1. Falls back to template-based response
2. Logs WARNING with LLM status
3. Continues functioning (degraded mode)
4. Increments `llm_failures_total` metric

**Given** classification pipeline fails  
**When** event is processed  
**Then** it:
1. Logs ERROR with trace_id and event payload
2. Stores event in failed_events table for retry
3. Returns error response to edge
4. Alerts are triggered (if configured)

**Given** unhandled exception occurs  
**When** request is processed  
**Then** FastAPI exception handler:
1. Logs full stack trace
2. Returns 500 with error_id (for support)
3. Does NOT expose internal details to client
4. Increments `unhandled_errors_total` metric

**Given** reliability targets  
**When** validated  
**Then** system meets:
- ≥99% crash-free interactions (NFR9)
- <1% unhandled errors (NFR10)
- Graceful degradation under failures (NFR13)

**Definition of Done:**
- [ ] Comprehensive error handling (no silent failures, NFR38)
- [ ] Retry logic for transient failures
- [ ] Graceful degradation (NFR13)
- [ ] Error metrics tracked (NFR9, NFR10)
- [ ] Error handling tested (fault injection)
- [ ] Documentation for error codes

**NFR Coverage:** NFR9-NFR14 (Reliability), NFR38 (Comprehensive error handling)  
**Estimated Effort:** 10-12 hours

---

#### Story 5.8: CI/CD Pipeline with Quality Gates

**As a** DevOps engineer  
**I want** automated CI/CD pipeline with quality gates  
**So that** only high-quality code is deployed (NFR46, NFR47)

**Acceptance Criteria:**

**Given** I am setting up CI/CD  
**When** I configure pipeline  
**Then** the following exists:
- GitHub Actions (or similar) workflow
- Stages: lint → test → build → deploy
- Quality gates at each stage (fails on errors)

**Given** code is pushed to repository  
**When** CI runs  
**Then** pipeline executes:
1. **Lint stage**: `ruff`, `black --check`, `mypy` (type checking)
2. **Test stage**: `pytest` with coverage report
3. **Security stage**: `bandit`, `safety` (dependency check)
4. **Build stage**: Docker image build (if applicable)
5. **Deploy stage**: Deploy to staging (if tests pass)

**Given** any stage fails  
**When** pipeline runs  
**Then** deployment is blocked  
**And** PR cannot be merged  
**And** developer is notified

**Given** test coverage <80%  
**When** tests run  
**Then** pipeline fails  
**And** coverage report is posted to PR

**Given** type checking fails (mypy errors)  
**When** lint stage runs  
**Then** pipeline fails  
**And** type errors are reported

**Given** code review required (NFR46)  
**When** PR is created  
**Then** at least 1 approval is required  
**And** all checks must pass before merge

**Given** deployment to production  
**When** release is triggered  
**Then** pipeline:
1. Runs full test suite
2. Builds production artifacts
3. Deploys with blue-green strategy (zero downtime)
4. Runs smoke tests on deployed version
5. Rolls back on smoke test failure

**Definition of Done:**
- [ ] CI/CD pipeline configured (GitHub Actions)
- [ ] Quality gates (lint, test, security)
- [ ] Test coverage enforcement (≥80%)
- [ ] Type checking (mypy) in CI
- [ ] Code review required (NFR46)
- [ ] Automated deployment to staging
- [ ] Documentation for CI/CD process

**NFR Coverage:** NFR46 (Code reviews required), NFR47 (CI/CD with quality gates)  
**Estimated Effort:** 8-10 hours

---

#### Story 5.9: Documentation and Code Quality Standards

**As a** developer  
**I want** comprehensive documentation and enforced code standards  
**So that** codebase is maintainable (NFR33-NFR42)

**Acceptance Criteria:**

**Given** I am documenting the project  
**When** I create documentation  
**Then** the following exists:
- README.md with project overview, setup, and usage
- ARCHITECTURE.md with system design
- API.md with endpoint documentation
- CONTRIBUTING.md with code standards
- Docstrings for all public APIs (NFR35)

**Given** code standards are defined  
**When** documented  
**Then** CONTRIBUTING.md includes:
- Type hints required (Python 3.11+, NFR34)
- Docstrings format (Google/NumPy style)
- Clean architecture principles (NFR36)
- SOLID principles (NFR37)
- Code review checklist

**Given** API documentation  
**When** FastAPI is configured  
**Then** OpenAPI docs are auto-generated:
- GET /docs (Swagger UI)
- GET /redoc (ReDoc UI)
- Complete with request/response schemas

**Given** code quality is enforced  
**When** linters run  
**Then** they check:
- `ruff`: Flake8, isort, pyupgrade rules
- `black`: Code formatting
- `mypy`: Type checking (strict mode)
- `pylint`: Code smells (NFR42)

**Given** inline documentation  
**When** complex logic exists  
**Then** comments explain:
- Why (not what - code is self-documenting)
- Algorithmic complexity
- Edge cases handled
- TODOs with ticket references

**Given** architectural decisions  
**When** made  
**Then** ADRs (Architecture Decision Records) are created  
**And** stored in `docs/adr/`

**Definition of Done:**
- [ ] Comprehensive README and documentation
- [ ] API docs auto-generated (OpenAPI)
- [ ] Code standards documented (CONTRIBUTING.md)
- [ ] Docstrings for all public APIs (NFR35)
- [ ] Type hints throughout (NFR34)
- [ ] Clean architecture enforced (NFR36, NFR37)
- [ ] No code smells (NFR42)
- [ ] ADRs for major decisions

**NFR Coverage:** NFR33-NFR42 (Code quality: type hints, docstrings, clean architecture, SOLID, error handling, idiomatic code, logging, no code smells)  
**Estimated Effort:** 12-16 hours

---

#### Story 5.10: Deployment and Scalability Testing

**As a** DevOps engineer  
**I want** to validate deployment and scalability  
**So that** system is production-ready (NFR30-NFR32)

**Acceptance Criteria:**

**Given** I am testing deployment  
**When** I deploy to production-like environment  
**Then** the following is validated:
- Docker/containerization works
- Environment configuration (via .env)
- Database migrations run successfully
- Services start and pass health checks

**Given** horizontal scaling requirement (NFR30)  
**When** multiple π instances are deployed  
**Then** they:
- Share database (stateless services)
- Handle load balancing correctly
- Don't conflict (no race conditions)

**Given** multiple edge devices (NFR31)  
**When** connected to single π instance  
**Then** π handles:
- Concurrent event ingestion from 10+ edges
- Multi-tenant isolation (no data leakage)
- Cache generation for all tenants

**Given** cache generation efficiency (NFR32)  
**When** domain-filtered cache is generated  
**Then** it:
- Includes only relevant domain data
- Completes in <10 seconds for 1000 products
- Output size optimized (≤100MB)

**Given** load testing  
**When** simulated peak load is applied  
**Then** system handles:
- 100 concurrent edge requests (NFR30)
- 1000 events/min ingestion
- 10 simultaneous cache syncs
- Without degradation (latency within targets)

**Given** deployment documentation  
**When** created  
**Then** it includes:
- Infrastructure requirements (CPU, RAM, storage)
- Deployment steps (Docker, Kubernetes, bare metal)
- Scaling guidelines (when to add instances)
- Monitoring and alerting setup

**Definition of Done:**
- [ ] Containerization (Docker) configured
- [ ] Horizontal scaling validated (NFR30)
- [ ] Multi-edge support tested (NFR31)
- [ ] Cache generation optimized (NFR32)
- [ ] Load testing passed (peak scenarios)
- [ ] Deployment documentation complete

**NFR Coverage:** NFR30-NFR32 (Scalability), NFR12 (System uptime in production)  
**Estimated Effort:** 10-12 hours

---

**Epic 5 Total Estimated Effort:** 112-140 hours  
**Epic 5 Total NFRs Covered:** All 47 NFRs (NFR1-NFR47)

---

## Summary

### Epic Overview

| Epic | Description | Stories | Effort (hrs) | FRs | NFRs |
|------|-------------|---------|--------------|-----|------|
| **Epic 1** | Core Edge Engine | 6 | 20-31 | 4 | - |
| **Epic 2** | Human Interface Layer | 9 | 54-72 | 12 | - |
| **Epic 3** | π Intelligence Layer | 10 | 77-96 | 10 | - |
| **Epic 4** | Edge-π Sync | 4 | 34-42 | 4 | - |
| **Epic 5** | Production Readiness | 10 | 112-140 | - | 47 |
| **TOTAL** | | **39 stories** | **297-381 hrs** | **30 FRs** | **47 NFRs** |

### Implementation Order

1. **Epic 1** (Foundation): HTTP API + cache → Proves edge architecture
2. **Epic 2** (Human Layer): Voice + gestures + LLM → Complete robot experience
3. **Epic 3** (Intelligence): Classification + memory → π brain operational
4. **Epic 4** (Sync): Edge ↔ π connection → Distributed architecture live
5. **Epic 5** (Quality): Throughout + final hardening → Production-ready

### All Requirements Covered

**Functional Requirements:** 30/30 (100%)  
**Non-Functional Requirements:** 47/47 (100%)

✅ All FRs mapped to specific stories  
✅ All NFRs addressed in Epic 5 (quality across all epics)  
✅ No forward dependencies in epic structure  
✅ Each epic delivers standalone value  
✅ Implementation is testable at each stage

---

**Document Status:** ✅ Complete - Ready for Implementation  
**Next Step:** Begin Epic 1, Story 1.1 (FastAPI Project Setup)

