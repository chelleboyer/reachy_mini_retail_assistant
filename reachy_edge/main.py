"""FastAPI main application for Reachy Edge Backend."""
import logging
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import structlog

from config import settings
from cache import L1Cache, L2Cache, CacheSyncPayload
from pi_client import EventEmitter
from tools import (
    ToolDependencies,
    ProductLookupTool,
    PromoManagerTool,
    SelfieTool,
    MovementTool
)
from llm import PromptManager, LLMInference
from models import HealthResponse, InteractionRequest, InteractionResponse

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    logger.info("Starting Reachy Edge Backend...")
    
    # Initialize cache layers
    app.state.l2_cache = L2Cache(settings.l2_db_path)
    app.state.l1_cache = L1Cache(
        max_size=settings.l1_max_size,
        ttl_seconds=settings.l1_ttl_seconds
    )
    
    # Initialize event emitter
    app.state.event_emitter = EventEmitter()
    
    # Initialize LLM
    app.state.llm = LLMInference(
        mode=settings.llm_mode,
        api_key=settings.openai_api_key,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens
    )
    
    # Initialize prompt manager
    app.state.prompt_manager = PromptManager(max_words=settings.max_response_words)
    
    # Initialize tools
    app.state.tools = {
        "product_lookup": ProductLookupTool(),
        "promo_manager": PromoManagerTool(),
        "selfie": SelfieTool(),
        "movement": MovementTool(),
    }
    
    # Preload hot data from L2 to L1
    await app.state.l2_cache.preload_hot_data(app.state.l1_cache)
    logger.info("Preloaded cache data")
    
    # Start event emitter worker
    asyncio.create_task(app.state.event_emitter.worker())
    logger.info("Event emitter worker started")
    
    logger.info(f"Reachy Edge Backend ready (ID: {settings.reachy_id}, Store: {settings.store_id})")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Reachy Edge Backend...")
    app.state.event_emitter.stop()
    await app.state.event_emitter.flush()
    logger.info("Shutdown complete")


app = FastAPI(
    title="Reachy Edge Backend",
    description="Fast, scalable Pi 5 backend for Reachy Mini retail assistant",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_tool_deps() -> ToolDependencies:
    """Get tool dependencies from app state."""
    return ToolDependencies(
        l1_cache=app.state.l1_cache,
        l2_cache=app.state.l2_cache,
        event_emitter=app.state.event_emitter,
        movement_manager=None,  # TODO: Wire to conversation app
        reachy_id=settings.reachy_id,
        store_id=settings.store_id,
        zone_id=settings.zone_id
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Reachy Edge Backend",
        "version": "0.1.0",
        "reachy_id": settings.reachy_id,
        "store_id": settings.store_id,
        "zone_id": settings.zone_id
    }


@app.get("/health", response_model=HealthResponse)
async def get_health() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns current service health status with timestamp and version.
    Always returns 'healthy' status in this story (no database checks yet).
    
    Returns:
        HealthResponse: Service health status, current UTC timestamp, and API version
    """
    from datetime import datetime, timezone
    
    timestamp = datetime.now(timezone.utc)
    
    logger.info("health_check", extra={
        "status": "healthy",
        "version": settings.api_version,
        "timestamp": timestamp.isoformat()
    })
    
    return {
        "status": "healthy",
        "timestamp": timestamp,
        "version": settings.api_version
    }


@app.post("/interact", response_model=InteractionResponse)
async def interact(request: InteractionRequest):
    """Main interaction endpoint."""
    import time
    start_time = time.time()
    
    logger.info(f"Interaction: session={request.session_id}, query='{request.query}'")
    
    try:
        # Determine intent and route to appropriate tool
        intent = _classify_intent(request.query)
        tool_name = _intent_to_tool(intent)
        
        if tool_name not in app.state.tools:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        
        tool = app.state.tools[tool_name]
        deps = _get_tool_deps()
        
        # Execute tool
        result = await tool.execute(request.query, deps)
        
        latency_ms = (time.time() - start_time) * 1000
        
        if not result.success:
            logger.warning(f"Tool execution failed: {result.error}")
            # Return fallback response
            return InteractionResponse(
                response="I'm having trouble with that. Let me get a staff member to help you.",
                intent=intent,
                tool_used=tool_name,
                latency_ms=latency_ms,
                cache_hit=False,
                metadata={"error": result.error}
            )
        
        return InteractionResponse(
            response=result.data["response"],
            intent=intent,
            tool_used=tool_name,
            latency_ms=latency_ms,
            cache_hit=result.latency_ms < 50,  # Heuristic for cache hit
            metadata=result.data
        )
    
    except Exception as e:
        logger.error(f"Error in interaction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cache/sync")
async def sync_cache(payload: CacheSyncPayload):
    """Receive cache updates from π."""
    logger.info(f"Received cache sync: version={payload.version}")
    
    try:
        # Update L2 cache
        if payload.products:
            await app.state.l2_cache.update_products(payload.products)
        
        if payload.promos:
            await app.state.l2_cache.update_promos(payload.promos)
        
        # Update version
        await app.state.l2_cache.set_version(payload.version)
        
        # Invalidate L1 to force reload
        app.state.l1_cache.invalidate()
        
        # Preload hot data
        await app.state.l2_cache.preload_hot_data(app.state.l1_cache)
        
        return {
            "status": "synced",
            "version": payload.version,
            "products_updated": len(payload.products) if payload.products else 0,
            "promos_updated": len(payload.promos) if payload.promos else 0
        }
    
    except Exception as e:
        logger.error(f"Error syncing cache: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


def _classify_intent(query: str) -> str:
    """Simple intent classification (TODO: replace with LLM)."""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["where", "find", "looking for", "location"]):
        return "product_lookup"
    
    if any(word in query_lower for word in ["deal", "sale", "promo", "discount", "offer"]):
        return "promo"
    
    if any(word in query_lower for word in ["selfie", "picture", "photo"]):
        return "selfie"
    
    # Default to product lookup
    return "product_lookup"


def _intent_to_tool(intent: str) -> str:
    """Map intent to tool name."""
    intent_map = {
        "product_lookup": "product_lookup",
        "promo": "promo_manager",
        "selfie": "selfie",
    }
    return intent_map.get(intent, "product_lookup")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
