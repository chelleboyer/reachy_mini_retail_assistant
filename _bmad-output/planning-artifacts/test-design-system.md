# System-Level Test Design - π Universal Second Brain

**Project:** reachy-mini-retail-assistant  
**Assessment Date:** 2026-01-10  
**Test Architect:** Murat (TEA)  
**Phase:** 3 (Solutioning - Testability Review)

---

## Executive Summary

**Overall Testability Assessment:** ✅ **PASS with Recommendations**

The architecture demonstrates strong testability fundamentals with clear separation of concerns, mockable boundaries, and comprehensive NFR requirements. The second brain design (Edge + π) enables independent testing of each layer. Minor recommendations focus on enhancing observability and test data management.

**Gate Check Recommendation:** ✅ **PROCEED** to implementation-readiness

---

## Testability Assessment

### 1. Controllability: ✅ PASS

**Strengths:**
- **Clean Architecture:** Edge and π layers are independently controllable
- **REST API Boundaries:** All interactions via HTTP/JSON enable easy test doubles
- **Domain Plugins:** YAML-based configurations allow test-specific domains without code changes
- **Database Isolation:** SQLite (edge) and PostgreSQL (π) support in-memory/ephemeral instances
- **Cache Layering:** L1 (memory) and L2 (SQLite) caches independently testable
- **Event-Driven:** Async event emission allows test-time event injection

**Testable State Control:**
- Edge cache pre-seeding via direct SQLite inserts
- π canonical storage seeding via API or direct DB
- LLM mocking via dependency injection (OpenAI client configurable)
- Session state control via test fixtures
- Time mocking for TTL/expiry testing (cache, sessions, promos)

**Test Scenarios Enabled:**
```python
# Example: Testable cache scenarios
- Empty cache → cold start
- Seeded L1 → hot path testing
- Corrupted L2 → error handling
- Expired promos → TTL enforcement
- Concurrent cache updates → race condition testing
```

**Recommendations:**
1. **Dependency Injection Framework:** Formalize DI for LLM, STT, TTS, Reachy SDK to enable clean mocking
2. **Test Fixtures:** Create reusable fixtures for common states (empty cache, seeded products, active sessions)
3. **Chaos Engineering Hooks:** Add fault injection API for network failures, DB slowness, LLM timeouts

---

### 2. Observability: ✅ PASS

**Strengths:**
- **Structured Logging:** JSON logs with trace IDs enable test verification
- **Metrics Endpoint:** Prometheus /metrics allows validation of NFR targets
- **Health Endpoints:** Comprehensive status reporting (cache stats, DB health)
- **Classification Explainability:** Confidence scores per stage enable accuracy testing
- **Event Replay System:** Built-in evaluation framework for regression testing

**Observable Test Points:**
```
✓ Cache hit/miss rates (L1, L2)
✓ Classification confidence (per stage)
✓ Latency metrics (P50/P95/P99)
✓ Knowledge graph size (entities, relationships)
✓ Event ingestion throughput
✓ LLM token usage
✓ Error rates per endpoint
```

**Test Verification Examples:**
```python
# Performance test validation
assert metrics['edge_request_duration_p95'] < 1.0  # NFR1
assert metrics['cache_hit_rate_l1'] > 0.9          # NFR19

# Classification accuracy
assert classification['domain_confidence'] >= 0.95  # NFR15
assert classification['intent_confidence'] >= 0.90  # NFR16
```

**Recommendations:**
1. **Test Logging Mode:** Add DEBUG mode that logs cache slices, LLM prompts, classifier decisions
2. **Trace Correlation:** Ensure trace_id propagates Edge → π for end-to-end test tracing
3. **Synthetic Monitoring:** Add canary endpoints for continuous production testing

---

### 3. Reliability: ✅ PASS

**Strengths:**
- **Stateless Services:** Edge and π services are stateless, enabling parallel test execution
- **Idempotent APIs:** Event ingestion with deduplication allows test retry
- **Database Transactions:** Atomic operations prevent partial state in tests
- **Test Isolation:** SQLite in-memory (edge) and ephemeral PostgreSQL (π) for test isolation
- **Retry Logic:** Exponential backoff on failures testable with fault injection
- **Graceful Degradation:** LLM fallback to templates testable by mocking failures

