# 🤖 π (Pi) Universal Second Brain - Reachy Mini Retail Assistant

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **A domain-agnostic intelligence layer for AI assistants**  
> Initial implementation: Voice-enabled retail assistant with Reachy Mini robot

π transforms unstructured interactions into structured, searchable knowledge using multi-stage classification. Think **Logseq meets RAG meets Zapier** - automatic classification, canonical storage, cross-domain reasoning.

---

## 🎯 What is This?

**Not just a retail assistant. Not just a chatbot. A universal intelligence layer.**

- **Edge Component (Reachy Mini)**: Fast, voice-enabled retail assistant with 2-tier cache architecture
- **π Backend**: Universal classification engine that learns and reasons across domains
- **Domain Plugins**: Configurable YAML-based domain adapters (retail, personal, business, research)

### Initial Use Case: Retail Assistance

- **Voice interaction**: Natural language product search and wayfinding
- **Expressive movements**: Head nodding, body rotation, motorized antenna gestures
- **Promotion awareness**: Active deal recommendations
- **Fast responses**: <2s end-to-end, <100ms cache lookups
- **Offline-capable**: Full functionality without backend (cache-only mode)

> **Note**: Reachy Mini is a desktop robot with a 6-DoF head, rotating body, and LED antennas - **no arms or physical manipulation**. See [REACHY-MINI-HARDWARE.md](docs/REACHY-MINI-HARDWARE.md) for full capabilities.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- FastAPI 0.109+
- SQLite 3 (included with Python)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/chelleboyer/reachy_mini_retail_assistant.git
   cd reachy-mini-retail-assistant
   ```

2. **Set up virtual environment**
   ```bash
   cd reachy_edge
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Verify health endpoint**
   ```bash
   curl http://localhost:8000/health
   ```

   Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2026-01-10T12:34:56.789Z",
     "version": "0.1.0"
   }
   ```

---

## 🧪 Testing

Run the test suite:

```bash
cd reachy_edge
python -m pytest tests/ -v
```

Run specific test file:

```bash
python -m pytest tests/test_main.py -v
python -m pytest tests/test_l2_cache.py -v
```

**Current Test Coverage:**
- ✅ Health endpoint (200 status, correct schema, ISO 8601 timestamp, version)
- ✅ FastAPI application startup
- ✅ L2 cache (SQLite FTS5 product search) - 97% coverage, 17/17 tests passing
- 🚧 LLM integration tests (in progress)

---

## 💾 L2 Cache - Product Storage & Search

### Overview

The L2 cache uses **SQLite FTS5** (Full-Text Search 5) for fast, persistent product storage with relevance ranking.

**Features:**
- **Full-text search** across SKU, name, category, location, and description
- **BM25 ranking** for relevance-scored results
- **Porter stemming** for better search quality (e.g., "truck" matches "trucker")
- **Fast performance**: <100ms search latency (NFR4)
- **Truck stop products**: 44 realistic products across 8 categories

### Database Schema

```sql
CREATE VIRTUAL TABLE products_fts USING fts5(
    sku,              -- Product SKU (searchable)
    name,             -- Product name (searchable)
    category,         -- Product category (searchable)
    location,         -- Store location (searchable)
    price UNINDEXED,  -- Price in USD (not searchable)
    description,      -- Full description (searchable)
    tokenize='porter unicode61'  -- Stemming & Unicode support
);
```

### Product Categories

- **Fuel & Fluids**: Diesel, DEF, motor oil, coolant, windshield washer
- **Trucker Supplies**: Logbooks, straps, bungee cords, mud flaps, chains
- **Electronics**: CB radios, GPS units, dash cams, phone chargers, headsets
- **Energy & Snacks**: Coffee, energy drinks, beef jerky, trail mix, protein bars
- **Hot Food**: Pizza, burgers, chicken tenders, breakfast sandwiches
- **Services**: Showers, laundry, truck wash, reserved parking
- **Safety & Lighting**: LED flares, safety vests, flashlights, emergency kits
- **Convenience**: Sunglasses, hygiene products, OTC meds, oral care

### Loading Sample Data

```bash
cd reachy_edge
python scripts/load_products.py

# Or specify custom database path
python scripts/load_products.py --db-path ./custom/path/products.db
```

Expected output:
```
✅ Successfully loaded 44 products into ./data/cache.db

Test query example:
  Results for 'diesel': 5 products
```

### FTS5 Query Examples

```python
from cache.l2_cache import ProductCache

cache = ProductCache()
cache.initialize()

# Single-word search
results = cache.search_products("diesel", max_results=5)
# Returns: Premium Diesel Fuel, BlueDEF, Shell Rotella Oil, etc.

# Multi-word search (AND query)
results = cache.search_products("CB radio")
# Returns: Cobra 29 LX CB Radio

