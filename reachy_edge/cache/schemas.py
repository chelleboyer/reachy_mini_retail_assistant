"""Cache data schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class Product(BaseModel):
    """Product information."""
    sku: str
    name: str
    aisle: str
    category: str
    price: Optional[float] = None
    description: Optional[str] = None


class Promo(BaseModel):
    """Promotion/deal information."""
    id: str
    description: str
    sku: Optional[str] = None
    category: Optional[str] = None
    discount_percent: Optional[float] = None
    expiry: Optional[datetime] = None
    priority: int = 0


class CacheSyncPayload(BaseModel):
    """Payload for cache sync from π."""
    version: str
    timestamp: datetime
    products: Optional[List[Product]] = None
    promos: Optional[List[Promo]] = None
    store_config: Optional[Dict[str, Any]] = None