**Test Parallelization:**
- ✅ Unit tests: Fully parallelizable (mocked dependencies)
- ✅ Integration tests: Parallel-safe with isolated databases
- ✅ E2E tests: Parallel-safe if multi-tenant IDs used per test
- ⚠️ Performance tests: Serial execution required (resource contention)

**Test Reproducibility:**
```python
# Deterministic test patterns
- Fixed seed data (same products, promos every run)
- Mocked time (freezegun for TTL testing)
- Mocked randomness (classification fallback order)
- Recorded LLM responses (VCR.py for API mocking)
```

**Recommendations:**
1. **Database Cleanup Hooks:** Ensure teardown cleans test tenants (no cross-test pollution)
2. **Async Test Helpers:** Provide awaitable helpers for event emission verification
3. **Flake Detection:** Add CI flake detection (rerun failures 3x) to catch non-determinism

---

## Architecturally Significant Requirements (ASRs)

Risk-scored quality requirements that drive testing strategy:

| ID | Requirement | Category | Probability | Impact | Risk Score | Test Approach |
|-----|-------------|----------|-------------|--------|------------|---------------|
| NFR1 | P95 interaction <1s | PERF | High | High | **9** | Load testing (k6), P95 assertions, caching validation |
| NFR2 | Fast path <500ms | PERF | High | High | **9** | Cache hit testing, latency benchmarks |
| NFR15 | ≥95% domain accuracy | BUS | Medium | High | **6** | Classification eval suite, confusion matrix |
| NFR16 | ≥90% intent accuracy | BUS | Medium | High | **6** | Ground truth dataset, replay testing |
| NFR19 | ≥90% cache hit rate | PERF | Medium | Medium | **4** | Cache analytics, access pattern testing |
| NFR25 | No PII storage | SEC | Low | Critical | **6** | Security scans, log inspection, PII detector |
| NFR26 | No image storage | SEC | Low | High | **3** | Filesystem monitoring, API audits |
| NFR39 | ≥80% test coverage | OPS | Medium | Medium | **4** | Coverage gates in CI, branch coverage |
| NFR9 | ≥99% crash-free | OPS | Medium | High | **6** | Chaos testing, error rate monitoring |
| NFR30 | Horizontal scaling | TECH | Medium | Medium | **4** | Multi-instance load tests, stateless validation |

**Risk Categories:**
- **PERF (Performance):** 3 ASRs - Primary testing focus
- **BUS (Business):** 2 ASRs - Classification accuracy critical
- **SEC (Security):** 2 ASRs - Privacy compliance required
- **OPS (Operations):** 2 ASRs - Reliability and maintainability
- **TECH (Technical):** 1 ASR - Scalability validation

---

## Test Levels Strategy

### Recommended Distribution

**API-Heavy + Multi-Service Architecture → 60/25/15 Split**

| Test Level | % Effort | Rationale | Key Focus |
|------------|----------|-----------|-----------|
| **Unit** | 60% | Core logic (cache, classifier, tools, FSM) independent of I/O | Cache algorithms, entity deduplication, knowledge graph queries, FSM transitions |
| **Integration** | 25% | API contracts, database operations, multi-stage pipeline | /interact, /events/ingest, /cache/sync endpoints, classification pipeline, sync protocol |
| **E2E** | 15% | Critical user flows, edge-to-π synchronization | Wayfinding flow (voice → cache → response → gesture), cache sync, event ingestion |

### Test Level Details

#### Unit Tests (60% - ~178-229 hours)

**Scope:**
- Cache algorithms (LRU eviction, TTL enforcement)
- FTS5 query building (search term sanitization)
- Product lookup tool (ranking, filtering)
- Classification stages (domain, intent, entity, canonical, response)
- Entity deduplication logic
- Knowledge graph queries (relationship traversal)
- FSM state transitions (all states, all transitions)
- Promo manager (date filtering, discount sorting)
- Reasoning engine (entity resolution, context loading)

