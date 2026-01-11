"""Tests for L2 Cache (SQLite FTS5) product storage."""
import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime

# Will fail until we create the l2_cache module
from cache.l2_cache import ProductCache
from models import Product


class TestProductCacheDatabaseInit:
    """Test database initialization."""
    
    def test_database_file_created(self):
        """Test that database file is created on initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache = ProductCache(str(db_path))
            cache.initialize()
            
            assert db_path.exists(), "Database file should be created"
            # Close connection to release file lock
            cache.close()
    
    def test_fts5_table_created(self):
        """Test that FTS5 virtual table is created with correct schema."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache = ProductCache(str(db_path))
            cache.initialize()
            
            # Query through the cache's connection (not a new connection)
            conn = cache._get_connection()
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='products_fts'"
            )
            result = cursor.fetchone()
            assert result is not None, "products_fts table should exist"
            
            # Close cache connection
            cache.close()
    
    def test_initialize_idempotent(self):
        """Test that calling initialize multiple times is safe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache = ProductCache(str(db_path))
            
            # Should not raise exception
            cache.initialize()
            cache.initialize()
            cache.initialize()
            
            # Close connection
            cache.close()


class TestProductInsertion:
    """Test product insertion into database."""
    
    @pytest.fixture
    def cache(self):
        """Create temporary cache for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache_instance = ProductCache(str(db_path))
            cache_instance.initialize()
            yield cache_instance
            # Close connection to release file lock (important on Windows)
            cache_instance.close()
    
    def test_insert_single_product(self, cache):
        """Test inserting a single product."""
        product = Product(
            sku="FUEL-DEF-001",
            name="BlueDEF Diesel Exhaust Fluid",
            category="Fuel & Fluids",
            location="Fuel Island 2",
            price=12.99,
            description="Premium DEF fluid for SCR systems"
        )
        
        cache.insert_product(product)
        
        # Verify insertion
        results = cache.search_products("DEF")
        assert len(results) == 1
        assert results[0].sku == "FUEL-DEF-001"
    
    def test_insert_multiple_products(self, cache):
        """Test bulk insertion of products."""
        products = [
            Product(
                sku="FUEL-DEF-001",
                name="BlueDEF Diesel Exhaust Fluid",
                category="Fuel & Fluids",
                location="Fuel Island 2",
                price=12.99,
                description="Premium DEF fluid"
            ),
            Product(
                sku="ELECT-CB-105",
                name="Cobra 29 LX CB Radio",
                category="Electronics",
                location="Aisle 4 - Electronics",
                price=129.99,
                description="40-channel CB radio"
            ),
        ]
        
        cache.insert_products(products)
        
        # Verify both inserted
        all_results = cache.search_products("fluid OR radio")
        assert len(all_results) == 2


