"""Second Brain backend API models."""
from datetime import datetime
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime


class BatchEventsRequest(BaseModel):
    events: list[dict] = Field(default_factory=list)


class BatchEventsResponse(BaseModel):
    accepted: int
    stored: int