**Tools:**
- `pytest` with `pytest-cov` (≥80% coverage)
- `unittest.mock` for I/O mocking
- `freezegun` for time mocking
- `pytest-asyncio` for async code
- `pytest-xdist` for parallel execution

**Example Unit Test:**
```python
def test_l1_cache_eviction_lru():
    """NFR17: L1 cache evicts least recently used when full"""
    cache = ProductCache(max_size=3)
    cache.set("apple", product_apple)
    cache.set("banana", product_banana)
    cache.set("carrot", product_carrot)
    
    cache.get("apple")  # Access apple (most recent)
    cache.set("donut", product_donut)  # Triggers eviction
    
    assert cache.get("banana") is None  # LRU evicted
    assert cache.get("apple") is not None
    assert len(cache) == 3  # Size limit enforced
```

---

#### Integration Tests (25% - ~74-95 hours)

**Scope:**
- API endpoints with real databases (SQLite, PostgreSQL in-memory)
- Edge → π event emission and ingestion
- Cache generation and sync protocol
- Classification pipeline with all 5 stages
- Multi-tenant data isolation
- Feed adapters (product, promo CSV/JSON ingestion)

**Tools:**
- `pytest` with FastAPI `TestClient`
- Docker Compose for test databases
- `httpx` for async API testing
- `testcontainers` for PostgreSQL (optional)

**Example Integration Test:**
```python
@pytest.mark.integration
async def test_interact_endpoint_cache_hierarchy(test_client, seeded_db):
    """NFR2: Fast path <500ms with cache"""
    response = await test_client.post(
        "/interact",
        json={"query": "where are apples"}
    )
    
    assert response.status_code == 200
    assert response.json()["latency_ms"] < 500  # NFR2
    assert "Aisle 3" in response.json()["response"]
    assert response.json()["cache_hit"] is True
```

---

#### E2E Tests (15% - ~45-57 hours)

**Scope:**
- Complete user flows (greeting → wayfinding → farewell)
- Voice input → LLM → gesture coordination
- Edge cache sync → event emission → π ingestion
- Multi-stage classification → canonical storage → knowledge graph
- Deal promotion flow (proactive engagement)
- Clarification flow (ambiguous query handling)

**Tools:**
- Playwright (if web UI exists for π demo)
- Custom test harness for Reachy robot (mocked hardware)
- `pytest` with scenario-based fixtures

**Example E2E Test:**
```python
@pytest.mark.e2e
async def test_wayfinding_flow_with_gesture(edge_client, pi_client):
    """FR28: Complete wayfinding flow from query to gesture"""
    # 1. Customer query via edge
    response = await edge_client.post(
        "/interact",
        json={"query": "where are organic apples", "session_id": "test-session-1"}
    )
    
    # 2. Verify response
    assert "Aisle 3" in response.json()["response"]
    assert response.json()["gesture_action"] == "point_left"
    
    # 3. Verify event emitted to π (async)
    await asyncio.sleep(1)  # Wait for event emission
    events = await pi_client.get("/events?session_id=test-session-1")
    
    # 4. Verify π classification
    assert events[0]["domain"] == "retail"
    assert events[0]["intent"] == "product_location"
    assert events[0]["entities"][0]["value"] == "organic apples"
```

---

## NFR Testing Approach

### 1. Security (NFR25-NFR29, NFR44)

**Testing Strategy:**

| NFR | Requirement | Test Approach | Tools |
|-----|-------------|---------------|-------|
| NFR25 | No PII storage | Log inspection, DB scans for PII patterns | `presidio`, custom regex |
| NFR26 | No image storage | Filesystem monitoring after selfie flow | `pytest` with temp dir |
| NFR27 | Append-only logs | DB integrity checks, no UPDATE/DELETE | SQL query audits |
| NFR28 | Full trace logging | Trace ID coverage in all logs | Log parser assertions |
| NFR29 | Multi-tenant isolation | Cross-tenant access attempts (negative tests) | Integration tests |
| NFR44 | Input validation | Fuzzing, SQL injection, XSS attempts | `hypothesis`, Pydantic validation tests |

