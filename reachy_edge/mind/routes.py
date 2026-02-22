"""Mind Monitor — SSE endpoints and dashboard routes.

Mounts under /mind on the FastAPI app:
  GET /mind          → HTML dashboard
  GET /mind/events   → SSE event stream (real-time)
  GET /mind/state    → JSON snapshot (initial load)
  GET /mind/products → Product catalog browser
  POST /mind/signal  → Receive forwarded Karen Whisperer signals
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import structlog
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, StreamingResponse

from . import MindEvent, mind_bus, EVENT_SIGNAL

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/mind", tags=["Mind Monitor"])


# ---------------------------------------------------------------------------
# SSE stream — real-time push
# ---------------------------------------------------------------------------

@router.get("/events")
async def mind_events():
    """Server-Sent Events stream of all mind activity.

    Connect with ``new EventSource('/mind/events')`` from the browser.
    """

    async def event_generator():
        # Send initial heartbeat
        yield "event: connected\ndata: {}\n\n"
        async for event in mind_bus.subscribe():
            yield event.to_sse()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


# ---------------------------------------------------------------------------
# State snapshot — for initial dashboard load
# ---------------------------------------------------------------------------

@router.get("/state")
async def mind_state(request: Request) -> Dict[str, Any]:
    """Return aggregated state for dashboard initialisation."""
    snapshot = mind_bus.snapshot()

    # Merge live cache stats from app state
    l1 = getattr(request.app.state, "l1_cache", None)
    l2 = getattr(request.app.state, "l2_cache", None)
    snapshot["cache"] = {
        "l1": l1.stats() if l1 else {},
        "l2": l2.stats() if l2 else {},
    }
    return snapshot


# ---------------------------------------------------------------------------
# Product catalog browser
# ---------------------------------------------------------------------------

@router.get("/products")
async def mind_products(request: Request, q: str = "", limit: int = 20):
    """Search the product catalog (or list all if no query)."""
    l2 = getattr(request.app.state, "l2_cache", None)
    if l2 is None:
        return {"products": [], "total": 0}

    if q.strip():
        results = await l2.search_products(q, max_results=limit)
    else:
        results = await l2.get_all_products(limit=limit)

    return {
        "products": [
            {
                "sku": p.sku,
                "name": p.name,
                "category": p.category,
                "location": p.location,
                "price": p.price,
                "description": getattr(p, "description", ""),
            }
            for p in results
        ],
        "total": len(results),
        "query": q,
    }


# ---------------------------------------------------------------------------
# Signal ingestion (from Karen Whisperer)
# ---------------------------------------------------------------------------

@router.post("/signal")
async def receive_signal(payload: Dict[str, Any]):
    """Receive a forwarded signal from Karen Whisperer's signal tracker."""
    await mind_bus.publish(
        MindEvent(type=EVENT_SIGNAL, data=payload)
    )
    return {"status": "received"}


# ---------------------------------------------------------------------------
# Dashboard HTML
# ---------------------------------------------------------------------------

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def mind_dashboard():
    """Serve the Mind Monitor dashboard."""
    html_path = Path(__file__).parent / "dashboard.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
