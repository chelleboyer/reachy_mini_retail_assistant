"""L1 (hot) in-memory cache with TTL."""
import time
from typing import Optional, Dict, Any
from threading import Lock
import logging

logger = logging.getLogger(__name__)


class L1Cache:
    """Fast in-memory cache with TTL and LRU eviction."""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 300):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if exists and not expired."""
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            
            entry = self._cache[key]
            
            # Check TTL
            if time.time() - entry["timestamp"] > self.ttl_seconds:
                del self._cache[key]
                self._misses += 1
                return None
            
            # Update access time for LRU
            entry["last_access"] = time.time()
            self._hits += 1
            return entry["value"]
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp."""
        with self._lock:
            # Evict oldest if at capacity
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._evict_oldest()
            
            self._cache[key] = {
                "value": value,
                "timestamp": time.time(),
                "last_access": time.time()
            }
    
    def invalidate(self, key: Optional[str] = None) -> None:
        """Invalidate specific key or entire cache."""
        with self._lock:
            if key:
                self._cache.pop(key, None)
            else:
                self._cache.clear()
                logger.info("L1 cache invalidated")
    
    def _evict_oldest(self) -> None:
        """Evict least recently accessed entry."""
        if not self._cache:
            return
        
        oldest_key = min(
            self._cache.keys(),
            key=lambda k: self._cache[k]["last_access"]
        )
        del self._cache[oldest_key]
    
    def size(self) -> int:
        """Return current cache size."""
        with self._lock:
            return len(self._cache)
    
    def stats(self) -> Dict[str, Any]:
        """Return cache statistics."""
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0
            
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate_pct": round(hit_rate, 2)
            }