**Security Test Examples:**
```python
def test_no_pii_in_logs(caplog):
    """NFR25: Logs must not contain PII"""
    process_query("my email is user@example.com")
    
    for record in caplog.records:
        assert "user@example.com" not in record.message
        assert "<EMAIL_REDACTED>" in record.message  # Expect redaction

def test_sql_injection_prevention():
    """NFR44: Parameterized queries prevent SQL injection"""
    malicious_query = "'; DROP TABLE products; --"
    response = client.post("/interact", json={"query": malicious_query})
    
    assert response.status_code == 200  # Request succeeds
    assert db.table_exists("products")  # Table not dropped
```

---

### 2. Performance (NFR1-NFR8, NFR45)

**Testing Strategy:**

| NFR | SLO | Test Type | Tool | Validation |
|-----|-----|-----------|------|------------|
| NFR1 | P95 <1s | Load test | k6 | P95 latency assertion |
| NFR2 | Fast path <500ms | Benchmark | pytest-benchmark | Cache-only queries |
| NFR3 | L1 hit <10ms | Unit | pytest | Mocked cache timing |
| NFR4 | L2 query <100ms | Integration | pytest | SQLite FTS5 timing |
| NFR5 | π class <200ms | Integration | pytest | Cached pattern timing |
| NFR6 | Sync <5s | Integration | pytest | Full sync cycle |
| NFR7 | Graph query <100ms | Unit | pytest | Relationship queries |
| NFR8 | Cached pattern <100ms | Integration | pytest | Classification cache hit |

**Load Testing Setup (k6):**
```javascript
// load-test-edge.js
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 50 },  // Ramp up
    { duration: '5m', target: 100 }, // Sustained load (NFR30)
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    'http_req_duration{p(95)}': ['value<1000'], // NFR1: P95 <1s
    'http_req_duration{p(50)}': ['value<500'],  // NFR2: P50 <500ms
  },
};

export default function() {
  let response = http.post('http://edge:8000/interact', 
    JSON.stringify({query: 'where are apples'}),
    {headers: {'Content-Type': 'application/json'}}
  );
  
  check(response, {
    'status 200': (r) => r.status === 200,
    'has response': (r) => r.json('response') !== undefined,
  });
}
```

---

### 3. Reliability (NFR9-NFR14, NFR38)

**Testing Strategy:**

| NFR | Requirement | Test Approach | Implementation |
|-----|-------------|---------------|----------------|
| NFR9 | ≥99% crash-free | Chaos testing, error injection | Pytest with fault injection fixtures |
| NFR10 | <1% unhandled errors | Exception coverage, error rate metrics | Sentry integration + assertions |
| NFR11 | Zero data corruption | Transaction rollback tests, DB integrity | SQLite PRAGMA checks |
| NFR12 | ≥99.5% uptime | Health check monitoring, recovery tests | Synthetic monitoring |
| NFR13 | Graceful degradation | Network failure scenarios | pytest with mocked failures |
| NFR14 | Offline cache usage | Disconnect π, verify edge works | Integration test |
| NFR38 | No silent failures | Log inspection, exception propagation | All exceptions logged + raised |

**Chaos Testing Example:**
```python
@pytest.mark.chaos
def test_graceful_degradation_llm_failure(edge_client, mock_llm_down):
    """NFR13: Edge degrades gracefully when LLM unavailable"""
    response = edge_client.post("/interact", json={"query": "where are apples"})
    
    assert response.status_code == 200  # Still responds
    assert response.json()["fallback_used"] is True  # Template response
    assert "Aisle 3" in response.json()["response"]  # Correct answer
    assert metrics["llm_failures_total"] == 1  # Metric incremented
```

---

### 4. Maintainability (NFR33-NFR43, NFR46-NFR47)

**Testing Strategy:**

