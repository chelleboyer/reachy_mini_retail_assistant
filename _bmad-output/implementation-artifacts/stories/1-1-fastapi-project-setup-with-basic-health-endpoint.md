# Story 1.1: FastAPI Project Setup with Basic Health Endpoint

Status: done

## Story

As a developer,
I want a FastAPI project with proper structure and a health endpoint,
so that we have a solid foundation and can verify the service is running.

## Acceptance Criteria

### AC1: Project Structure Created

**Given** I am setting up the retail edge backend  
**When** I initialize the FastAPI project  
**Then** the following structure exists:
- `reachy_edge/main.py` with FastAPI app instance
- `reachy_edge/config.py` with environment-based configuration
- `reachy_edge/models.py` with Pydantic models
- `reachy_edge/requirements.txt` with dependencies (fastapi, uvicorn, sqlite3, pydantic)
- `reachy_edge/README.md` with setup instructions

### AC2: Health Endpoint Returns Correct Response

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

### AC3: Code Quality Standards Met

**Given** the health endpoint implementation  
**When** I review the code  
**Then** it includes:
- Type hints on all functions
- Docstrings for the health endpoint
- Structured logging (INFO level)
- Clean, idiomatic Python 3.11+

## Tasks / Subtasks

- [x] Task 1: Create project structure (AC1)
  - [x] Create reachy_edge/ directory if not exists
  - [x] Create main.py with FastAPI app instance
  - [x] Create config.py with environment configuration
  - [x] Create models.py with Pydantic base models
  - [x] Create requirements.txt with initial dependencies
  - [x] Create README.md with setup instructions

- [x] Task 2: Implement health endpoint (AC2)
  - [x] Add GET /health route in main.py
  - [x] Return HealthResponse model with status, timestamp, version
  - [x] Test endpoint returns 200 with correct schema

- [x] Task 3: Ensure code quality standards (AC3)
  - [x] Add type hints to all functions
  - [x] Add docstrings (Google or NumPy style)
  - [x] Configure structured logging with INFO level
  - [x] Verify Python 3.11+ idioms used

- [x] Task 4: Documentation and testing
  - [x] Document API endpoint in README.md
  - [x] Add example curl command to test health endpoint
  - [x] Create initial test file (tests/test_main.py) with health endpoint test
  - [x] Commit all files to version control

## Dev Notes

### Epic Context

**Epic 1: Core Edge Engine - Minimal Viable Edge**

This is the **foundation story** for the entire edge backend. The goal is to establish the FastAPI project structure with a working health endpoint that proves the service is operational. This story is intentionally minimal - no database, no cache, no business logic yet - just a clean starting point.

**Epic Objectives:**
- Prove the edge architecture works with HTTP + JSON
- Create testable REST API foundation
- Establish code quality standards from the start

**Why This Story First:**
- Smallest possible deliverable that proves the tech stack works
- Establishes project structure conventions for all future stories
- Provides immediate testability (curl/Postman validation)
- Sets quality baseline (type hints, docstrings, logging)

### Architecture Alignment

**From UNIVERSAL-ARCHITECTURE.md:**

**Technology Stack:**
- **Language:** Python 3.11+ (latest stable)
- **Framework:** FastAPI (async, OpenAPI auto-generation)
- **Validation:** Pydantic v2 for request/response models
- **Server:** Uvicorn (ASGI server)

**Key Architectural Principles:**
1. **Type Safety:** Full type hints on all functions (NFR34)
2. **API-First:** RESTful endpoints with OpenAPI docs auto-generated
3. **Observability:** Structured logging from day one (NFR43)
4. **Clean Code:** Idiomatic Python 3.11+, docstrings on public APIs (NFR33-NFR42)

**Edge Layer Characteristics:**
- Runs on Raspberry Pi 5
- FastAPI backend with async/await support
- JSON request/response (no voice/LLM in Epic 1)
- Health endpoint for monitoring (NFR26)
- Foundation for future cache layers (Stories 1.2-1.4)

### Project Structure Standards

**Target File Structure:**
```
reachy_edge/
├── main.py                 # FastAPI app instance and routes
├── config.py               # Environment configuration
├── models.py               # Pydantic models
├── requirements.txt        # Python dependencies
├── README.md               # Setup and usage instructions
├── tests/
│   └── test_main.py        # Health endpoint tests
└── (future: db/, cache/, tools/, fsm/)
```

**Naming Conventions:**
- **Modules:** lowercase with underscores (`reachy_edge`, not `ReachyEdge`)
- **Classes:** PascalCase (`HealthResponse`, `Config`)
- **Functions:** snake_case (`get_health`, `configure_logging`)
- **Constants:** UPPER_SNAKE_CASE (`API_VERSION`, `LOG_LEVEL`)

### Configuration Management

**Environment Variables (config.py):**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_version: str = "0.1.0"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_prefix = "REACHY_EDGE_"  # e.g., REACHY_EDGE_LOG_LEVEL
```

**Why Pydantic Settings:**
- Type-safe configuration with validation
- Environment variable support
- Default values for development
- Easy testing with override

### Health Endpoint Specification

**Route:** `GET /health`

**Response Model:**
```python
from pydantic import BaseModel
from datetime import datetime

