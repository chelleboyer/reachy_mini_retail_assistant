"""Integration test: Karen Whisperer (robot) + Edge Backend (API).

Usage:
    # 1. Start the Edge Backend in one terminal:
    #    cd reachy_mini_retail_assistant
    #    python -m reachy_edge.main
    #
    # 2. Run this test in another terminal:
    #    python test_robot_backend.py              # API-only (no robot)
    #    python test_robot_backend.py --robot       # API + live robot
    #    python test_robot_backend.py --robot --talk # Full: API + robot + voice (needs OPENAI_API_KEY)

Phases:
    Phase 1 — Backend API health & endpoints (always runs)
    Phase 2 — Karen Whisperer tools against live API (always runs)
    Phase 3 — Robot connection + gestures (--robot flag)
    Phase 4 — Full conversation loop hint (--talk flag, manual)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
EDGE_API_URL = os.getenv("RETAIL_API_URL", "http://localhost:8000")
TIMEOUT = 5.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def ok(label: str, detail: str = "") -> None:
    print(f"  [OK]  {label}" + (f"  ({detail})" if detail else ""))


def fail(label: str, detail: str = "") -> None:
    print(f"  [FAIL] {label}" + (f"  ({detail})" if detail else ""))


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# Phase 1 — Edge Backend API
# ---------------------------------------------------------------------------
async def phase1_backend_api() -> bool:
    """Verify the Edge Backend is running and endpoints respond."""
    section("Phase 1: Edge Backend API")
    passed = True

    async with httpx.AsyncClient(base_url=EDGE_API_URL, timeout=TIMEOUT) as client:
        # Health
        try:
            r = await client.get("/health")
            r.raise_for_status()
            data = r.json()
            ok("GET /health", f"status={data['status']}, version={data['version']}")
        except Exception as e:
            fail("GET /health", str(e))
            print(f"\n  *** Edge Backend not reachable at {EDGE_API_URL}")
            print(f"  *** Start it first:  python -m reachy_edge.main\n")
            return False

        # Root
        try:
            r = await client.get("/")
            r.raise_for_status()
            data = r.json()
            ok("GET /", f"reachy_id={data['reachy_id']}, store={data['store_id']}")
        except Exception as e:
            fail("GET /", str(e))
            passed = False

        # Store info
        try:
            r = await client.get("/api/store/info")
            r.raise_for_status()
            info = r.json()
            ok("GET /api/store/info", f"name={info['name']}, {info['product_count']} products, {info['promo_count']} promos")
        except Exception as e:
            fail("GET /api/store/info", str(e))
            passed = False

        # Product search
        for query in ["beef jerky", "diesel", "energy drink", "unicorn tears"]:
            try:
                r = await client.get("/api/products/search", params={"q": query, "limit": 3})
                r.raise_for_status()
                data = r.json()
                ok(f"search '{query}'", f"{data['result_count']} results in {data['search_time_ms']}ms")
            except Exception as e:
                fail(f"search '{query}'", str(e))
                passed = False

        # Promos
        try:
            r = await client.get("/api/promos/active", params={"limit": 3})
            r.raise_for_status()
            data = r.json()
            ok("GET /api/promos/active", f"{data['count']} promos")
        except Exception as e:
            fail("GET /api/promos/active", str(e))
            passed = False

        # Interact endpoint
        try:
            r = await client.post("/interact", json={"query": "where is the coffee?", "session_id": "test-001"})
            r.raise_for_status()
            data = r.json()
            ok("POST /interact", f"intent={data['intent']}, tool={data['tool_used']}, latency={data['latency_ms']:.0f}ms")
        except Exception as e:
            fail("POST /interact", str(e))
            passed = False

    return passed


# ---------------------------------------------------------------------------
# Phase 2 — Karen Whisperer profile tools (HTTP calls, no robot needed)
# ---------------------------------------------------------------------------
async def phase2_kw_tools() -> bool:
    """Instantiate the KW profile tools and run them against the live API."""
    section("Phase 2: Karen Whisperer Profile Tools → Edge Backend")

    # Add the conversation app source to sys.path so we can import the tools
    kw_root = Path(__file__).parent.parent / "reachy_mini_karen_whisperer"
    conv_src = kw_root / "src" / "reachy_mini_conversation_app" / "src"
    kw_src = kw_root / "src" / "reachy_mini_karen_whisperer"

    # Try multiple potential locations
    search_paths = [
        conv_src,
        kw_root / "src" / "reachy_mini_conversation_app" / "src",
        Path(__file__).parent.parent / "reachy_mini_karen_whisperer" / "src" / "reachy_mini_conversation_app" / "src",
    ]

    for p in search_paths:
        if p.exists() and str(p) not in sys.path:
            sys.path.insert(0, str(p))

    # Also add the profile directory itself
    profile_dir = conv_src / "reachy_mini_conversation_app" / "profiles" / "retail_assistant"

    passed = True
    tools_tested = 0

    # Set the RETAIL_API_URL env var so tools pick it up
    os.environ["RETAIL_API_URL"] = EDGE_API_URL

    # Test lookup_product
    try:
        from reachy_mini_conversation_app.profiles.retail_assistant.lookup_product import LookupProductTool
        tool = LookupProductTool()
        result = await tool(deps=None, query="beef jerky", max_results=3)
        if result.get("found"):
            ok("lookup_product('beef jerky')", f"{result['product_count']} products found")
        else:
            ok("lookup_product('beef jerky')", f"no match (graceful): {result.get('message', '')}")
        tools_tested += 1
    except ImportError as e:
        fail("lookup_product import", str(e))
        print("    Hint: ensure reachy_mini_conversation_app is installed or on sys.path")
        passed = False
    except Exception as e:
        fail("lookup_product execution", str(e))
        passed = False

    # Test get_store_info
    try:
        from reachy_mini_conversation_app.profiles.retail_assistant.get_store_info import GetStoreInfoTool
        tool = GetStoreInfoTool()
        result = await tool(deps=None)
        if "error" not in result:
            ok("get_store_info()", f"store={result.get('name')}, {result.get('product_count')} products")
        else:
            fail("get_store_info()", result.get("message", ""))
        tools_tested += 1
    except ImportError as e:
        fail("get_store_info import", str(e))
        passed = False
    except Exception as e:
        fail("get_store_info execution", str(e))
        passed = False

    # Test get_active_promos
    try:
        from reachy_mini_conversation_app.profiles.retail_assistant.get_active_promos import GetActivePromosTool
        tool = GetActivePromosTool()
        result = await tool(deps=None)
        ok("get_active_promos()", f"has_promos={result.get('has_promos')}, count={result.get('promo_count', 0)}")
        tools_tested += 1
    except ImportError as e:
        fail("get_active_promos import", str(e))
        passed = False
    except Exception as e:
        fail("get_active_promos execution", str(e))
        passed = False

    # Test signal_tracker (pure local, no API call)
    try:
        from reachy_mini_conversation_app.profiles.retail_assistant.signal_tracker import RecordInteractionSignalTool
        tool = RecordInteractionSignalTool()
        result = await tool(
            deps=None,
            intent="product_search",
            entity="beef jerky",
            resolved=True,
            confidence=0.95,
            sentiment="positive",
        )
        ok("record_interaction_signal()", f"signal_count={result.get('signal_count')}")
        tools_tested += 1
    except ImportError as e:
        fail("signal_tracker import", str(e))
        passed = False
    except Exception as e:
        fail("signal_tracker execution", str(e))
        passed = False

    print(f"\n  Tools tested: {tools_tested}")
    return passed


# ---------------------------------------------------------------------------
# Phase 3 — Robot connection + gestures
# ---------------------------------------------------------------------------
async def phase3_robot() -> bool:
    """Connect to the Reachy Mini and run basic gestures."""
    section("Phase 3: Robot Connection & Gestures")

    try:
        from reachy_mini import ReachyMini
        from reachy_mini.utils import create_head_pose
    except ImportError:
        fail("reachy_mini import", "SDK not installed")
        return False

    print("  Connecting to Reachy Mini (media_backend='no_media')...")
    try:
        robot = ReachyMini(media_backend="no_media")
    except Exception as e:
        fail("ReachyMini()", str(e))
        print("    Hint: is the reachy-mini daemon running? (reachy-mini start)")
        return False

    ok("Connected", f"simulation={robot.client.get_status().get('simulation_enabled', '?')}")

    passed = True
    import numpy as np

    # Nod yes
    try:
        print("  Gesture: nod yes...")
        robot.goto_target(head=create_head_pose(pitch=15), duration=0.4)
        robot.goto_target(head=create_head_pose(pitch=-15), duration=0.4)
        robot.goto_target(head=create_head_pose(), duration=0.4)
        ok("Nod yes")
    except Exception as e:
        fail("Nod yes", str(e))
        passed = False

    # Shake no
    try:
        print("  Gesture: shake no...")
        robot.goto_target(head=create_head_pose(yaw=20), duration=0.3)
        robot.goto_target(head=create_head_pose(yaw=-20), duration=0.3)
        robot.goto_target(head=create_head_pose(), duration=0.3)
        ok("Shake no")
    except Exception as e:
        fail("Shake no", str(e))
        passed = False

    # Play an emotion from the library
    try:
        print("  Gesture: emotion (happy)...")
        from reachy_mini.motion.recorded_move import RecordedMoves
        moves = RecordedMoves("pollen-robotics/reachy-mini-emotions-library")
        robot.play_move(moves.get("happy"), initial_goto_duration=1.0)
        time.sleep(2.0)
        ok("Emotion: happy")
    except Exception as e:
        fail("Emotion: happy", str(e))
        passed = False

    # Antenna wiggle (antennas take [right_rad, left_rad])
    try:
        print("  Gesture: antenna wiggle...")
        deg = np.deg2rad(30)
        robot.goto_target(antennas=[-deg, deg], duration=0.3)
        robot.goto_target(antennas=[deg, -deg], duration=0.3)
        robot.goto_target(antennas=[0.0, 0.0], duration=0.3)
        ok("Antenna wiggle")
    except Exception as e:
        fail("Antenna wiggle", str(e))
        passed = False

    # Combined: search a product via API, then react with gesture
    try:
        print("  Combined: product search → robot reaction...")
        async with httpx.AsyncClient(base_url=EDGE_API_URL, timeout=TIMEOUT) as client:
            r = await client.get("/api/products/search", params={"q": "coffee", "limit": 1})
            r.raise_for_status()
            data = r.json()

        if data["result_count"] > 0:
            product = data["products"][0]
            print(f"    Found: {product['name']} at {product['location']} (${product['price']})")
            # Happy nod — found the product!
            robot.goto_target(head=create_head_pose(pitch=10), duration=0.3)
            robot.goto_target(head=create_head_pose(pitch=-5), duration=0.3)
            robot.goto_target(head=create_head_pose(), duration=0.3)
            ok("Product found → happy nod")
        else:
            # Confused tilt — didn't find it
            robot.goto_target(head=create_head_pose(roll=20), duration=0.4)
            robot.goto_target(head=create_head_pose(), duration=0.4)
            ok("Product not found → confused tilt")
    except Exception as e:
        fail("Combined product+gesture", str(e))
        passed = False

    # Return to neutral
    try:
        robot.goto_target(head=create_head_pose(), antennas=[0.0, 0.0], duration=0.5)
    except Exception:
        pass

    robot.client.disconnect()
    ok("Robot disconnected cleanly")

    return passed


# ---------------------------------------------------------------------------
# Phase 4 — Full conversation hint
# ---------------------------------------------------------------------------
def phase4_talk_hint() -> None:
    """Print instructions for running the full KW conversation with the robot."""
    section("Phase 4: Full Conversation (manual)")
    print("""
  To run the full Karen Whisperer conversation app with the robot:

  Terminal 1 — Edge Backend:
    cd reachy_mini_retail_assistant
    python -m reachy_edge.main

  Terminal 2 — Karen Whisperer:
    cd reachy_mini_karen_whisperer/src/reachy_mini_karen_whisperer
    # Create .env with:
    #   OPENAI_API_KEY=sk-...
    #   REACHY_MINI_CUSTOM_PROFILE=retail_assistant
    #   RETAIL_API_URL=http://localhost:8000
    python -m reachy_mini_karen_whisperer.app

  The robot will:
    1. Connect to the Reachy Mini daemon
    2. Load the retail_assistant profile (tools + personality)
    3. Start listening via microphone (OpenAI Realtime voice)
    4. Answer product questions by calling the Edge Backend API
    5. Track interaction signals for pattern detection
    6. Express emotions and gestures while talking

  Try saying:
    - "Hey, do you have any beef jerky?"
    - "What deals do you have today?"
    - "Where's the coffee?"
    - "Take a selfie with me!"
