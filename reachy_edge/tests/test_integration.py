"""End-to-End Integration Tests — Story 6

Validates the full pipeline:
    Karen Whisperer tool → HTTP request → API endpoint → FTS5 cache → response

Three test suites:
    1. Happy-path: all 3 API endpoints return valid data
    2. Error-path: graceful behavior on bad input / missing data
    3. Load test: 50 concurrent requests under P95 <200ms

Run with:
    pytest reachy_edge/tests/test_integration.py -v

These tests use FastAPI's TestClient (no live server required).
"""
from __future__ import annotations

import asyncio
import statistics
import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from reachy_edge.main import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """TestClient spins up the ASGI app in-process (lifespan included)."""
    with TestClient(app) as c:
        yield c


# ===================================================================
# SUITE 1 — Happy-path: all 3 API endpoints
# ===================================================================

class TestProductSearchEndpoint:
    """GET /api/products/search — FTS5 product search."""

    def test_search_returns_products(self, client):
        """Basic search returns a non-empty product list."""
        resp = client.get("/api/products/search", params={"q": "diesel"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["result_count"] > 0
        assert len(data["products"]) > 0
        assert data["query"] == "diesel"

    def test_search_product_has_required_fields(self, client):
        """Every product result has sku, name, category, location, price."""
        resp = client.get("/api/products/search", params={"q": "diesel"})
        product = resp.json()["products"][0]
        for field in ("sku", "name", "category", "location", "price"):
            assert field in product, f"Missing field: {field}"

    def test_search_respects_limit(self, client):
        """Limit parameter caps the number of results."""
        resp = client.get("/api/products/search", params={"q": "energy", "limit": 2})
        assert resp.status_code == 200
        assert len(resp.json()["products"]) <= 2

    def test_search_returns_search_time(self, client):
        """Response includes search_time_ms metric."""
        resp = client.get("/api/products/search", params={"q": "coffee"})
        data = resp.json()
        assert "search_time_ms" in data
        assert isinstance(data["search_time_ms"], (int, float))

    def test_search_no_results_for_gibberish(self, client):
        """Gibberish query returns zero results, not an error."""
        resp = client.get("/api/products/search", params={"q": "xyzzy999qqq"})
        assert resp.status_code == 200
        assert resp.json()["result_count"] == 0

    def test_search_empty_query_rejected(self, client):
        """Empty query string is rejected with 422."""
        resp = client.get("/api/products/search", params={"q": ""})
        assert resp.status_code == 422

    def test_search_missing_query_rejected(self, client):
        """Missing q parameter is rejected with 422."""
        resp = client.get("/api/products/search")
        assert resp.status_code == 422

    def test_search_case_insensitive(self, client):
        """Search is case-insensitive (FTS5 default)."""
        upper = client.get("/api/products/search", params={"q": "DIESEL"}).json()
        lower = client.get("/api/products/search", params={"q": "diesel"}).json()
        assert upper["result_count"] == lower["result_count"]

    def test_search_by_category(self, client):
        """Searching by category name returns relevant products."""
        resp = client.get("/api/products/search", params={"q": "Fuel"})
        assert resp.status_code == 200
        assert resp.json()["result_count"] > 0

    def test_search_under_100ms(self, client):
        """Single search completes in <100ms."""
        start = time.time()
        client.get("/api/products/search", params={"q": "jerky"})
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < 100, f"Search took {elapsed_ms:.1f}ms (limit: 100ms)"


# ===================================================================
# SUITE 2 — Promo endpoint
# ===================================================================

class TestPromoEndpoint:
    """GET /api/promos/active — Active promotions."""

    def test_promos_returns_200(self, client):
        """Promos endpoint always returns 200 even with no data."""
        resp = client.get("/api/promos/active")
        assert resp.status_code == 200
        data = resp.json()
        assert "promos" in data
        assert "count" in data
        assert isinstance(data["promos"], list)

    def test_promos_limit_parameter(self, client):
        """Limit parameter is accepted and doesn't error."""
        resp = client.get("/api/promos/active", params={"limit": 1})
        assert resp.status_code == 200

    def test_promos_sku_filter(self, client):
        """SKU filter parameter is accepted (even if no match)."""
        resp = client.get("/api/promos/active", params={"product_sku": "FUEL-DIESEL-001"})
        assert resp.status_code == 200
        assert isinstance(resp.json()["promos"], list)


# ===================================================================
# SUITE 3 — Store info endpoint
# ===================================================================

class TestStoreInfoEndpoint:
    """GET /api/store/info — Store configuration."""

    def test_store_info_returns_200(self, client):
        """Store info endpoint returns 200."""
        resp = client.get("/api/store/info")
        assert resp.status_code == 200

    def test_store_info_has_required_fields(self, client):
        """Response includes all expected store metadata."""
        data = client.get("/api/store/info").json()
        for field in ("store_id", "reachy_id", "name", "hours", "categories",
                       "product_count", "promo_count", "status"):
            assert field in data, f"Missing field: {field}"

    def test_store_info_has_categories(self, client):
        """Store info returns at least one product category."""
        data = client.get("/api/store/info").json()
        assert len(data["categories"]) > 0

    def test_store_info_product_count_matches_loaded_data(self, client):
        """Product count matches the 44 sample products loaded at startup."""
        data = client.get("/api/store/info").json()
        assert data["product_count"] == 44

    def test_store_info_status_is_open(self, client):
        """Store status is 'open'."""
        data = client.get("/api/store/info").json()
        assert data["status"] == "open"


# ===================================================================
# SUITE 4 — Full conversation flow (simulates Karen Whisperer)
# ===================================================================

class TestConversationFlow:
    """Simulate the 3-step flow a KW tool chain would make."""

    def test_full_tool_chain(self, client):
        """Simulate: get_store_info → lookup_product → get_active_promos."""
        # Step 1: get_store_info (bot orients itself)
        store = client.get("/api/store/info").json()
        assert store["status"] == "open"
        assert store["product_count"] > 0

        # Step 2: lookup_product (customer asks "do you have energy drinks?")
        products = client.get(
            "/api/products/search",
            params={"q": "energy drinks", "limit": 3},
        ).json()
        assert products["result_count"] > 0
        first_sku = products["products"][0]["sku"]

        # Step 3: get_active_promos filtered by that SKU
        promos = client.get(
            "/api/promos/active",
            params={"product_sku": first_sku},
        ).json()
        assert isinstance(promos["promos"], list)

    def test_sequential_searches_use_l1_cache(self, client):
        """Repeated identical searches should hit L1 cache."""
        # First call populates L1
        r1 = client.get("/api/products/search", params={"q": "coffee"}).json()
        # Second call should hit L1
        r2 = client.get("/api/products/search", params={"q": "coffee"}).json()
        assert r1["result_count"] == r2["result_count"]
        # L1 hit should be faster — but at minimum, cache_hit flag should be true
        assert r2["cache_hit"] is True


# ===================================================================
# SUITE 5 — Error paths
# ===================================================================

class TestErrorPaths:
    """Verify graceful handling of edge cases and bad input."""

    def test_search_limit_too_high_clamped(self, client):
        """Limit above max (20) is rejected with 422."""
        resp = client.get("/api/products/search", params={"q": "diesel", "limit": 100})
        assert resp.status_code == 422

    def test_search_limit_zero_rejected(self, client):
        """Limit of 0 is rejected with 422."""
        resp = client.get("/api/products/search", params={"q": "diesel", "limit": 0})
        assert resp.status_code == 422

    def test_promo_limit_too_high_rejected(self, client):
        """Promo limit above max (10) is rejected with 422."""
        resp = client.get("/api/promos/active", params={"limit": 50})
        assert resp.status_code == 422

    def test_nonexistent_endpoint_404(self, client):
        """Random endpoint returns 404."""
        resp = client.get("/api/nonexistent")
        assert resp.status_code == 404

    def test_search_special_characters_safe(self, client):
        """Special characters in search don't crash the server."""
        for q in ["'; DROP TABLE--", "<script>", "café", "diesel & gas", "a" * 200]:
            resp = client.get("/api/products/search", params={"q": q})
            assert resp.status_code in (200, 422), f"Failed on query: {q}"


# ===================================================================
# SUITE 6 — Load test: 50 concurrent requests
# ===================================================================

class TestLoadPerformance:
    """Basic load test — 50 concurrent searches, P95 <200ms."""

    def test_50_concurrent_searches(self, client):
        """50 parallel searches complete with P95 latency <200ms and zero errors."""
        n = 50
        queries = [
            "diesel", "coffee", "energy", "jerky", "water",
            "tire", "blanket", "charger", "sunglasses", "candy",
        ]
        latencies: list[float] = []
        errors: list[str] = []

        def single_search(query: str) -> None:
            start = time.time()
            try:
                resp = client.get("/api/products/search", params={"q": query})
                elapsed_ms = (time.time() - start) * 1000
                latencies.append(elapsed_ms)
                if resp.status_code != 200:
                    errors.append(f"{query}: HTTP {resp.status_code}")
            except Exception as exc:
                errors.append(f"{query}: {exc}")

        with ThreadPoolExecutor(max_workers=10) as pool:
            # Fire 50 requests (cycle through 10 queries × 5)
            futures = [pool.submit(single_search, queries[i % len(queries)]) for i in range(n)]
            for f in futures:
                f.result(timeout=10)

        assert len(errors) == 0, f"Errors: {errors}"
        assert len(latencies) == n, f"Only {len(latencies)}/{n} completed"

        p95 = sorted(latencies)[int(n * 0.95) - 1]
        avg = statistics.mean(latencies)
        max_lat = max(latencies)

        print(f"\n  Load test results (n={n}):")
        print(f"  P95: {p95:.1f}ms  |  avg: {avg:.1f}ms  |  max: {max_lat:.1f}ms")

        assert p95 < 200, f"P95 latency {p95:.1f}ms exceeds 200ms limit"