class HealthResponse(BaseModel):
    status: str  # "healthy" or "unhealthy"
    timestamp: datetime
    version: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "timestamp": "2026-01-10T12:34:56.789Z",
                "version": "0.1.0"
            }
        }
    }
```

**Implementation Notes:**
- Always return "healthy" in this story (no database checks yet)
- Use `datetime.now(timezone.utc)` for UTC timestamps (ISO 8601)
- Version from config.py Settings
- Log each health check at INFO level with structured data

**Example Structured Log:**
```python
logger.info("health_check", extra={
    "status": "healthy",
    "version": settings.api_version,
    "timestamp": timestamp.isoformat()
})
```

### Dependencies

**requirements.txt (Initial):**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0  # For testing async FastAPI

# Logging
structlog==24.1.0

# Future stories will add: aiosqlite, cachetools, openai, etc.
```

**Version Notes:**
- FastAPI 0.109+: Latest stable with Pydantic v2 support
- Uvicorn with [standard]: Includes websockets, watchfiles for dev
- Pydantic 2.5+: Better performance, new validation API
- structlog: Structured logging for observability (NFR43)

### Logging Configuration

**Structured Logging Pattern:**
```python
import structlog

# Configure in main.py startup
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()
```

**Why Structured Logging Now:**
- NFR43: Proper logging (structured, leveled, contextual)
- Enables trace IDs in future stories
- JSON output for easy parsing/aggregation
- Sets logging standard for all future code

### Testing Standards

**Initial Test Structure (tests/test_main.py):**
```python
import pytest
from fastapi.testclient import TestClient
from reachy_edge.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint_returns_200(client):
    """Test health endpoint returns 200 status code"""
    response = client.get("/health")
    assert response.status_code == 200

def test_health_endpoint_returns_correct_schema(client):
    """Test health endpoint returns correct JSON schema"""
    response = client.get("/health")
    data = response.json()
    
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"

def test_health_endpoint_timestamp_is_iso8601(client):
    """Test health endpoint timestamp is valid ISO 8601"""
    from datetime import datetime
    response = client.get("/health")
    data = response.json()
    
    # Should parse without error
    timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
    assert timestamp is not None
```

**Testing Guidelines for This Story:**
- Use TestClient (synchronous) for now (async tests in later stories)
- Test happy path: 200 response, correct schema
- Test data quality: ISO 8601 timestamps, correct version
- Aim for ≥80% coverage (NFR39) - achievable with 3-4 tests

### README.md Template

**Content to Include:**
```markdown
# Reachy Edge - Retail Assistant Backend

FastAPI backend for Reachy Mini retail assistant robot.

## Setup

1. Install Python 3.11+
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `uvicorn reachy_edge.main:app --reload`

## API Endpoints

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-10T12:34:56.789Z",
  "version": "0.1.0"
}
```

**Test with curl:**
```bash
curl http://localhost:8000/health
```

## Development

- **FastAPI Docs:** http://localhost:8000/docs (Swagger UI)
- **ReDoc:** http://localhost:8000/redoc (Alternative docs)

## Testing

Run tests: `pytest`
Run with coverage: `pytest --cov=reachy_edge --cov-report=html`
```

### Code Quality Checklist

**Before Marking Story as Done:**
- [ ] **Type Hints:** All functions have type annotations (NFR34)
- [ ] **Docstrings:** All public functions have docstrings (NFR35)
- [ ] **Logging:** Structured logging configured and used (NFR43)
- [ ] **Clean Code:** No code smells, follows Python conventions (NFR42)
- [ ] **Testing:** ≥80% test coverage (NFR39)
- [ ] **Documentation:** README.md complete with setup instructions
- [ ] **API Docs:** FastAPI auto-generates OpenAPI docs at /docs
- [ ] **Version Control:** All files committed with clear commit message

### Non-Functional Requirements (NFRs)

**Directly Addressed in This Story:**
- **NFR26:** Health and observability endpoints (GET /health)
- **NFR33:** Python version specified (3.11+)
- **NFR34:** Type hints required on all functions
- **NFR35:** Docstrings for all public APIs
- **NFR39:** Unit test coverage ≥80%
- **NFR42:** No code smells, clean conventions
- **NFR43:** Proper logging (structured, leveled, contextual)

**Foundation for Future Stories:**
- NFR1-NFR8: Performance (health endpoint proves service operational)
- NFR9-NFR14: Reliability (error handling in future stories)
- NFR47: CI/CD with quality gates (Epic 5, Story 5.8)

### Integration Points

**Future Story Dependencies:**
- **Story 1.2:** Will add `reachy_edge/db/products.py` (L2 cache)
- **Story 1.3:** Will add `reachy_edge/tools/product_lookup.py`
- **Story 1.4:** Will add `reachy_edge/cache/lru_cache.py` (L1 cache)
- **Story 1.5:** Will add POST /interact endpoint (uses 1.2-1.4)
- **Story 1.6:** Will enhance GET /health with cache stats (uses 1.4)

**No Backwards Dependencies:**
- This story is completely standalone
- No previous stories to reference
- Clean slate for establishing patterns

### Potential Pitfalls to Avoid

❌ **DON'T:**
- Create database code yet (that's Story 1.2)
- Add caching logic (Stories 1.3-1.4)
- Implement business logic (Story 1.5)
- Over-engineer configuration (keep it simple for now)
- Skip docstrings or type hints (sets bad precedent)
- Use print() for logging (use structlog)

✅ **DO:**
- Keep it minimal - just FastAPI app + health endpoint
- Establish code quality patterns (types, docs, logging)
- Write tests for the health endpoint
- Document setup clearly in README
- Use Pydantic for request/response models
- Configure structured logging from the start

### Example Implementation Snippet

**main.py (Minimal Example):**
```python
"""
Reachy Edge - Retail Assistant Backend

FastAPI application providing REST API for retail edge intelligence.
"""
from datetime import datetime, timezone
from fastapi import FastAPI
from pydantic import BaseModel
import structlog

