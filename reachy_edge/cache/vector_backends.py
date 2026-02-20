"""Pluggable L2 backends for product retrieval."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import math
import sqlite3

from .schemas import Product as CacheProduct


class ProductRetrievalBackend(ABC):
    @abstractmethod
    def upsert_products(self, products: list[CacheProduct]) -> None:
        pass

    @abstractmethod
    def search_one(self, query: str) -> Optional[CacheProduct]:
        pass

    @abstractmethod
    def stats(self) -> dict:
        pass


class SQLiteKeywordBackend(ProductRetrievalBackend):
    """SQLite FTS-backed backend with light aisle schema mapping."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        if self._conn is None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _init_db(self) -> None:
        conn = self._connect()
        conn.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS products_fts USING fts5(
                sku,
                name,
                category,
                location,
                price UNINDEXED,
                description,
                tokenize='porter unicode61'
            )
            """
        )
        conn.commit()

    @staticmethod
    def _to_location(aisle: str) -> str:
        return aisle if aisle.lower().startswith("aisle") else f"Aisle {aisle}"

    @staticmethod
    def _to_aisle(location: str) -> str:
        low = location.lower().strip()
        if low.startswith("aisle"):
            parts = location.split(maxsplit=1)
            return parts[1] if len(parts) > 1 else location
        return location

    def upsert_products(self, products: list[CacheProduct]) -> None:
        conn = self._connect()
        conn.execute("DELETE FROM products_fts")
        rows = [
            (
                p.sku,
                p.name,
                p.category,
                self._to_location(p.aisle),
                p.price,
                p.description or "",
            )
            for p in products
        ]
        conn.executemany(
            """
            INSERT INTO products_fts (sku, name, category, location, price, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()

    def search_one(self, query: str) -> Optional[CacheProduct]:
        if not query.strip():
            return None
        conn = self._connect()
        cursor = conn.execute(
            """
            SELECT sku, name, category, location, price, description
            FROM products_fts
            WHERE products_fts MATCH ?
            ORDER BY bm25(products_fts)
            LIMIT 1
            """,
            (query,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return CacheProduct(
            sku=row["sku"],
            name=row["name"],
            aisle=self._to_aisle(row["location"]),
            category=row["category"],
            price=row["price"],
            description=row["description"],
        )

    def stats(self) -> dict:
        return {"backend": "sqlite"}


class QdrantVectorBackend(ProductRetrievalBackend):
    """Optional Qdrant-backed backend with graceful local fallback."""

    def __init__(self, url: str, collection: str, embedding_dim: int):
        self.url = url
        self.collection = collection
        self.embedding_dim = embedding_dim
        self._products: dict[str, CacheProduct] = {}
        self._client = None
        self._init_client()

    def _init_client(self) -> None:
        try:
            from qdrant_client import QdrantClient  # type: ignore

            self._client = QdrantClient(url=self.url)
        except Exception:
            self._client = None

    @staticmethod
    def _embed(text: str, dim: int) -> list[float]:
        vec = [0.0] * dim
        if not text:
            return vec
        for idx, ch in enumerate(text.lower()):
            vec[idx % dim] += (ord(ch) % 31) / 31.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def _ensure_collection(self) -> None:
        if not self._client:
            return
        try:
            from qdrant_client.models import VectorParams, Distance  # type: ignore

            self._client.recreate_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=self.embedding_dim, distance=Distance.COSINE),
            )
        except Exception:
            self._client = None

    def upsert_products(self, products: list[CacheProduct]) -> None:
        for p in products:
            self._products[p.sku] = p

        if not self._client:
            return

        self._ensure_collection()
        try:
            from qdrant_client.models import PointStruct  # type: ignore

            points = []
            for idx, p in enumerate(products):
                text = f"{p.sku} {p.name} {p.category} {p.aisle} {p.description or ''}"
                points.append(
                    PointStruct(
                        id=idx,
                        vector=self._embed(text, self.embedding_dim),
                        payload={
                            "sku": p.sku,
                            "name": p.name,
                            "aisle": p.aisle,
                            "category": p.category,
                            "price": p.price,
                            "description": p.description,
                        },
                    )
                )
            self._client.upsert(collection_name=self.collection, points=points)
        except Exception:
            self._client = None

    def search_one(self, query: str) -> Optional[CacheProduct]:
        if self._client:
            try:
                hits = self._client.search(
                    collection_name=self.collection,
                    query_vector=self._embed(query, self.embedding_dim),
                    limit=1,
                )
                if hits:
                    payload = hits[0].payload
                    return CacheProduct(
                        sku=str(payload.get("sku", "")),
                        name=str(payload.get("name", "")),
                        aisle=str(payload.get("aisle", "")),
                        category=str(payload.get("category", "")),
                        price=payload.get("price"),
                        description=payload.get("description"),
                    )
            except Exception:
                self._client = None

        q = query.lower().strip()
        for p in self._products.values():
            hay = f"{p.sku} {p.name} {p.category} {p.aisle} {p.description or ''}".lower()
            if q in hay:
                return p
        return next(iter(self._products.values()), None)

    def stats(self) -> dict:
        return {
            "backend": "qdrant",
            "client_enabled": self._client is not None,
            "cached_products": len(self._products),
        }
