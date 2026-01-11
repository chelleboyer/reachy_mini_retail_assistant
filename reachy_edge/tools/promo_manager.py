"""Promotion management tool."""
import time
import logging
from typing import List

from tools.base import Tool, ToolDependencies, ToolResult
from models.events import Event, EventType
from cache.schemas import Promo

logger = logging.getLogger(__name__)


class PromoManagerTool(Tool):
    """Tool for managing and promoting deals."""
    
    name = "promo_manager"
    description = "Get and promote active deals"
    
    async def execute(self, query: str, deps: ToolDependencies, **kwargs) -> ToolResult:
        """Get active promotions and format response."""
        start_time = time.time()
        
        try:
            # Check if specific promo requested or general deals
            limit = kwargs.get("limit", 3)
            
            # Try L1 cache first
            promos = deps.l1_cache.get("active_promos")
            
            if not promos:
                # Get from L2
                promos = await deps.l2_cache.get_active_promos(limit=limit)
                # Cache for future queries
                deps.l1_cache.set("active_promos", promos)
            
            if not promos:
                response = "We don't have any special deals right now, but I can help you find what you're looking for!"
                latency_ms = (time.time() - start_time) * 1000
                
                return ToolResult(
                    success=True,
                    data={"response": response, "promos": []},
                    latency_ms=latency_ms
                )
            
            # Format response (keep under 35 words)
            response = self._format_response(promos[:limit])
            latency_ms = (time.time() - start_time) * 1000
            
            # Emit event for each promo shown
            if deps.event_emitter:
                for promo in promos[:limit]:
                    await deps.event_emitter.emit({
                        "event_type": EventType.PROMO_SHOWN,
                        "query": query,
                        "response": response,
                        "tool_used": self.name,
                        "latency_ms": latency_ms,
                        "reachy_id": deps.reachy_id,
                        "store_id": deps.store_id,
                        "zone_id": deps.zone_id,
                        "metadata": {"promo_id": promo.id, "description": promo.description}
                    })
            
            return ToolResult(
                success=True,
                data={"response": response, "promos": promos[:limit]},
                latency_ms=latency_ms
            )
        
        except Exception as e:
            logger.error(f"Error in promo manager: {e}", exc_info=True)
            latency_ms = (time.time() - start_time) * 1000
            return ToolResult(
                success=False,
                error=str(e),
                latency_ms=latency_ms
            )
    
    def _format_response(self, promos: List[Promo]) -> str:
        """Format promo response (concise)."""
        if len(promos) == 1:
            promo = promos[0]
            return f"Great deal today: {promo.description}!"
        
        # Multiple promos - be concise
        deal_list = ", ".join([p.description for p in promos[:2]])
        if len(promos) > 2:
            return f"Today's deals: {deal_list}, and more. Want to hear details?"
        return f"Today's deals: {deal_list}."
