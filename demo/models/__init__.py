"""Product model for demo."""
from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    """Product model with FTS5 search support."""
    sku: str = Field(..., description="Unique product SKU")
    name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    location: str = Field(..., description="Store location")
    price: float = Field(..., ge=0, description="Price in USD")
    description: str = Field(..., description="Product description")
    relevance_score: Optional[float] = Field(default=None, description="FTS5 search relevance score")


__all__ = ["Product"]
