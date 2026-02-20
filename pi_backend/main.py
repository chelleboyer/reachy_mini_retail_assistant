"""π backend FastAPI service."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException

from .cache.generator import generate_cache
from .config import settings
from .db.canonical_store import CanonicalStore
from .db.knowledge_graph import KnowledgeGraph
from .db.vector_store import VectorStore
from .models import BatchEventsRequest, BatchEventsResponse, HealthResponse

app = FastAPI(title="Pi Backend", version=settings.api_version)
store = CanonicalStore(settings.db_path)
kg = KnowledgeGraph(settings.db_path)
vector = VectorStore(backend=settings.vector_backend, qdrant_url=settings.qdrant_url, collection=settings.qdrant_collection)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        timestamp=datetime.now(timezone.utc),
    )


@app.post("/events/batch", response_model=BatchEventsResponse)
@app.post("/events/ingest", response_model=BatchEventsResponse)
async def ingest_events(
    payload: BatchEventsRequest,
    x_tenant_id: str = Header(default="default"),
    x_trace_id: str | None = Header(default=None),
) -> BatchEventsResponse:
    if not payload.events:
        raise HTTPException(status_code=400, detail="No events provided")

    trace_id = x_trace_id or str(uuid4())
    stored = 0
    for event in payload.events:
        event.setdefault("tenant_id", x_tenant_id)
        event.setdefault("trace_id", trace_id)
        event.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        store.save_event(event)
        stored += 1

    return BatchEventsResponse(accepted=len(payload.events), stored=stored)


@app.get("/cache/sync")
async def cache_sync(
    domain: str = "retail",
    store_id: str = "STORE-DEV",
    since_version: str | None = None,
    x_tenant_id: str = Header(default="default"),
) -> dict[str, Any]:
    payload = generate_cache(domain=domain, store_id=store_id)
    payload["tenant_id"] = x_tenant_id
    payload["since_version"] = since_version
    payload["diff"] = {"added": payload["products"], "updated": [], "deleted": []}
    return payload
