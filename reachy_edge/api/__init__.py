"""Public API routes for Karen Whisperer integration.

These endpoints provide the clean REST interface that Karen Whisperer's
custom tools call over HTTP to access product, promo, and store data.

Endpoints:
    GET /api/products/search?q=...&limit=5  → Product search
    GET /api/promos/active?limit=3          → Active promotions
    GET /api/store/info                     → Store configuration
"""
from .routes import router

__all__ = ["router"]
