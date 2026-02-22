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

from ..models import Product as SearchProduct
from .schemas import Product as CacheProduct, Promo

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

    def clear(self) -> None:
        """Delete all rows from the FTS5 table."""
        conn = self._get_connection()
        conn.execute("DELETE FROM products_fts")
        conn.commit()
        logger.info("database_cleared", table="products_fts")

    def insert_product(self, product: SearchProduct) -> None:
        """Insert a single product into the FTS5 cache.
        
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
    
    def insert_products(self, products: List[SearchProduct]) -> None:
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
    
    def search_products(self, query: str, max_results: int = 5) -> List[SearchProduct]:
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
                
                product = SearchProduct(
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
    
    def get_all_products(self, limit: int = 100) -> List[SearchProduct]:
        """Return all products (unranked), limited by *limit*."""
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT sku, name, category, location, price, description FROM products_fts LIMIT ?",
                (limit,),
            )
            return [
                SearchProduct(
                    sku=row["sku"],
                    name=row["name"],
                    category=row["category"],
                    location=row["location"],
                    price=float(row["price"]),
                    description=row["description"],
                )
                for row in cursor.fetchall()
            ]
        except Exception:
            return []

    def product_count(self) -> int:
        """Return total number of products in the FTS5 table."""
        conn = self._get_connection()
        try:
            row = conn.execute("SELECT count(*) AS c FROM products_fts").fetchone()
            return int(row["c"]) if row else 0
        except Exception:
            return 0

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
    
    def insert_product(self, product: SearchProduct) -> None:
        """Insert single product (thread-safe)."""
        self._get_cache().insert_product(product)
    
    def insert_products(self, products: List[SearchProduct]) -> None:
        """Bulk insert products (thread-safe)."""
        self._get_cache().insert_products(products)

    def clear(self) -> None:
        """Clear all products (thread-safe)."""
        self._get_cache().clear()

    def search_products(self, query: str, max_results: int = 5) -> List[SearchProduct]:
        """Search products (thread-safe)."""
        return self._get_cache().search_products(query, max_results)

    def get_all_products(self, limit: int = 100) -> List[SearchProduct]:
        """Return all products (thread-safe)."""
        return self._get_cache().get_all_products(limit)

    def product_count(self) -> int:
        """Return product count (thread-safe)."""
        return self._get_cache().product_count()

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



class L2Cache:
    """Async-friendly cache facade used by FastAPI app and tools.

    This wraps ProductCache (FTS5 search) and a lightweight promo/version store
    to provide the methods used by the interaction layer.
    """

    def __init__(self, db_path: str = "./data/cache.db"):
        self.db_path = db_path
        self._products = ThreadSafeProductCache(db_path)
        self._products.initialize()
        self._promos: dict[str, Promo] = {}
        self._version: str = "v0"

    @staticmethod
    def _to_search_product(product: CacheProduct) -> SearchProduct:
        """Convert cache schema product to FTS search product model."""
        location = product.aisle if product.aisle.lower().startswith("aisle") else f"Aisle {product.aisle}"
        return SearchProduct(
            sku=product.sku,
            name=product.name,
            category=product.category,
            location=location,
            price=product.price or 0.0,
            description=product.description or "",
        )

    @staticmethod
    def _extract_aisle(location: str) -> str:
        """Extract aisle token from location string."""
        lower = location.lower().strip()
        if lower.startswith("aisle"):
            parts = location.split(maxsplit=1)
            return parts[1] if len(parts) > 1 else location
        return location

    @staticmethod
    def _to_cache_product(product: SearchProduct) -> CacheProduct:
        """Convert FTS search product model to cache schema product."""
        return CacheProduct(
            sku=product.sku,
            name=product.name,
            aisle=L2Cache._extract_aisle(product.location),
            category=product.category,
            price=product.price,
            description=product.description,
        )

    async def update_products(self, products: list[CacheProduct]) -> None:
        """Replace product cache with new set of products."""
        self._products.initialize()
        self._products.clear()
        search_products = [self._to_search_product(p) for p in products]
        self._products.insert_products(search_products)

    async def search_products(self, query: str, max_results: int = 5) -> list[SearchProduct]:
        """Search products using FTS5 full-text search with BM25 ranking.

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of matching products ordered by relevance
        """
        return self._products.search_products(query, max_results=max_results)

    async def get_all_products(self, limit: int = 100) -> list[SearchProduct]:
        """Return all products (unranked), limited by *limit*."""
        return self._products.get_all_products(limit)

    async def search_product(self, query: str) -> Optional[CacheProduct]:
        """Find the best matching product for a query."""
        results = self._products.search_products(query, max_results=1)
        if not results:
            return None
        return self._to_cache_product(results[0])

    async def update_promos(self, promos: list[Promo]) -> None:
        """Upsert promotions in memory."""
        for promo in promos:
            self._promos[promo.id] = promo

    async def get_active_promos(self, limit: int = 3) -> list[Promo]:
        """Return active promotions sorted by priority desc."""
        ordered = sorted(self._promos.values(), key=lambda p: p.priority, reverse=True)
        return ordered[:limit]

    async def set_version(self, version: str) -> None:
        """Set sync version marker."""
        self._version = version

    async def preload_hot_data(self, l1_cache) -> None:
        """Preload frequently used keys into L1 cache."""
        promos = await self.get_active_promos(limit=3)
        if promos:
            l1_cache.set("active_promos", promos)

    def stats(self) -> dict:
        """Expose cache stats for health checks."""
        return {
            "version": self._version,
            "product_count": self._products.product_count(),
            "promo_count": len(self._promos),
            "status": "active",
        }
