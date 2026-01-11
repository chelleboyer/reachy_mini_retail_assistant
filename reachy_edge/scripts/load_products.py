#!/usr/bin/env python3
"""Load sample product data into L2 cache (SQLite FTS5 database).

Usage:
    python scripts/load_products.py [--db-path PATH]
    
Options:
    --db-path PATH    Path to database file (default: ./data/cache.db)
"""
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cache.l2_cache import ProductCache
from data.sample_products import load_sample_data
import structlog

logger = structlog.get_logger(__name__)


def main():
    """Load sample products into database."""
    parser = argparse.ArgumentParser(
        description="Load sample truck stop products into L2 cache"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="./data/cache.db",
        help="Path to database file (default: ./data/cache.db)"
    )
    args = parser.parse_args()
    
    db_path = args.db_path
    
    logger.info("initializing_database", db_path=db_path)
    
    # Initialize cache
    with ProductCache(db_path) as cache:
        cache.initialize()
        
        # Load sample data
        logger.info("loading_sample_products")
        count = load_sample_data(cache)
        
        logger.info("products_loaded", count=count, db_path=db_path)
        
        # Verify with test queries
        logger.info("verifying_with_test_queries")
        
        test_queries = [
            "diesel",
            "CB radio",
            "shower",
            "pizza",
            "safety vest"
        ]
        
        for query in test_queries:
            results = cache.search_products(query, max_results=3)
            logger.info(
                "test_query_results",
                query=query,
                result_count=len(results),
                top_result=results[0].name if results else None
            )
    
    print(f"\n✅ Successfully loaded {count} products into {db_path}")
    print("\nTest query example:")
    print(f"  Results for 'diesel': {len([r for r in cache.search_products('diesel') if r])} products")


if __name__ == "__main__":
    main()