| NFR | Requirement | Validation Approach | Enforcement |
|-----|-------------|---------------------|-------------|
| NFR33 | Production-grade code | Code review checklist | PR template |
| NFR34 | Type hints (3.11+) | mypy strict mode | CI gate |
| NFR35 | Full docstrings | pydocstyle | CI gate |
| NFR36 | Clean architecture | Layer dependency tests | pytest-archon |
| NFR37 | SOLID principles | Complexity metrics | radon, pylint |
| NFR38 | Error handling | Exception coverage | Unit tests |
| NFR39 | ≥80% coverage | pytest-cov | CI gate (blocks merge) |
| NFR40 | Integration tests | API endpoint coverage | CI runs |
| NFR41 | Idiomatic code | Linter compliance | ruff, black |
| NFR42 | No code smells | Static analysis | pylint, sonarqube |
| NFR43 | Structured logging | Log format validation | Unit tests |
| NFR46 | Code reviews required | Branch protection | GitHub settings |
| NFR47 | CI/CD with gates | Pipeline definition | GitHub Actions |

**CI Pipeline Quality Gates:**
```yaml
# .github/workflows/ci.yml (excerpt)
- name: Type Check
  run: mypy . --strict
  
- name: Lint
  run: |
    ruff check .
    black --check .
    pylint src/
    
- name: Test with Coverage
  run: |
    pytest --cov=src --cov-report=term --cov-fail-under=80
    
- name: Security Scan
  run: |
    bandit -r src/
    safety check
```

---

## Test Environment Requirements

### Development Environment

**Local Testing:**
- Python 3.11+
- SQLite 3.35+ (FTS5 support)
- Docker (for PostgreSQL in integration tests)
- OpenAI API key (for LLM tests) OR mocked responses

**Hardware:**
- Reachy SDK (mocked for unit/integration, real for E2E if available)
- Microphone/speakers (mocked for voice tests)
- Camera (mocked for selfie tests)

### CI/CD Environment

**GitHub Actions (or equivalent):**
- Ubuntu 22.04 runners
- Python 3.11 pre-installed
- Docker available for testcontainers
- Secrets: OpenAI API key (test tier)
- PostgreSQL service container (integration tests)

### Staging Environment

**Infrastructure:**
- Edge: Raspberry Pi 5 (4GB RAM) OR equivalent VM
- π Backend: Cloud VM (2 vCPU, 4GB RAM minimum)
- PostgreSQL: Managed instance (AWS RDS, Supabase, etc.)
- Monitoring: Prometheus + Grafana

**Test Data:**
- 100-500 products (realistic retail inventory subset)
- 10-20 active promos
- 5-10 test sessions with interaction history

### Production-Like Testing

**Load Testing Environment:**
- Scaled-down production clone (50% capacity)
- 1000 products, 50 promos (representative dataset)
- k6 load generator (separate VM)
- Metrics collection enabled

---

## Testability Concerns

### ⚠️ Minor Concerns (Non-Blocking)

1. **Hardware Mocking Complexity**
   - **Issue:** Reachy robot SDK (gestures, camera) requires hardware or complex mocking
   - **Impact:** E2E tests may be harder to run in CI without real hardware
   - **Mitigation:** Create `MockReachySDK` with recorded gesture sequences
   - **Risk Score:** 2 (Low probability, Low impact)

2. **Voice I/O Testing**
   - **Issue:** STT/TTS testing requires audio fixtures or service mocking
   - **Impact:** Voice flow E2E tests need pre-recorded audio samples
   - **Mitigation:** Use VCR.py for Google STT/TTS API mocking
   - **Risk Score:** 2 (Low probability, Low impact)

3. **LLM Non-Determinism**
   - **Issue:** OpenAI responses may vary between test runs
   - **Impact:** Response text assertions may be brittle
   - **Mitigation:** Use VCR.py for recorded responses OR assert response patterns (not exact text)
   - **Risk Score:** 3 (Medium probability, Low impact)

4. **Multi-Tenant Test Isolation**
   - **Issue:** Parallel tests need unique tenant_ids to avoid data leakage
   - **Impact:** Test setup complexity increases
   - **Mitigation:** UUID-based tenant IDs per test, cleanup hooks
   - **Risk Score:** 2 (Low probability, Low impact)

### ✅ No Blocking Concerns

Architecture is testable without significant refactoring. All concerns are addressable with standard mocking patterns and test infrastructure.

---

## Recommendations for Sprint 0

**Before first story implementation, set up testing foundation:**

### 1. Test Framework Setup (Story 5.1 dependencies)

