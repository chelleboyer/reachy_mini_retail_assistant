"""L2 Cache - SQLite FTS5 Product Storage.

Provides persistent product storage with full-text search capabilities using SQLite's
FTS5 extension and BM25 ranking algorithm for relevance scoring.

Performance target: <100ms search latency (NFR4)
"""
import sqlite3
import threading
from pathlib import Path
from typing import List, Optional
import structlog

from models import Product

logger = structlog.get_logger(__name__)


class ProductCache:
    """SQLite FTS5-based product cache with full-text search.
    
    Implements L2 cache tier for persistent product storage with fast full-text
    search capabilities. Uses FTS5 virtual tables with BM25 ranking for relevance.
    
    Thread Safety:
        NOT thread-safe. SQLite connections are not thread-safe by default.
        For multi-threaded use (e.g., FastAPI with workers), create one
        ProductCache instance per thread/request.
    
    Attributes:
        db_path: Path to SQLite database file
        _conn: Database connection (lazy-initialized)
    """
    
    def __init__(self, db_path: str = "data/products.db"):
        """Initialize product cache.
        
        Args:
            db_path: Path to SQLite database file (created if doesn't exist)
        """
        self.db_path = Path(db_path)
        self._conn: Optional[sqlite3.Connection] = None
        logger.info("product_cache_initialized", db_path=str(self.db_path))
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection.
        
        Returns:
            Active SQLite connection
        """
        if self._conn is None:
            # Ensure parent directory exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row  # Enable column access by name
            logger.debug("database_connection_created", db_path=str(self.db_path))
        
        return self._conn
    
    def initialize(self) -> None:
        """Initialize database schema with FTS5 virtual table.
        
        Creates the products_fts FTS5 virtual table if it doesn't exist.
        Safe to call multiple times (idempotent).
        
        Schema:
            - sku: Product SKU (searchable)
            - name: Product name (searchable)
            - category: Product category (searchable)
            - location: Store location (searchable)
            - price: Price in USD (UNINDEXED - not searchable)
            - description: Full product description (searchable)
        
        Uses porter stemming and unicode61 tokenizer for better search quality.
        """
        conn = self._get_connection()
        
        # Create FTS5 virtual table with BM25 ranking
        # UNINDEXED on price since we don't search by price
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS products_fts USING fts5(
                sku,
                name,
                category,
                location,
                price UNINDEXED,
                description,
                tokenize='porter unicode61'
            )
        """)
        
        conn.commit()
        logger.info("database_initialized", table="products_fts", tokenizer="porter unicode61")
    
    def insert_product(self, product: Product) -> None:
        """Insert a single product into the cache.
        
        Args:
            product: Product model to insert
        
        Raises:
            sqlite3.IntegrityError: If database operation fails
        
        Note:
            Does not check for duplicate SKUs. FTS5 virtual tables do not
            support PRIMARY KEY constraints. Consider checking manually if needed.
        """
        conn = self._get_connection()
        
        try:
            conn.execute("""
                INSERT INTO products_fts (sku, name, category, location, price, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                product.sku,
                product.name,
                product.category,
                product.location,
                product.price,
                product.description
            ))
            
            conn.commit()
            logger.debug("product_inserted", sku=product.sku, name=product.name)
        except Exception as e:
            conn.rollback()
            logger.error("product_insert_failed", sku=product.sku, error=str(e))
            raise
    
    def insert_products(self, products: List[Product]) -> None:
        """Bulk insert multiple products into the cache.
        
        Args:
            products: List of Product models to insert
        
        Raises:
            sqlite3.IntegrityError: If database operation fails
        
        Note:
            Transaction is atomic - either all products are inserted or none.
            Rolls back on any error to maintain database consistency.
        """
        conn = self._get_connection()
        
        try:
            # Batch insert for better performance
            data = [
                (p.sku, p.name, p.category, p.location, p.price, p.description)
                for p in products
            ]
            
            conn.executemany("""
                INSERT INTO products_fts (sku, name, category, location, price, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data)
            
            conn.commit()
            logger.info("products_bulk_inserted", count=len(products))
        except Exception as e:
            conn.rollback()
            logger.error("products_bulk_insert_failed", error=str(e), count=len(products))
            raise
    
    def search_products(self, query: str, max_results: int = 5) -> List[Product]:
        """Search products using FTS5 full-text search with BM25 ranking.
        
        Searches across sku, name, category, location, and description fields.
        Results are ranked by relevance using BM25 algorithm.
        
        Args:
            query: Search query string (can be multi-word)
            max_results: Maximum number of results to return (default: 5)
        
        Returns:
            List of matching Product models, ordered by relevance (highest first)
            Empty list if no matches or empty query
        
        Performance:
            Target latency: <100ms for up to 50 products (NFR4)
        """
        # Handle empty query
        if not query or not query.strip():
            return []
        
        conn = self._get_connection()
        
        try:
            # FTS5 search with BM25 ranking
            # bm25() returns negative scores, lower (more negative) = more relevant
            cursor = conn.execute("""
                SELECT sku, name, category, location, price, description,
                       bm25(products_fts) as relevance_score
                FROM products_fts
                WHERE products_fts MATCH ?
                ORDER BY bm25(products_fts)
                LIMIT ?
            """, (query, max_results))
            
            results = []
            for row in cursor.fetchall():
                # Convert BM25 score (negative) to positive relevance score
                # More negative = more relevant, so negate and add offset
                relevance = abs(float(row['relevance_score']))
                
                product = Product(
                    sku=row['sku'],
                    name=row['name'],
                    category=row['category'],
                    location=row['location'],
                    price=float(row['price']),
                    description=row['description'],
                    relevance_score=relevance
                )
                results.append(product)
            
            logger.debug(
                "search_completed",
                query=query,
                result_count=len(results),
                max_results=max_results
            )
            
            return results
        
        except sqlite3.OperationalError as e:
            # Handle FTS5 query syntax errors gracefully
            logger.warning("search_failed", query=query, error=str(e))
            return []
    
    def close(self) -> None:
        """Close database connection.
        
        Should be called when cache is no longer needed to release resources.
        """
        if self._conn:
            self._conn.close()
            self._conn = None
            logger.debug("database_connection_closed", db_path=str(self.db_path))
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures connection is closed."""
        self.close()


class ThreadSafeProductCache:
    """Thread-safe wrapper for ProductCache using thread-local storage.
    
    Creates one ProductCache instance per thread, ensuring SQLite connection
    safety in multi-threaded environments (e.g., FastAPI with multiple workers).
    
    Usage:
        # Create shared cache instance
        cache = ThreadSafeProductCache("data/cache.db")
        
        # Each thread gets its own connection automatically
        cache.initialize()
        results = cache.search_products("diesel")
    
    Note:
        For FastAPI applications, prefer using dependency injection with
        request-scoped ProductCache instances instead of this wrapper.
    """
    
    def __init__(self, db_path: str = "data/products.db"):
        """Initialize thread-safe cache wrapper.
        
        Args:
            db_path: Path to SQLite database file (shared across threads)
        """
        self.db_path = db_path
        self._local = threading.local()
        logger.info("thread_safe_cache_initialized", db_path=self.db_path)
    
    def _get_cache(self) -> ProductCache:
        """Get or create ProductCache for current thread.
        
        Returns:
            ProductCache instance for current thread
        """
        if not hasattr(self._local, 'cache'):
            self._local.cache = ProductCache(self.db_path)
            logger.debug("thread_local_cache_created", thread_id=threading.get_ident())
        return self._local.cache
    
    def initialize(self) -> None:
        """Initialize database schema (thread-safe)."""
        self._get_cache().initialize()
    
    def insert_product(self, product: Product) -> None:
        """Insert single product (thread-safe)."""
        self._get_cache().insert_product(product)
    
    def insert_products(self, products: List[Product]) -> None:
        """Bulk insert products (thread-safe)."""
        self._get_cache().insert_products(products)
    
    def search_products(self, query: str, max_results: int = 5) -> List[Product]:
        """Search products (thread-safe)."""
        return self._get_cache().search_products(query, max_results)
    
    def close(self) -> None:
        """Close current thread's connection."""
        if hasattr(self._local, 'cache'):
            self._local.cache.close()
            delattr(self._local, 'cache')
    
    def close_all(self) -> None:
        """Close all thread-local connections.
        
        Note: Only closes the current thread's connection since we can't
        access other threads' local storage. Each thread should call close()
        when done.
        """
        self.close()
        logger.info("thread_safe_cache_closed", db_path=self.db_path)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes current thread's connection."""
        self.close()

