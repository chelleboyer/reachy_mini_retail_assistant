"""Public API routes — the contract Karen Whisperer tools call.

Three clean GET endpoints that wrap existing cache/tool logic:
    GET /api/products/search  — FTS5 product search
    GET /api/promos/active    — Active promotions
    GET /api/store/info       — Store configuration & hours
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

import structlog
from fastapi import APIRouter, Query, Request
from pydantic import BaseModel, Field

from ..mind import mind_bus, MindEvent

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api", tags=["Public API"])


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class ProductResult(BaseModel):
    sku: str
    name: str
    category: str
    location: str
    price: float
    description: str
    relevance_score: Optional[float] = None


class ProductSearchResponse(BaseModel):
    """Response from product search endpoint."""
    products: List[ProductResult]
    query: str
    result_count: int
    search_time_ms: float
    cache_hit: bool


class PromoResult(BaseModel):
    id: str
    description: str
    sku: Optional[str] = None
    category: Optional[str] = None
    discount_percent: Optional[float] = None
    priority: int = 0


class PromoResponse(BaseModel):
    """Response from active promos endpoint."""
    promos: List[PromoResult]
    count: int


class StoreInfoResponse(BaseModel):
    """Response from store info endpoint."""
    store_id: str
    reachy_id: str
    zone_id: str
    name: str
    hours: str
    categories: List[str]
    product_count: int
    promo_count: int
    status: str


# ---------------------------------------------------------------------------
# GET /api/products/search
# ---------------------------------------------------------------------------

@router.get("/products/search", response_model=ProductSearchResponse)
async def search_products(
    request: Request,
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(5, ge=1, le=20, description="Max results"),
):
    """Search products by name, SKU, category, or description.

    Uses FTS5 full-text search with BM25 relevance ranking.
    L1 cache is checked first for repeated queries.
    """
    start = time.time()
    l1 = getattr(request.app.state, "l1_cache", None)
    l2 = getattr(request.app.state, "l2_cache", None)

    cache_key = f"product:{q.lower().strip()}"
    cache_hit = False
    products = []

    # L1 check
    if l1:
        cached = l1.get(cache_key)
        if cached is not None:
            cache_hit = True
            products = cached if isinstance(cached, list) else [cached]

    # L2 FTS5 search
    if not products and l2:
        products = await l2.search_products(q, max_results=limit)
        if products and l1:
            l1.set(cache_key, products)

    search_time_ms = round((time.time() - start) * 1000, 2)

    # Publish to Mind Monitor
    mind_bus.publish_sync(MindEvent(
        type="cache_hit" if cache_hit else "search",
        data={
            "query": q, "result_count": len(products),
            "tier": "L1" if cache_hit else "L2",
            "latency_ms": search_time_ms, "endpoint": "/api/products/search",
        },
    ))

    return ProductSearchResponse(
        products=[
            ProductResult(
                sku=p.sku, name=p.name, category=p.category,
                location=p.location, price=p.price,
                description=p.description,
                relevance_score=getattr(p, "relevance_score", None),
            )
            for p in products[:limit]
        ],
        query=q,
        result_count=len(products),
        search_time_ms=search_time_ms,
        cache_hit=cache_hit,
    )


# ---------------------------------------------------------------------------
# GET /api/promos/active
# ---------------------------------------------------------------------------

@router.get("/promos/active", response_model=PromoResponse)
async def get_active_promos(
    request: Request,
    limit: int = Query(3, ge=1, le=10, description="Max promos"),
    product_sku: Optional[str] = Query(None, description="Filter by product SKU"),
):
    """Get currently active promotions, optionally filtered by product SKU."""
    l1 = getattr(request.app.state, "l1_cache", None)
    l2 = getattr(request.app.state, "l2_cache", None)

    promos = None

    # L1 check
    if l1:
        promos = l1.get("active_promos")

    # L2 fallback
    if promos is None and l2:
        promos = await l2.get_active_promos(limit=limit)
        if promos and l1:
            l1.set("active_promos", promos)

    promos = promos or []

    # Optional SKU filter
    if product_sku:
        promos = [p for p in promos if p.sku and p.sku.lower() == product_sku.lower()]

    promos = promos[:limit]

    return PromoResponse(
        promos=[
            PromoResult(
                id=p.id, description=p.description,
                sku=p.sku, category=p.category,
                discount_percent=p.discount_percent,
                priority=p.priority,
            )
            for p in promos
        ],
        count=len(promos),
    )


# ---------------------------------------------------------------------------
# GET /api/store/info
# ---------------------------------------------------------------------------

@router.get("/store/info", response_model=StoreInfoResponse)
async def get_store_info(request: Request):
    """Get store configuration, hours, and summary stats."""
    from ..config import settings

    l2 = getattr(request.app.state, "l2_cache", None)
    l2_stats = l2.stats() if l2 else {}

    # Pull distinct categories from products
    categories: List[str] = []
    if l2:
        try:
            all_products = await l2.get_all_products(limit=200)
            categories = sorted(set(p.category for p in all_products))
        except Exception:
            pass

    return StoreInfoResponse(
        store_id=settings.store_id,
        reachy_id=settings.reachy_id,
        zone_id=settings.zone_id,
        name="Travel Center",  # TODO: make configurable
        hours="24/7",          # TODO: make configurable
        categories=categories,
        product_count=l2_stats.get("product_count", 0),
        promo_count=l2_stats.get("promo_count", 0),
        status="open",
    )
