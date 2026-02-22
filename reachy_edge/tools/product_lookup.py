"""Product lookup tool for wayfinding."""
from __future__ import annotations

import logging
import time

from .base import Tool, ToolDependencies, ToolResult
from ..models.events import EventType

logger = logging.getLogger(__name__)


class ProductLookupTool(Tool):
    """Tool for finding products in the store."""

    name = "product_lookup"
    description = "Find product location in store"

    async def lookup_product(
        self,
        query: str,
        deps: ToolDependencies,
        max_results: int = 5,
    ) -> list:
        """Lookup products and rank exact SKU matches first."""
        products = await deps.l2_cache.search_products(query, max_results=max_results)
        if not products:
            return []

        query_norm = query.strip().lower()
        products.sort(key=lambda p: 0 if p.sku.lower() == query_norm else 1)
        return products

    async def execute(self, query: str, deps: ToolDependencies, **kwargs) -> ToolResult:
        """Look up product and return concise response."""
        start_time = time.time()
        max_results = int(kwargs.get("max_results", 3))

        try:
            cache_key = f"product:{query.lower()}"
            cache_hit = False

            top_product = deps.l1_cache.get(cache_key)
            products = []
            if top_product:
                cache_hit = True
                products = [top_product]
            else:
                products = await self.lookup_product(query=query, deps=deps, max_results=max_results)
                if products:
                    deps.l1_cache.set(cache_key, products[0])

            latency_ms = (time.time() - start_time) * 1000

            if not products:
                response = f"I couldn't find any products matching '{query}'."
                if deps.event_emitter:
                    await deps.event_emitter.emit(
                        {
                            "event_type": EventType.CACHE_MISS,
                            "query": query,
                            "response": response,
                            "tool_used": self.name,
                            "latency_ms": latency_ms,
                            "reachy_id": deps.reachy_id,
                            "store_id": deps.store_id,
                            "zone_id": deps.zone_id,
                        }
                    )
                return ToolResult(success=False, data={"response": response, "products": []}, error="Product not found", latency_ms=latency_ms)

            response = self._format_response(products[0])

            if deps.event_emitter:
                await deps.event_emitter.emit(
                    {
                        "event_type": EventType.CACHE_HIT if cache_hit else EventType.PRODUCT_QUERY,
                        "query": query,
                        "response": response,
                        "tool_used": self.name,
                        "latency_ms": latency_ms,
                        "reachy_id": deps.reachy_id,
                        "store_id": deps.store_id,
                        "zone_id": deps.zone_id,
                        "metadata": {
                            "sku": products[0].sku,
                            "location": products[0].location,
                            "result_count": len(products),
                            "cache_hit": cache_hit,
                        },
                    }
                )

            return ToolResult(
                success=True,
                data={
                    "response": response,
                    "products": products,
                    "cache_hit": cache_hit,
                    "result_count": len(products),
                },
                latency_ms=latency_ms,
            )

        except Exception as exc:
            logger.error("error_in_product_lookup", exc_info=True)
            latency_ms = (time.time() - start_time) * 1000
            return ToolResult(success=False, error=str(exc), latency_ms=latency_ms)

    @staticmethod
    def _format_response(product: any) -> str:
        """Format product location response under 35 words."""
        return f"{product.name} is at {product.location}. Check the {product.category} section there."
