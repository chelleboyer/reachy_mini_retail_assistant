"""Data models for Reachy Edge Backend."""
from pydantic import BaseModel
from datetime import datetime

from models.interaction import InteractionRequest, InteractionResponse
from models.events import Event, EventType


class HealthResponse(BaseModel):
    """Health check response model.
    
    Attributes:
        status: Current service health status ('healthy' or 'unhealthy')
        timestamp: Current timestamp in ISO 8601 format
        version: API version number
    """
    status: str
    timestamp: datetime
    version: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "timestamp": "2026-01-10T12:34:56.789Z",
                "version": "0.1.0"
            }
        }
    }


__all__ = ["HealthResponse", "InteractionRequest", "InteractionResponse", "Event", "EventType"]
