"""Movement and gesture tool."""
import time
import logging

from tools.base import Tool, ToolDependencies, ToolResult

logger = logging.getLogger(__name__)


class MovementTool(Tool):
    """Tool for coordinating robot gestures and movements."""
    
    name = "movement"
    description = "Control robot gestures and movements"
    
    async def execute(self, query: str, deps: ToolDependencies, **kwargs) -> ToolResult:
        """Execute movement or gesture."""
        start_time = time.time()
        
        try:
            gesture = kwargs.get("gesture", "point")
            direction = kwargs.get("direction", "forward")
            
            # If movement_manager is available, use it
            if deps.movement_manager:
                # This would integrate with the conversation app's MovementManager
                logger.info(f"Would execute gesture '{gesture}' in direction '{direction}'")
                # deps.movement_manager.queue_move(...)
            else:
                logger.warning("Movement manager not available")
            
            latency_ms = (time.time() - start_time) * 1000
            
            return ToolResult(
                success=True,
                data={
                    "gesture": gesture,
                    "direction": direction,
                    "executed": deps.movement_manager is not None
                },
                latency_ms=latency_ms
            )
        
        except Exception as e:
            logger.error(f"Error in movement tool: {e}", exc_info=True)
            latency_ms = (time.time() - start_time) * 1000
            return ToolResult(
                success=False,
                error=str(e),
                latency_ms=latency_ms
            )