**Actions:**
- [ ] Configure `pytest` with coverage (pytest.ini, .coveragerc)
- [ ] Set up `pytest-asyncio` for async tests
- [ ] Install `freezegun` for time mocking
- [ ] Install `pytest-xdist` for parallel execution
- [ ] Create `tests/unit/`, `tests/integration/`, `tests/e2e/` structure
- [ ] Add `conftest.py` with shared fixtures

**Deliverable:** Test infrastructure ready for TDD

---

### 2. Mock Infrastructure (Epic 1-2 enablers)

**Actions:**
- [ ] Create `MockLLMClient` (OpenAI API mock with VCR.py)
- [ ] Create `MockReachySDK` (gesture, camera stubs)
- [ ] Create `MockSTT` / `MockTTS` (audio I/O stubs)
- [ ] Create test fixtures for cache seeding (`@pytest.fixture def seeded_cache`)
- [ ] Create test fixtures for database seeding (`@pytest.fixture def test_db`)

**Deliverable:** Reusable mocks for all external dependencies

---

### 3. CI Pipeline (Story 5.8)

**Actions:**
- [ ] Create `.github/workflows/ci.yml`
- [ ] Add quality gates: mypy, ruff, black, pytest with coverage
- [ ] Configure branch protection (require tests to pass, 1 approval)
- [ ] Add coverage reporting (comment on PRs with coverage delta)
- [ ] Add security scanning (bandit, safety)

**Deliverable:** Automated testing on every PR

---

### 4. Load Testing Setup (Story 5.5)

**Actions:**
- [ ] Install k6 in CI/staging
- [ ] Create `load-test-edge.js` script (100 concurrent users)
- [ ] Create `load-test-pi.js` script (1000 events/min ingestion)
- [ ] Set up Prometheus scraping in staging
- [ ] Create Grafana dashboard for load test visualization

**Deliverable:** Performance testing infrastructure

---

### 5. Test Data Management

**Actions:**
- [ ] Create `tests/fixtures/products.json` (sample 50 products)
- [ ] Create `tests/fixtures/promos.json` (sample 10 promos)
- [ ] Create seed script: `python -m tests.seed_data`
- [ ] Document test data requirements per epic

**Deliverable:** Consistent test data across all test levels

---

## Appendix: Test Coverage Targets by Epic

| Epic | Unit | Integration | E2E | Total Effort |
|------|------|-------------|-----|--------------|
| Epic 1 (Core Edge) | 15 hrs | 5 hrs | 3 hrs | 23 hrs (NFR39 compliance) |
| Epic 2 (Human Interface) | 35 hrs | 15 hrs | 10 hrs | 60 hrs (NFR39 compliance) |
| Epic 3 (π Intelligence) | 50 hrs | 20 hrs | 10 hrs | 80 hrs (NFR39 compliance) |
| Epic 4 (Edge-π Sync) | 20 hrs | 10 hrs | 5 hrs | 35 hrs (NFR39 compliance) |
| Epic 5 (Prod Readiness) | Already included in Epic 1-4 | - | - | - |

**Note:** Epic 5 stories (5.1-5.10) distribute testing effort across Epic 1-4 implementation. The totals above already include ≥80% coverage requirements from NFR39.

---

## Summary

**Testability Grade:** ✅ **A** (Excellent)

**Key Strengths:**
- Clean separation of concerns (Edge, π, Storage)
- REST API boundaries enable easy mocking
- Comprehensive observability (logs, metrics, traces)
- Event replay system built-in for regression testing

**Testing Investment:**
- Unit: 178-229 hours (60%)
- Integration: 74-95 hours (25%)
- E2E: 45-57 hours (15%)
- **Total: 297-381 hours** (aligned with Epic 1-4 implementation estimates)

**Gate Check Decision:** ✅ **PROCEED** to implementation-readiness workflow

---

**Next Steps:**
1. Execute **implementation-readiness** workflow (Architect validates all artifacts)
2. Set up Sprint 0 test infrastructure (recommendations above)
3. Begin Epic 1, Story 1.1 with TDD approach

**Test Design Status:** ✅ Complete - Ready for Implementation Gate
