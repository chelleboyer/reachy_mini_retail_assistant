"""Tests for L2 Cache (SQLite FTS5) product storage."""
import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime
import threading
import time

# Will fail until we create the l2_cache module
from cache.l2_cache import ProductCache, ThreadSafeProductCache
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


class TestDuplicateHandling:
    """Test duplicate SKU behavior."""
    
    @pytest.fixture
    def cache(self):
        """Create temporary cache for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache_instance = ProductCache(str(db_path))
            cache_instance.initialize()
            yield cache_instance
            cache_instance.close()
    
    def test_duplicate_sku_insertion(self, cache):
        """Test that duplicate SKUs are allowed (FTS5 limitation)."""
        product1 = Product(
            sku="FUEL-DEF-001",
            name="BlueDEF Diesel Exhaust Fluid",
            category="Fuel & Fluids",
            location="Fuel Island 2",
            price=12.99,
            description="Premium DEF fluid"
        )
        product2 = Product(
            sku="FUEL-DEF-001",  # Same SKU
            name="Different Product",
            category="Different Category",
            location="Different Location",
            price=99.99,
            description="Different description"
        )
        
        # Both should insert successfully (FTS5 has no PRIMARY KEY constraint)
        cache.insert_product(product1)
        cache.insert_product(product2)
        
        # Search should return both (use quoted string for hyphenated SKU)
        results = cache.search_products('"FUEL-DEF-001"')
        assert len(results) == 2, "FTS5 allows duplicate SKUs"


class TestTransactionRollback:
    """Test transaction rollback on errors."""
    
    @pytest.fixture
    def cache(self):
        """Create temporary cache for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache_instance = ProductCache(str(db_path))
            cache_instance.initialize()
            yield cache_instance
            cache_instance.close()
    
    def test_insert_rollback_on_error(self, cache):
        """Test that failed insert rolls back transaction."""
        # Insert a valid product first
        valid_product = Product(
            sku="VALID-001",
            name="Valid Product",
            category="Test",
            location="Test Location",
            price=10.0,
            description="Valid product"
        )
        cache.insert_product(valid_product)
        
        # Corrupt the connection to force an error
        # Close and set to invalid object to trigger exception
        original_conn = cache._conn
        cache._conn = "not a connection"  # This will cause execute() to fail
        
        invalid_product = Product(
            sku="INVALID-001",
            name="Invalid Product",
            category="Test",
            location="Test Location",
            price=20.0,
            description="Should fail"
        )
        
        # This should raise an AttributeError
        with pytest.raises(AttributeError):
            cache.insert_product(invalid_product)
        
        # Restore connection and verify only valid product exists
        cache._conn = original_conn
        results = cache.search_products('"VALID-001"')
        assert len(results) == 1
        results = cache.search_products('"INVALID-001"')
        assert len(results) == 0


class TestContextManager:
    """Test context manager lifecycle."""
    
    def test_context_manager_opens_and_closes(self):
        """Test that context manager properly initializes and closes connection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            
            with ProductCache(str(db_path)) as cache:
                cache.initialize()
                
                # Insert a product
                product = Product(
                    sku="CTX-001",
                    name="Context Test Product",
                    category="Test",
                    location="Test Location",
                    price=15.0,
                    description="Testing context manager"
                )
                cache.insert_product(product)
                
                # Verify it was inserted (use quoted string for hyphenated SKU)
                results = cache.search_products('"CTX-001"')
                assert len(results) == 1
                assert cache._conn is not None, "Connection should be active"
            
            # After context exit, connection should be closed
            assert cache._conn is None, "Connection should be closed after context exit"
    
    def test_context_manager_closes_on_exception(self):
        """Test that context manager closes connection even on exception."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            
            try:
                with ProductCache(str(db_path)) as cache:
                    cache.initialize()
                    # Raise an exception
                    raise ValueError("Test exception")
            except ValueError:
                pass  # Expected
            
            # Connection should still be closed
            assert cache._conn is None, "Connection should be closed even after exception"


class TestThreadSafety:
    """Test thread-safe cache wrapper."""
    
    def test_thread_local_connections(self):
        """Test that each thread gets its own connection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache = ThreadSafeProductCache(str(db_path))
            cache.initialize()
            
            # Track thread IDs that successfully inserted
            results = []
            
            def insert_in_thread(thread_id: int):
                """Insert product from separate thread."""
                product = Product(
                    sku=f"THREAD-{thread_id:03d}",
                    name=f"Thread {thread_id} Product",
                    category="Test",
                    location="Test Location",
                    price=float(thread_id),
                    description=f"Product from thread {thread_id}"
                )
                cache.insert_product(product)
                results.append(thread_id)
                # Close this thread's connection
                cache.close()
            
            # Create multiple threads
            threads = []
            for i in range(5):
                t = threading.Thread(target=insert_in_thread, args=(i,))
                threads.append(t)
                t.start()
            
            # Wait for all threads to complete
            for t in threads:
                t.join()
            
            # Verify all threads succeeded
            assert len(results) == 5, "All threads should complete successfully"
            
            # Verify all products were inserted
            all_results = cache.search_products("Thread")
            assert len(all_results) >= 5, f"Should have at least 5 products, got {len(all_results)}"
            
            cache.close_all()
    
    def test_concurrent_searches(self):
        """Test concurrent searches from multiple threads."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_products.db"
            cache = ThreadSafeProductCache(str(db_path))
            cache.initialize()
            
            # Insert test products
            products = [
                Product(
                    sku=f"SEARCH-{i:03d}",
                    name=f"Search Product {i}",
                    category="Test",
                    location="Test Location",
                    price=float(i),
                    description="Test product for concurrent search"
                )
                for i in range(10)
            ]
            cache.insert_products(products)
            
            # Track search results from each thread
            search_results = []
            
            def search_in_thread():
                """Search from separate thread."""
                results = cache.search_products("Search Product")
                search_results.append(len(results))
                # Close this thread's connection
                cache.close()
            
            # Create multiple threads doing searches
            threads = []
            for i in range(10):
                t = threading.Thread(target=search_in_thread)
                threads.append(t)
                t.start()
            
            # Wait for all threads
            for t in threads:
                t.join()
            
            # All searches should return results
            assert len(search_results) == 10, "All search threads should complete"
            assert all(count > 0 for count in search_results), "All searches should find products"
            
            cache.close_all()