from reachy_edge.config import Settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()
settings = Settings()

# FastAPI app instance
app = FastAPI(
    title="Reachy Edge API",
    description="Retail assistant edge backend",
    version=settings.api_version
)

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str

@app.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Current service health status
    """
    timestamp = datetime.now(timezone.utc)
    
    logger.info("health_check", extra={
        "status": "healthy",
        "version": settings.api_version
    })
    
    return HealthResponse(
        status="healthy",
        timestamp=timestamp,
        version=settings.api_version
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
```

### References

**Source Documents:**
- [PRD.md](../../docs/PRD.md) - Functional Requirements (FR26)
- [UNIVERSAL-ARCHITECTURE.md](../../docs/UNIVERSAL-ARCHITECTURE.md) - Architecture patterns
- [epics.md](../planning-artifacts/epics.md#story-11-fastapi-project-setup-with-basic-health-endpoint) - Story details
- [implementation-readiness-report-2026-01-10.md](../planning-artifacts/implementation-readiness-report-2026-01-10.md) - Gate check (Grade A+)

**Technology Documentation:**
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/latest/
- structlog: https://www.structlog.org/

**NFR Coverage:**
- NFR26: Health endpoint (this story)
- NFR33-NFR35, NFR39, NFR42-NFR43: Code quality standards

---

## Definition of Done

- [ ] Project structure created with all required files (main.py, config.py, models.py, requirements.txt, README.md)
- [ ] FastAPI app starts successfully with `uvicorn reachy_edge.main:app --reload`
- [ ] GET /health returns 200 with correct JSON schema
- [ ] Code follows NFR33-NFR47 (type hints, docstrings, clean code)
- [ ] README has clear setup and run instructions
- [ ] Tests written with ≥80% coverage
- [ ] Structured logging configured and working
- [ ] FastAPI docs accessible at /docs and /redoc
- [ ] All files committed to version control with descriptive commit message
- [ ] Story marked as "done" in sprint-status.yaml

---

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.5 (2026-01-10)

### Debug Log References

- Health endpoint tested successfully: http://localhost:8000/health
- All tests passed: 5/5 passing in tests/test_main.py
- Response format validated: {"status": "healthy", "timestamp": "2026-01-11T03:20:56.364743Z", "version": "0.1.0"}

### Completion Notes List

1. **Existing Code Refactored**: The reachy_edge project already existed with advanced features (cache, LLM, tools). Refactored health endpoint to match Story 1.1 AC2 requirements.

2. **Health Endpoint Updated**: 
   - Changed from `status: "ok"` to `status: "healthy"`
   - Added `timestamp` field with ISO 8601 format (UTC)
   - Added `version` field from config
   - Removed extra fields (reachy_id, store_id, cache stats, etc.) to match minimal spec
   - Created HealthResponse Pydantic model

3. **Structured Logging Implemented**:
   - Replaced basic logging with structlog
   - Configured JSON renderer with ISO timestamps
   - Added structured log entry in health endpoint

4. **Testing Added**:
   - Created tests/test_main.py with 5 comprehensive tests
   - All tests passing (100% pass rate)
   - Tests cover: status code, schema validation, ISO 8601 format, status value, version

5. **Dependencies Updated**:
   - Added pytest>=7.4.4 and pytest-asyncio>=0.23.3 to requirements.txt
   - Added structlog>=24.1.0 for structured logging
   - All dependencies installed in venv

6. **Configuration Enhanced**:
   - Added api_version = "0.1.0" to Settings class in config.py

### File List

**Modified Files:**
- `reachy_edge/main.py` - Updated health endpoint, added structlog configuration, added HealthResponse import
- `reachy_edge/config.py` - Added api_version field to Settings
- `reachy_edge/models/__init__.py` - Created HealthResponse model with proper docstrings
- `reachy_edge/requirements.txt` - Added pytest, pytest-asyncio, structlog
- `reachy_edge/README.md` - Updated health endpoint documentation with correct response format

**Created Files:**
- `reachy_edge/tests/test_main.py` - Comprehensive health endpoint tests (5 tests, all passing)
