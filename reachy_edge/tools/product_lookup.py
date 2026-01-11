"""Product lookup tool for wayfinding."""
import time
from typing import Optional
import logging

from tools.base import Tool, ToolDependencies, ToolResult
from models.events import Event, EventType

logger = logging.getLogger(__name__)


class ProductLookupTool(Tool):
    """Tool for finding products in the store."""
    
    name = "product_lookup"
    description = "Find product location in store"
    
    async def execute(self, query: str, deps: ToolDependencies, **kwargs) -> ToolResult:
        """Look up product and return location."""
        start_time = time.time()
        
        try:
            # Try L1 cache first
            cache_key = f"product:{query.lower()}"
            product = deps.l1_cache.get(cache_key)
            
            if product:
                logger.debug(f"L1 cache hit for product: {query}")
                response = self._format_response(product)
                latency_ms = (time.time() - start_time) * 1000
                
                # Emit event
                if deps.event_emitter:
                    await deps.event_emitter.emit({
                        "event_type": EventType.CACHE_HIT,
                        "query": query,
                        "response": response,
                        "tool_used": self.name,
                        "latency_ms": latency_ms,
                        "reachy_id": deps.reachy_id,
                        "store_id": deps.store_id,
                        "zone_id": deps.zone_id,
                    })
                
                return ToolResult(
                    success=True,
                    data={"response": response, "product": product},
                    latency_ms=latency_ms
                )
            
            # L2 cache lookup
            product = await deps.l2_cache.search_product(query)
            
            if product:
                logger.debug(f"L2 cache hit for product: {query}")
                # Store in L1 for future queries
                deps.l1_cache.set(cache_key, product)
                
                response = self._format_response(product)
                latency_ms = (time.time() - start_time) * 1000
                
                # Emit event
                if deps.event_emitter:
                    await deps.event_emitter.emit({
                        "event_type": EventType.PRODUCT_QUERY,
                        "query": query,
                        "response": response,
                        "tool_used": self.name,
                        "latency_ms": latency_ms,
                        "reachy_id": deps.reachy_id,
                        "store_id": deps.store_id,
                        "zone_id": deps.zone_id,
                        "metadata": {"sku": product.sku, "aisle": product.aisle}
                    })
                
                return ToolResult(
                    success=True,
                    data={"response": response, "product": product},
                    latency_ms=latency_ms
                )
            
            # Product not found
            latency_ms = (time.time() - start_time) * 1000
            response = f"I'm not sure where to find {query}. Let me get a staff member to help you."
            
            if deps.event_emitter:
                await deps.event_emitter.emit({
                    "event_type": EventType.CACHE_MISS,
                    "query": query,
                    "response": response,
                    "tool_used": self.name,
                    "latency_ms": latency_ms,
                    "reachy_id": deps.reachy_id,
                    "store_id": deps.store_id,
                    "zone_id": deps.zone_id,
                })
            
            return ToolResult(
                success=False,
                data={"response": response},
                error="Product not found",
                latency_ms=latency_ms
            )
        
        except Exception as e:
            logger.error(f"Error in product lookup: {e}", exc_info=True)
            latency_ms = (time.time() - start_time) * 1000
            return ToolResult(
                success=False,
                error=str(e),
                latency_ms=latency_ms
            )
    
    def _format_response(self, product: any) -> str:
        """Format product location response."""
        # Keep it under 35 words
        return f"{product.name} is in aisle {product.aisle}. Head that way and look for the {product.category} section."
