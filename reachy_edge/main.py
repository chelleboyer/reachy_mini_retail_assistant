"""FastAPI main application for Edge Backend."""
from __future__ import annotations

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

import structlog
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .config import settings
from .cache import L1Cache, L2Cache, CacheSyncPayload
from .fsm import InteractionStateMachine
from .brain_client import EventEmitter
from .tools import (
    ToolDependencies,
    ProductLookupTool,
    PromoManagerTool,
    SelfieTool,
    MovementTool
)
from .llm import PromptManager, LLMInference
from .models import HealthResponse, InteractionRequest, InteractionResponse
from .mind import mind_bus, MindEvent, EVENT_REQUEST, EVENT_RESPONSE, EVENT_ERROR
from .mind.routes import router as mind_router
from .api.routes import router as api_router

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(),
)
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    logger.info("starting_reachy_edge")

    app.state.l2_cache = L2Cache(settings.l2_db_path)
    app.state.l1_cache = L1Cache(max_size=settings.l1_max_size, ttl_seconds=settings.l1_ttl_seconds)
    app.state.event_emitter = EventEmitter()
    app.state.llm = LLMInference(
        mode=settings.llm_mode,
        api_key=settings.openai_api_key,
        model=settings.inference_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )
    app.state.prompt_manager = PromptManager(max_words=settings.max_response_words)
    app.state.fsm = InteractionStateMachine()
    app.state.tools = {
        "product_lookup": ProductLookupTool(),
        "promo_manager": PromoManagerTool(),
        "selfie": SelfieTool(),
        "movement": MovementTool(),
    }

    # Auto-load sample products so the API works out of the box
    from .data.sample_products import get_sample_products
    from .cache.schemas import Product as CacheProduct
    sample = get_sample_products()
    cache_products = [
        CacheProduct(
            sku=p.sku, name=p.name,
            aisle=app.state.l2_cache._extract_aisle(p.location),
            category=p.category, price=p.price, description=p.description,
        )
        for p in sample
    ]
    await app.state.l2_cache.update_products(cache_products)
    logger.info("sample_products_loaded", count=len(sample))

    await app.state.l2_cache.preload_hot_data(app.state.l1_cache)
    asyncio.create_task(app.state.event_emitter.worker())

    app.state._start_time = time.time()
    mind_bus.publish_sync(MindEvent(type="startup", data={
        "reachy_id": settings.reachy_id,
        "store_id": settings.store_id,
    }))

    logger.info(
        "reachy_edge_ready",
        reachy_id=settings.reachy_id,
        store_id=settings.store_id,
        l2_backend=settings.l2_backend,
        inference_model=settings.inference_model,
        embedding_model=settings.embedding_model,
    )

    yield

    logger.info("shutting_down_reachy_edge")
    mind_bus.publish_sync(MindEvent(type="shutdown", data={}))
    app.state.event_emitter.stop()
    await app.state.event_emitter.flush()


app = FastAPI(
    title="Edge Backend",
    description="Fast, scalable edge backend for retail assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Mind Monitor middleware — publishes request/response events on every call
# ---------------------------------------------------------------------------

class MindMiddleware(BaseHTTPMiddleware):
    """Publish request/response events to the Mind Monitor event bus."""

    async def dispatch(self, request: Request, call_next):
        # Skip SSE / static mind endpoints to avoid noise
        if request.url.path.startswith("/mind"):
            return await call_next(request)

        start = time.time()
        mind_bus.publish_sync(MindEvent(
            type=EVENT_REQUEST,
            data={"method": request.method, "path": request.url.path,
                  "query": dict(request.query_params)},
        ))

        try:
            response: Response = await call_next(request)
            latency_ms = (time.time() - start) * 1000
            mind_bus.publish_sync(MindEvent(
                type=EVENT_RESPONSE,
                data={"path": request.url.path, "status": response.status_code,
                      "latency_ms": round(latency_ms, 2)},
            ))
            return response
        except Exception as exc:
            latency_ms = (time.time() - start) * 1000
            mind_bus.publish_sync(MindEvent(
                type=EVENT_ERROR,
                data={"path": request.url.path, "error": str(exc),
                      "latency_ms": round(latency_ms, 2)},
            ))
            raise


app.add_middleware(MindMiddleware)
app.include_router(mind_router)
app.include_router(api_router)


def _get_tool_deps() -> ToolDependencies:
    """Get tool dependencies from app state."""
    return ToolDependencies(
        l1_cache=app.state.l1_cache,
        l2_cache=app.state.l2_cache,
        event_emitter=app.state.event_emitter,
        movement_manager=None,
        reachy_id=settings.reachy_id,
        store_id=settings.store_id,
        zone_id=settings.zone_id,
    )


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "service": "Reachy Edge Backend",
        "version": settings.api_version,
        "reachy_id": settings.reachy_id,
        "store_id": settings.store_id,
        "zone_id": settings.zone_id,
    }


