"""Test tool functionality."""
import pytest
from reachy_edge.tools import (
    ProductLookupTool,
    PromoManagerTool,
    ToolDependencies
)
from reachy_edge.cache import L1Cache, L2Cache
from reachy_edge.cache.schemas import Product, Promo
from datetime import datetime


@pytest.mark.asyncio
async def test_product_lookup_tool():
    """Test product lookup tool."""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name
    
    try:
        l1_cache = L1Cache()
        l2_cache = L2Cache(db_path)
        
        # Add test product
        products = [
            Product(sku="SKU001", name="Milk", aisle="5", category="Dairy")
        ]
        await l2_cache.update_products(products)
        
        deps = ToolDependencies(
            l1_cache=l1_cache,
            l2_cache=l2_cache,
            reachy_id="TEST",
            store_id="TEST",
            zone_id="TEST"
        )
        
        tool = ProductLookupTool()
        result = await tool.execute("milk", deps)
        
        assert result.success is True
        assert "aisle 5" in result.data["response"].lower()
    
    finally:
        os.unlink(db_path)


@pytest.mark.asyncio
async def test_promo_manager_tool():
    """Test promo manager tool."""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name
    
    try:
        l1_cache = L1Cache()
        l2_cache = L2Cache(db_path)
        
        # Add test promos
        promos = [
            Promo(id="PROMO1", description="50% off dairy", priority=10)
        ]
        await l2_cache.update_promos(promos)
        
        deps = ToolDependencies(
            l1_cache=l1_cache,
            l2_cache=l2_cache,
            reachy_id="TEST",
            store_id="TEST",
            zone_id="TEST"
        )
        
        tool = PromoManagerTool()
        result = await tool.execute("deals", deps)
        
        assert result.success is True
        assert "50%" in result.data["response"]
    
    finally:
        os.unlink(db_path)