class TestProductSearch:
    """Test FTS5 product search functionality."""
    
    @pytest.fixture
    def loaded_cache(self):
        """Create cache with sample truck stop products."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache_instance = ProductCache(str(db_path))
            cache_instance.initialize()
            
            # Load sample products
            products = [
                Product(
                    sku="FUEL-DIESEL-001",
                    name="Diesel Fuel - Premium",
                    category="Fuel & Fluids",
                    location="Fuel Island 1",
                    price=3.89,
                    description="Premium diesel fuel for commercial trucks"
                ),
                Product(
                    sku="FUEL-DEF-001",
                    name="BlueDEF Diesel Exhaust Fluid",
                    category="Fuel & Fluids",
                    location="Fuel Island 2",
                    price=12.99,
                    description="DEF fluid meets ISO 22241 standards"
                ),
                Product(
                    sku="ELECT-CB-105",
                    name="Cobra 29 LX CB Radio",
                    category="Electronics",
                    location="Aisle 4",
                    price=129.99,
                    description="40-channel CB radio with weather alerts"
                ),
                Product(
                    sku="SERV-SHOWER-001",
                    name="Shower Credit - 30 Minutes",
                    category="Services",
                    location="Service Desk",
                    price=15.00,
                    description="Clean private shower for longhaul drivers"
                ),
            ]
            cache_instance.insert_products(products)
            
            yield cache_instance
            # Close connection to release file lock (important on Windows)
            cache_instance.close()
    
    def test_search_by_name(self, loaded_cache):
        """Test searching by product name."""
        results = loaded_cache.search_products("diesel")
        assert len(results) >= 1
        assert any("diesel" in r.name.lower() or "diesel" in r.description.lower() for r in results)
    
    def test_search_by_category(self, loaded_cache):
        """Test searching by category."""
        results = loaded_cache.search_products("electronics")
        assert len(results) >= 1
        assert all(r.category == "Electronics" for r in results)
    
    def test_search_by_sku(self, loaded_cache):
        """Test exact SKU match."""
        # Use quotes for exact phrase match in FTS5
        results = loaded_cache.search_products('"FUEL DEF 001"')
        assert len(results) >= 1
    
    def test_search_multi_word(self, loaded_cache):
        """Test multi-word search with BM25 ranking."""
        results = loaded_cache.search_products("CB radio")
        assert len(results) >= 1
        # CB Radio should rank highly
        assert "CB" in results[0].name or "radio" in results[0].name.lower()
    
    def test_search_description_keywords(self, loaded_cache):
        """Test searching by description keywords."""
        results = loaded_cache.search_products("longhaul")
        assert len(results) >= 1
        assert any("driver" in r.description.lower() for r in results)
    
    def test_search_no_results(self, loaded_cache):
        """Test search with no matches returns empty list."""
        results = loaded_cache.search_products("xyzabc123")
        assert len(results) == 0
        assert isinstance(results, list)
    
    def test_search_max_results_limit(self, loaded_cache):
        """Test that max_results parameter limits results."""
        results = loaded_cache.search_products("fuel", max_results=1)
        assert len(results) <= 1
    
    def test_search_returns_relevance_score(self, loaded_cache):
        """Test that search results include relevance scores."""
        results = loaded_cache.search_products("diesel")
        assert len(results) > 0
        for result in results:
            assert result.relevance_score is not None
            assert isinstance(result.relevance_score, float)


class TestPerformance:
    """Test search performance requirements."""
    
    @pytest.fixture
    def large_cache(self):
        """Create cache with 50 products for performance testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache_instance = ProductCache(str(db_path))
            cache_instance.initialize()
            
            # Generate 50 products
            products = []
            for i in range(50):
                products.append(Product(
                    sku=f"TEST-{i:03d}",
                    name=f"Test Product {i}",
                    category="Test Category",
                    location=f"Aisle {i % 10}",
                    price=float(i + 1),
                    description=f"Test description for product {i}"
                ))
            
            cache_instance.insert_products(products)
            yield cache_instance
            # Close connection to release file lock (important on Windows)
            cache_instance.close()
    
    def test_search_performance_under_100ms(self, large_cache):
        """Test that search completes in <100ms (NFR4)."""
        import time
        
        start = time.time()
        results = large_cache.search_products("test")
        latency_ms = (time.time() - start) * 1000
        
        assert latency_ms < 100, f"Search took {latency_ms:.2f}ms, should be <100ms"
        assert len(results) > 0


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    @pytest.fixture
    def cache(self):
        """Create temporary cache."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache_instance = ProductCache(str(db_path))
            cache_instance.initialize()
            yield cache_instance
            # Close connection to release file lock (important on Windows)
            cache_instance.close()
    
    def test_search_empty_database(self, cache):
        """Test searching empty database returns empty list."""
        results = cache.search_products("anything")
        assert len(results) == 0
    
    def test_search_empty_query(self, cache):
        """Test searching with empty query."""
        results = cache.search_products("")
        assert len(results) == 0
    
    def test_search_special_characters(self, cache):
        """Test searching with special characters doesn't crash."""
        # Should not raise exception
        results = cache.search_products("test@#$%")
        assert isinstance(results, list)