# Category search
results = cache.search_products("electronics")
# Returns: CB radios, GPS units, dash cams, chargers, headsets

# Service search
results = cache.search_products("shower")
# Returns: Shower Credit - 30 Minutes

# Description keyword search
results = cache.search_products("DOT compliant")
# Returns: Simplified Logbook for Truck Drivers

# Phrase search (exact match)
results = cache.search_products('"truck stop"')
# Returns: Products with exact phrase "truck stop"
```

### Python API

```python
from cache.l2_cache import ProductCache
from models import Product

# Initialize cache
cache = ProductCache(db_path="./data/cache.db")
cache.initialize()

# Insert single product
product = Product(
    sku="FUEL-DIESEL-001",
    name="Premium Diesel Fuel",
    category="Fuel & Fluids",
    location="Fuel Island 1",
    price=3.89,
    description="Ultra-low sulfur diesel"
)
cache.insert_product(product)

# Bulk insert
products = [product1, product2, product3]
cache.insert_products(products)

# Search with relevance scores
results = cache.search_products("diesel fuel", max_results=5)
for result in results:
    print(f"{result.name} - ${result.price} - Score: {result.relevance_score}")

# Close connection when done
cache.close()

# Or use context manager (auto-close)
with ProductCache() as cache:
    cache.initialize()
    results = cache.search_products("CB radio")
```

---

## 📁 Project Structure

```
reachy-mini-retail-assistant/
├── reachy_edge/              # Edge component (FastAPI backend)
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Environment-based configuration
│   ├── models/               # Pydantic data models
│   │   ├── __init__.py       # HealthResponse, API schemas
│   │   ├── events.py         # Event models for π backend
│   │   └── interaction.py    # Interaction state models
│   ├── cache/                # 2-tier cache system
│   │   ├── l1_cache.py       # L1: In-memory LRU cache
│   │   ├── l2_cache.py       # L2: SQLite FTS5 cache
│   │   └── schemas.py        # Cache data schemas
│   ├── llm/                  # LLM integration
│   │   ├── inference.py      # LLM inference with caching
│   │   └── prompt_manager.py # Cache-only prompt templates
│   ├── tools/                # Assistant tools
│   │   ├── product_lookup.py # Product search by name/SKU
│   │   ├── promo_manager.py  # Active promotions
│   │   ├── movement.py       # Head/body orientation, antenna control
│   │   └── selfie.py         # Optional engagement
│   ├── pi_client/            # π backend integration
│   │   └── event_emitter.py  # Async event emission
│   ├── tests/                # Test suite
│   │   ├── test_main.py      # Health endpoint tests
│   │   ├── test_cache.py     # Cache layer tests
│   │   └── test_tools.py     # Tool integration tests
│   └── requirements.txt      # Python dependencies
│
├── pi_space/                 # π Universal Backend (future)
│   ├── app.py                # Classification pipeline
│   └── README_HF.md          # Hugging Face deployment guide
│
├── docs/                     # Documentation
│   ├── PRD.md                # Product Requirements Document
│   ├── UNIVERSAL-ARCHITECTURE.md  # System architecture
│   ├── deployment-architecture.md # Deployment guide
│   └── success-metrics.md    # KPIs and measurement
│
├── _bmad-output/             # Planning artifacts
│   ├── planning-artifacts/
│   │   ├── epics.md          # 5 epics, 39 stories
│   │   ├── sprint-status.yaml # Sprint tracking
│   │   └── test-design-system.md # Test strategy
│   └── implementation-artifacts/
│       └── stories/          # Detailed story files
│
└── _bmad/                    # BMAD workflow framework
    ├── bmm/                  # Build-Measure-Method workflows
    └── cis/                  # Creative Innovation Suite
