"""Selfie tool for customer engagement."""
import time
import logging

from tools.base import Tool, ToolDependencies, ToolResult
from models.events import Event, EventType

logger = logging.getLogger(__name__)


class SelfieTool(Tool):
    """Tool for offering and taking selfies."""
    
    name = "selfie"
    description = "Offer and coordinate selfie with customer"
    
    async def execute(self, query: str, deps: ToolDependencies, **kwargs) -> ToolResult:
        """Handle selfie interaction."""
        start_time = time.time()
        
        try:
            action = kwargs.get("action", "offer")
            
            if action == "offer":
                response = "Would you like to take a selfie with me? I love taking pictures!"
            elif action == "accept":
                response = "Awesome! Let's do this. Say cheese in 3... 2... 1... Click!"
                # TODO: Trigger actual camera when hardware is connected
            elif action == "decline":
                response = "No problem! Let me know if you need help finding anything."
            else:
                response = "Want a selfie? I'm ready when you are!"
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Emit event
            if deps.event_emitter:
                await deps.event_emitter.emit({
                    "event_type": EventType.SELFIE,
                    "query": query,
                    "response": response,
                    "tool_used": self.name,
                    "latency_ms": latency_ms,
                    "reachy_id": deps.reachy_id,
                    "store_id": deps.store_id,
                    "zone_id": deps.zone_id,
                    "metadata": {"action": action}
                })
            
            return ToolResult(
                success=True,
                data={"response": response, "action": action},
                latency_ms=latency_ms
            )
        
        except Exception as e:
            logger.error(f"Error in selfie tool: {e}", exc_info=True)
            latency_ms = (time.time() - start_time) * 1000
            return ToolResult(
                success=False,
                error=str(e),
                latency_ms=latency_ms
            )
