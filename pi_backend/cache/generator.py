"""Cache generation stub for edge sync."""
from datetime import datetime, timezone


def generate_cache(domain: str, store_id: str) -> dict:
    return {
        "cache_version": f"v0-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "domain": domain,
        "store_id": store_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "products": [],
        "promos": [],
        "l1_seed": [],
        "config": {"cache_ttl": 86400},
    }
