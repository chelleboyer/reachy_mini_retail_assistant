"""L2 persistent cache using SQLite with FTS5."""
import sqlite3
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
import logging
from datetime import datetime

from cache.schemas import Product, Promo

logger = logging.getLogger(__name__)


class L2Cache:
    """SQLite-based persistent cache with full-text search."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_db_exists()
        self._init_schema()
        self._version = self._load_version()
    
    def _ensure_db_exists(self) -> None:
        """Ensure database file and directory exist."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_schema(self) -> None:
        """Initialize database schema with FTS5 for fast search."""
        with self._get_connection() as conn:
            # Products table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    sku TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    aisle TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # FTS5 virtual table for product search
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS products_fts USING fts5(
                    sku, name, category, description,
                    content='products',
                    content_rowid='rowid'
                )
            """)
            
            # Promos table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS promos (
                    id TEXT PRIMARY KEY,
                    description TEXT NOT NULL,
                    sku TEXT,
                    category TEXT,
                    discount_percent REAL,
                    expiry TIMESTAMP,
                    priority INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Metadata table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def _load_version(self) -> str:
        """Load current cache version."""
        with self._get_connection() as conn:
            result = conn.execute(
                "SELECT value FROM metadata WHERE key = 'version'"
            ).fetchone()
            return result["value"] if result else "0.0.0"
    
    async def search_product(self, query: str) -> Optional[Product]:
        """Search for product using FTS5."""
        with self._get_connection() as conn:
            # Try FTS search first
            result = conn.execute("""
                SELECT p.* FROM products p
                JOIN products_fts ON products_fts.rowid = p.rowid
                WHERE products_fts MATCH ?
                ORDER BY rank
                LIMIT 1
            """, (query,)).fetchone()
            
            if not result:
                # Fallback to LIKE search
                result = conn.execute("""
                    SELECT * FROM products
                    WHERE name LIKE ? OR category LIKE ? OR description LIKE ?
                    LIMIT 1
                """, (f"%{query}%", f"%{query}%", f"%{query}%")).fetchone()
            
            if result:
                return Product(**dict(result))
            return None
    
    async def get_active_promos(self, limit: int = 3) -> List[Promo]:
        """Get active promotions sorted by priority."""
        with self._get_connection() as conn:
            results = conn.execute("""
                SELECT * FROM promos
                WHERE expiry IS NULL OR expiry > ?
                ORDER BY priority DESC, created_at DESC
                LIMIT ?
            """, (datetime.utcnow(), limit)).fetchall()
            
            return [Promo(**dict(row)) for row in results]
    
    async def update_products(self, products: List[Product]) -> None:
        """Bulk update products."""
        with self._get_connection() as conn:
            for product in products:
                conn.execute("""
                    INSERT OR REPLACE INTO products (sku, name, aisle, category, price, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    product.sku,
                    product.name,
                    product.aisle,
                    product.category,
                    product.price,
                    product.description
                ))
            
            # Rebuild FTS index
            conn.execute("INSERT INTO products_fts(products_fts) VALUES('rebuild')")
            conn.commit()
            
        logger.info(f"Updated {len(products)} products in L2 cache")
    
    async def update_promos(self, promos: List[Promo]) -> None:
        """Bulk update promotions."""
        with self._get_connection() as conn:
            for promo in promos:
                conn.execute("""
                    INSERT OR REPLACE INTO promos (id, description, sku, category, discount_percent, expiry, priority)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    promo.id,
                    promo.description,
                    promo.sku,
                    promo.category,
                    promo.discount_percent,
                    promo.expiry,
                    promo.priority
                ))
            conn.commit()
        
        logger.info(f"Updated {len(promos)} promos in L2 cache")
    
    async def set_version(self, version: str) -> None:
        """Update cache version."""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO metadata (key, value, updated_at)
                VALUES ('version', ?, ?)
            """, (version, datetime.utcnow()))
            conn.commit()
        
        self._version = version
    
    def version(self) -> str:
        """Get current cache version."""
        return self._version
    
    async def preload_hot_data(self, l1_cache: Any) -> None:
        """Preload frequently accessed data into L1 cache."""
        # Get top products by some heuristic (for now, just recent ones)
        with self._get_connection() as conn:
            results = conn.execute("""
                SELECT * FROM products
                ORDER BY created_at DESC
                LIMIT 100
            """).fetchall()
            
            for row in results:
                product = Product(**dict(row))
                # Cache by product name for quick lookup
                l1_cache.set(f"product:{product.name.lower()}", product)
        
        # Preload active promos
        promos = await self.get_active_promos(limit=10)
        l1_cache.set("active_promos", promos)
        
        logger.info(f"Preloaded hot data into L1 cache")
