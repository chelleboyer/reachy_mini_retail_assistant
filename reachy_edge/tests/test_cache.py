"""Test cache functionality."""
import pytest
from reachy_edge.cache import L1Cache, L2Cache
from reachy_edge.cache.schemas import Product, Promo
from datetime import datetime


def test_l1_cache_set_get():
    """Test L1 cache basic operations."""
    cache = L1Cache(max_size=10, ttl_seconds=60)
    
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    assert cache.get("key2") is None


def test_l1_cache_eviction():
    """Test L1 cache LRU eviction."""
    cache = L1Cache(max_size=2, ttl_seconds=60)
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")  # Should evict key1
    
    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"


def test_l1_cache_stats():
    """Test L1 cache statistics."""
    cache = L1Cache()
    
    cache.set("key1", "value1")
    cache.get("key1")  # Hit
    cache.get("key2")  # Miss
    
    stats = cache.stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["hit_rate_pct"] == 50.0


@pytest.mark.asyncio
async def test_l2_cache_products():
    """Test L2 cache product operations."""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name
    
    try:
        cache = L2Cache(db_path)
        
        products = [
            Product(sku="SKU001", name="Milk", aisle="5", category="Dairy", price=3.99),
            Product(sku="SKU002", name="Bread", aisle="2", category="Bakery", price=2.49)
        ]
        
        await cache.update_products(products)
        
        # Search
        result = await cache.search_product("milk")
        assert result is not None
        assert result.sku == "SKU001"
        assert result.aisle == "5"
    
    finally:
        os.unlink(db_path)


@pytest.mark.asyncio
async def test_l2_cache_promos():
    """Test L2 cache promo operations."""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name
    
    try:
        cache = L2Cache(db_path)
        
        promos = [
            Promo(id="PROMO1", description="50% off dairy", category="Dairy", priority=10),
            Promo(id="PROMO2", description="Buy 2 get 1 free", category="Bakery", priority=5)
        ]
        
        await cache.update_promos(promos)
        
        # Get active promos
        active = await cache.get_active_promos(limit=2)
        assert len(active) == 2
        assert active[0].id == "PROMO1"  # Higher priority first
    
    finally:
        os.unlink(db_path)
