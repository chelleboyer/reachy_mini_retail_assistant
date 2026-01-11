"""Base tool interface and dependencies."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class ToolResult(BaseModel):
    """Result from tool execution."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    latency_ms: float = 0.0


class ToolDependencies:
    """Dependencies injected into tools."""
    
    def __init__(
        self,
        l1_cache: Any = None,
        l2_cache: Any = None,
        event_emitter: Any = None,
        movement_manager: Any = None,
        reachy_id: str = "",
        store_id: str = "",
        zone_id: str = ""
    ):
        self.l1_cache = l1_cache
        self.l2_cache = l2_cache
        self.event_emitter = event_emitter
        self.movement_manager = movement_manager
        self.reachy_id = reachy_id
        self.store_id = store_id
        self.zone_id = zone_id


class Tool(ABC):
    """Base class for all tools."""
    
    name: str = "base_tool"
    description: str = "Base tool"
    
    @abstractmethod
    async def execute(self, query: str, deps: ToolDependencies, **kwargs) -> ToolResult:
        """Execute the tool with given query and dependencies."""
        pass
    
    def _log_usage(self, deps: ToolDependencies, query: str, result: ToolResult) -> None:
        """Log tool usage for analytics."""
        logger.info(f"Tool {self.name} executed: query='{query}', success={result.success}")
