"""Interaction request/response models."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class InteractionRequest(BaseModel):
    """Request model for customer interaction."""
    
    query: str = Field(..., description="Customer question or statement")
    session_id: str = Field(..., description="Unique session identifier")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Conversation context")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class InteractionResponse(BaseModel):
    """Response model for customer interaction."""
    
    response: str = Field(..., description="Response to customer")
    intent: Optional[str] = Field(default=None, description="Detected intent")
    tool_used: Optional[str] = Field(default=None, description="Tool that generated response")
    latency_ms: float = Field(..., description="Response latency in milliseconds")
    cache_hit: bool = Field(default=False, description="Whether response came from cache")
    needs_clarification: bool = Field(default=False, description="Whether clarification is needed")
    clarification_question: Optional[str] = Field(default=None, description="Follow-up question if needed")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