```

---

## 📊 Development Status

**Phase**: Sprint 1 - Epic 1 (Core Edge Engine)

| Epic | Stories | Status | Description |
|------|---------|--------|-------------|
| **Epic 1: Core Edge Engine** | 6 | 🟡 In Progress | Minimal viable edge with 2-tier cache |
| Epic 2: Human Interface Layer | 9 | ⚪ Planned | Voice, gestures, LLM integration |
| Epic 3: π Intelligence Layer | 10 | ⚪ Planned | Classification engine, canonical storage |
| Epic 4: Integration & Deployment | 8 | ⚪ Planned | Sync protocol, monitoring, deployment |
| Epic 5: Enhancement & Scale | 6 | ⚪ Planned | Analytics, multi-store, plugins |

**Current Story**: [Story 1.1 - FastAPI Project Setup](/_bmad-output/implementation-artifacts/stories/1-1-fastapi-project-setup-with-basic-health-endpoint.md) ✅ **COMPLETE**

**Next Story**: Story 1.2 - L2 Cache (SQLite FTS5 Product Storage)

---

## 🏗️ Architecture Overview

### Edge Component (Reachy Mini)

**2-Tier Cache Architecture:**
- **L1 Cache**: In-memory LRU (≤1MB) - Hot products, active promos (99.9% hit rate target)
- **L2 Cache**: SQLite FTS5 (≤100MB) - Full product catalog, store config (<100ms lookup)

**Design Principles:**
- **Fast-first**: Cache-only responses, no blocking I/O
- **Offline-capable**: Full functionality without backend
- **Event-driven**: Async π backend integration
- **Testable**: High test coverage, comprehensive NFR validation

### π Backend (Future - Epic 3)

**Multi-Stage Classification Pipeline:**
1. **Domain Classification**: Which domain handles this? (retail, personal, etc.)
2. **Intent Classification**: What action is requested?
3. **Entity Extraction**: What are the key entities?
4. **Canonical Mapping**: Store in universal format
5. **Response Generation**: Context-aware answers

---

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Environment
ENVIRONMENT=development

# API Configuration
API_VERSION=0.1.0
LOG_LEVEL=INFO

# Cache Configuration (Future - Story 1.2+)
L1_CACHE_SIZE_MB=1
L2_CACHE_SIZE_MB=100

# π Backend (Future - Epic 3)
PI_BACKEND_URL=https://api.pi-brain.com
PI_API_KEY=your-api-key-here
```

---

## 🧑‍💻 Development Workflow

This project uses the **BMAD** (Build-Measure-Analyze-Deploy) workflow framework:

1. **Planning Phase**: PRD → Architecture → Epics → Stories
2. **Implementation**: Story-driven development with clear acceptance criteria
3. **Testing**: Unit tests + Integration tests + NFR validation
4. **Review**: Code review + Retrospectives

### Key Workflows

- **Sprint Planning**: Create sprint-status.yaml, plan story sequence
- **Story Creation**: Generate detailed story files with dev notes
- **Implementation**: Dev agent implements story, updates status
- **Code Review**: Fresh context review with adversarial prompts
- **Retrospective**: Capture learnings, update patterns

See [_bmad/bmm/workflows/](_bmad/bmm/workflows/) for detailed workflow guides.

---

## 📈 Non-Functional Requirements (NFRs)

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR1 | Voice interaction end-to-end | <2s | 🚧 Planned |
| NFR2 | LLM response generation | <500ms | 🚧 Planned |
| NFR4 | L2 cache product search | <100ms | 🚧 Story 1.2 |
| NFR5 | L1 cache hot product lookup | <10ms | 🚧 Story 1.4 |
| NFR6 | L1 cache hit rate | 99.9% | 🚧 Story 1.4 |
| NFR8 | Edge device uptime | 99.5% | 🚧 Epic 4 |
| NFR10 | Conversation flow smoothness | <200ms gaps | 🚧 Epic 2 |

---

## 🤝 Contributing

This project is currently in active development. Contributions welcome after Sprint 1 completion.

**How to contribute:**
1. Read [docs/PRD.md](docs/PRD.md) for product context
2. Check [_bmad-output/planning-artifacts/sprint-status.yaml](_bmad-output/planning-artifacts/sprint-status.yaml) for current status
3. Follow BMAD workflow for story-driven development
4. Ensure tests pass and NFRs are validated

---

## 📚 Documentation

- **[Product Requirements Document](docs/PRD.md)**: Full vision, goals, requirements
- **[Architecture](docs/UNIVERSAL-ARCHITECTURE.md)**: System design, patterns, decisions
- **[Epic Breakdown](_bmad-output/planning-artifacts/epics.md)**: All 39 stories with acceptance criteria
- **[Test Design](_bmad-output/planning-artifacts/test-design-system.md)**: Testing strategy, NFR coverage
- **[Story Files](_bmad-output/implementation-artifacts/stories/)**: Detailed implementation guides

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

Built with:
- **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance async web framework
- **[Pydantic](https://pydantic.dev/)**: Data validation and settings management
- **[SQLite FTS5](https://www.sqlite.org/fts5.html)**: Full-text search engine
- **[structlog](https://www.structlog.org/)**: Structured logging
- **[pytest](https://pytest.org/)**: Testing framework

Inspired by:
- **Reachy**: Open-source expressive humanoid robot platform
- **Logseq**: Local-first knowledge management
- **Ray Serve**: Fast model serving
- **Zapier**: Workflow automation

---

## 📧 Contact

- **GitHub**: [@chelleboyer](https://github.com/chelleboyer)
- **Project**: [reachy_mini_retail_assistant](https://github.com/chelleboyer/reachy_mini_retail_assistant)

---

**Status**: 🚧 Sprint 1 in progress - Story 1.1 complete (1/39 stories)  
**Last Updated**: January 10, 2026
