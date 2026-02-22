"""Smoke test: simulate Karen Whisperer tool calls against the live server."""
import httpx
import asyncio
import os

RETAIL_API_URL = os.getenv("RETAIL_API_URL", "http://localhost:8080")


async def simulate_kw_tools():
    async with httpx.AsyncClient(timeout=5.0) as client:
        print("=== KW Tool: get_store_info ===")
        r = await client.get(f"{RETAIL_API_URL}/api/store/info")
        store = r.json()
        print(f"  Store: {store['name']} | Hours: {store['hours']} | {store['product_count']} products | Status: {store['status']}")
        print(f"  Categories: {', '.join(store['categories'])}")
        print()

        print('=== KW Tool: lookup_product("beef jerky") ===')
        r = await client.get(f"{RETAIL_API_URL}/api/products/search", params={"q": "beef jerky", "limit": 3})
        data = r.json()
        print(f"  Found {data['result_count']} products in {data['search_time_ms']}ms:")
        for p in data["products"]:
            print(f"    - {p['name']} | ${p['price']} | {p['location']} (SKU: {p['sku']})")
        print()

        if data["products"]:
            sku = data["products"][0]["sku"]
            print(f'=== KW Tool: get_active_promos(product_sku="{sku}") ===')
            r = await client.get(f"{RETAIL_API_URL}/api/promos/active", params={"product_sku": sku})
            promos = r.json()
            print(f"  {promos['count']} active promos for {sku}")
            print()

        print('=== KW Tool: lookup_product("diesel") ===')
        r = await client.get(f"{RETAIL_API_URL}/api/products/search", params={"q": "diesel", "limit": 3})
        data = r.json()
        print(f"  Found {data['result_count']} products:")
        for p in data["products"]:
            print(f"    - {p['name']} | ${p['price']} | {p['location']}")
        print()

        print('=== Error path: graceful empty result ===')
        r = await client.get(f"{RETAIL_API_URL}/api/products/search", params={"q": "unicorn tears", "limit": 3})
        data = r.json()
        print(f'  Query "unicorn tears" -> {data["result_count"]} results (no crash)')
        print()
        print("ALL KW TOOL SIMULATIONS PASSED")


asyncio.run(simulate_kw_tools())