@app.get("/health", response_model=HealthResponse)
async def get_health() -> dict[str, Any]:
    """Enhanced health endpoint with cache and runtime stats (Story 1.6)."""
    timestamp = datetime.now(timezone.utc)
    l1 = getattr(app.state, "l1_cache", None)
    l2 = getattr(app.state, "l2_cache", None)
    emitter = getattr(app.state, "event_emitter", None)
    llm = getattr(app.state, "llm", None)

    details = {
        "l1": l1.stats() if l1 else {"status": "not_initialized"},
        "l2": l2.stats() if l2 else {"status": "not_initialized"},
        "event_emitter": emitter.stats() if emitter else {"status": "not_initialized"},
        "llm": llm.get_stats() if llm else {"status": "not_initialized"},
        "models": {
            "inference_provider": settings.inference_provider,
            "inference_model": settings.inference_model,
            "embedding_provider": settings.embedding_provider,
            "embedding_model": settings.embedding_model,
        },
    }
    return {
        "status": "healthy",
        "timestamp": timestamp,
        "version": settings.api_version,
        "details": details,
    }


@app.post("/interact", response_model=InteractionResponse)
async def interact(request: InteractionRequest) -> InteractionResponse:
    """Main interaction endpoint (Story 1.5 + Epic 2 core flow)."""
    start = time.time()
    deps = _get_tool_deps()
    fsm: InteractionStateMachine = app.state.fsm

    try:
        fsm.begin()
        intent = _classify_intent(request.query)
        tool_name = _intent_to_tool(intent)
        tool = app.state.tools[tool_name]

        fsm.processing()
        result = await tool.execute(request.query, deps, max_results=3)
        latency_ms = (time.time() - start) * 1000

        fsm.responding()
        if not result.success:
            mind_bus.publish_sync(MindEvent(
                type="cache_miss",
                data={"query": request.query, "intent": intent, "tool": tool_name},
            ))
            return InteractionResponse(
                response=result.data.get("response", "I couldn't find that right now."),
                intent=intent,
                tool_used=tool_name,
                latency_ms=latency_ms,
                cache_hit=False,
                metadata={"state": fsm.state.value, "error": result.error, **(result.data or {})},
            )

        cache_hit = bool((result.data or {}).get("cache_hit", False))
        result_count = (result.data or {}).get("result_count", 0)
        mind_bus.publish_sync(MindEvent(
            type="cache_hit" if cache_hit else "search",
            data={
                "query": request.query,
                "intent": intent,
                "tool": tool_name,
                "result_count": result_count,
                "tier": "L1" if cache_hit else "L2",
                "latency_ms": round(latency_ms, 2),
            },
        ))
        metadata = {
            "state": fsm.state.value,
            "products": (result.data or {}).get("products", []),
            "result_count": (result.data or {}).get("result_count", 0),
        }

        return InteractionResponse(
            response=result.data["response"],
            intent=intent,
            tool_used=tool_name,
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            metadata=metadata,
        )
    except Exception as exc:
        logger.error("interaction_error", error=str(exc), exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        fsm.reset()


@app.post("/cache/sync")
@app.post("/cache/apply")
async def apply_cache(payload: CacheSyncPayload) -> dict[str, Any]:
    """Receive cache updates from the Second Brain and apply them to local caches."""
    try:
        if payload.products:
            await app.state.l2_cache.update_products(payload.products)
        if payload.promos:
            await app.state.l2_cache.update_promos(payload.promos)

        await app.state.l2_cache.set_version(payload.version)
        app.state.l1_cache.invalidate()
        await app.state.l2_cache.preload_hot_data(app.state.l1_cache)

        return {
            "status": "synced",
            "version": payload.version,
            "products_updated": len(payload.products) if payload.products else 0,
            "promos_updated": len(payload.promos) if payload.promos else 0,
        }
    except Exception as exc:
        logger.error("cache_sync_error", error=str(exc), exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


def _classify_intent(query: str) -> str:
    """Rule-based intent classifier for MVP."""
    query_lower = query.lower()
    if any(word in query_lower for word in ["where", "find", "looking for", "location"]):
        return "product_lookup"
    if any(word in query_lower for word in ["deal", "sale", "promo", "discount", "offer"]):
        return "promo"
    if any(word in query_lower for word in ["selfie", "picture", "photo"]):
        return "selfie"
    return "product_lookup"


def _intent_to_tool(intent: str) -> str:
    """Map intent to tool name."""
    return {"product_lookup": "product_lookup", "promo": "promo_manager", "selfie": "selfie"}.get(
        intent, "product_lookup"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "reachy_edge.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
