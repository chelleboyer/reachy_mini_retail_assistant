"""Event models for Second Brain integration."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """Types of events sent to the Second Brain."""
    CACHE_HIT = "cache_hit"
    CACHE_MISS = "cache_miss"
    PRODUCT_QUERY = "product_query"
    PROMO_SHOWN = "promo_shown"
    NAVIGATION = "navigation"
    SELFIE = "selfie"
    CLARIFICATION = "clarification"
    ERROR = "error"


class Event(BaseModel):
    """Event sent to the Second Brain for classification and storage."""
    
    event_type: EventType
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    reachy_id: str
    store_id: str
    zone_id: str
    
    # Event payload
    query: Optional[str] = None
    response: Optional[str] = None
    intent: Optional[str] = None
    tool_used: Optional[str] = None
    latency_ms: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    
    model_config = {"use_enum_values": True}
