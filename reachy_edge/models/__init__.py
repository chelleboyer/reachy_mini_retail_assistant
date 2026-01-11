"""Data models for Reachy Edge Backend."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

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


class Product(BaseModel):
    """Product model for L2 cache storage.
    
    Represents truck stop/travel center product with full-text search support.
    
    Attributes:
        sku: Unique product identifier
        name: Product display name
        category: Product category (Fuel, Trucker Supplies, Electronics, etc.)
        location: Physical location in store (e.g., "Aisle 2", "Fuel Island 3")
        price: Product price in USD
        description: Full product description with keywords
        relevance_score: Search relevance score from FTS5 BM25 ranking (optional)
    """
    sku: str = Field(..., description="Unique product SKU")
    name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    location: str = Field(..., description="Store location")
    price: float = Field(..., ge=0, description="Price in USD")
    description: str = Field(..., description="Product description")
    relevance_score: Optional[float] = Field(default=None, description="FTS5 search relevance score")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "sku": "FUEL-DEF-001",
                "name": "BlueDEF Diesel Exhaust Fluid",
                "category": "Fuel & Fluids",
                "location": "Fuel Island 2",
                "price": 12.99,
                "description": "Premium DEF fluid for SCR systems, DOT compliant",
                "relevance_score": 1.234
            }
        }
    }


__all__ = [
    "HealthResponse",
    "Product",
    "InteractionRequest",
    "InteractionResponse",
    "Event",
    "EventType"
]
