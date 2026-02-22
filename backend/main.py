"""Second Brain backend FastAPI service."""
from datetime import datetime, timezone
from fastapi import FastAPI

from .config import settings
from .models import HealthResponse, BatchEventsRequest, BatchEventsResponse
from .db.canonical_store import CanonicalStore
from .db.knowledge_graph import KnowledgeGraph
from .cache.generator import generate_cache

app = FastAPI(title="Second Brain Backend", version=settings.api_version)
store = CanonicalStore(settings.db_path)
kg = KnowledgeGraph(settings.db_path)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="healthy", version=settings.api_version, timestamp=datetime.now(timezone.utc))


@app.post("/events/batch", response_model=BatchEventsResponse)
async def ingest_events(payload: BatchEventsRequest) -> BatchEventsResponse:
    stored = 0
    for event in payload.events:
        store.save_event(event)
        stored += 1
    return BatchEventsResponse(accepted=len(payload.events), stored=stored)


@app.get("/cache/sync")
async def cache_sync(domain: str = "retail", store_id: str = "STORE-DEV") -> dict:
    return generate_cache(domain=domain, store_id=store_id)