""")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main() -> None:
    global EDGE_API_URL

    parser = argparse.ArgumentParser(description="Test Karen Whisperer + Edge Backend integration")
    parser.add_argument("--robot", action="store_true", help="Connect to real robot (Phase 3)")
    parser.add_argument("--talk", action="store_true", help="Show full conversation instructions (Phase 4)")
    parser.add_argument("--url", default=EDGE_API_URL, help=f"Edge Backend URL (default: {EDGE_API_URL})")
    args = parser.parse_args()

    EDGE_API_URL = args.url
    os.environ["RETAIL_API_URL"] = EDGE_API_URL

    print(f"\nKaren Whisperer + Edge Backend Integration Test")
    print(f"Edge Backend URL: {EDGE_API_URL}")

    results: dict[str, bool] = {}

    # Phase 1 — always
    results["Phase 1: Backend API"] = await phase1_backend_api()
    if not results["Phase 1: Backend API"]:
        print("\n  Phase 1 failed — cannot continue without the backend.")
        print("  Start the Edge Backend:  python -m reachy_edge.main\n")
        sys.exit(1)

    # Phase 2 — always
    results["Phase 2: KW Tools"] = await phase2_kw_tools()

    # Phase 3 — robot
    if args.robot:
        results["Phase 3: Robot"] = await phase3_robot()

    # Phase 4 — talk instructions
    if args.talk:
        phase4_talk_hint()

    # Summary
    section("Summary")
    all_passed = True
    for phase, passed in results.items():
        status = "[OK]" if passed else "[FAIL]"
        print(f"  {status}  {phase}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n  All phases passed!")
    else:
        print("\n  Some phases had failures — check output above.")

    if not args.robot:
        print("\n  Tip: run with --robot to test the physical robot")
    if not args.talk:
        print("  Tip: run with --talk for full conversation instructions")


if __name__ == "__main__":
    asyncio.run(main())
