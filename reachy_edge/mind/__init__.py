"""Mind Monitor — real-time event bus for Reachy Edge observability.

Provides a pub/sub event bus with a ring buffer for recent events
and async SSE (Server-Sent Events) fan-out to connected dashboards.

Usage::

    from reachy_edge.mind import mind_bus

    # Publish an event (from anywhere in the app)
    await mind_bus.publish({"type": "request", "query": "milk", ...})

    # Subscribe to the stream (SSE endpoint)
    async for event in mind_bus.subscribe():
        yield f"data: {json.dumps(event)}\\n\\n"
"""
from __future__ import annotations

import asyncio
import json
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Dict, List, Optional

import structlog

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Event types
# ---------------------------------------------------------------------------

EVENT_REQUEST = "request"          # Incoming API request
EVENT_RESPONSE = "response"        # Outgoing API response
EVENT_CACHE_HIT = "cache_hit"      # L1 or L2 hit
EVENT_CACHE_MISS = "cache_miss"    # Cache miss
EVENT_SEARCH = "search"            # FTS5 search executed
EVENT_SIGNAL = "signal"            # Karen Whisperer signal forwarded
EVENT_HEALTH = "health"            # Periodic health snapshot
EVENT_ERROR = "error"              # Error occurred
EVENT_STARTUP = "startup"          # Service started
EVENT_SHUTDOWN = "shutdown"        # Service stopping


@dataclass
class MindEvent:
    """A single observable event in Reachy's mind."""

    type: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    data: Dict[str, Any] = field(default_factory=dict)
    id: int = 0  # Auto-assigned by the bus

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "type": self.type, "timestamp": self.timestamp, "data": self.data}

    def to_sse(self) -> str:
        """Format as Server-Sent Event."""
        payload = json.dumps(self.to_dict())
        return f"id: {self.id}\nevent: mind\ndata: {payload}\n\n"


# ---------------------------------------------------------------------------
# Mind Bus — pub/sub with ring buffer
# ---------------------------------------------------------------------------

class MindBus:
    """Async event bus with ring buffer and SSE fan-out.

    Attributes:
        max_history: Max events kept in ring buffer.
        _subscribers: Set of asyncio.Queue objects, one per SSE client.
    """

    def __init__(self, max_history: int = 500):
        self.max_history = max_history
        self._history: deque[MindEvent] = deque(maxlen=max_history)
        self._subscribers: set[asyncio.Queue[MindEvent]] = set()
        self._counter = 0
        self._start_time = time.time()

        # Aggregate counters for dashboard summary
        self._total_requests = 0
        self._total_cache_hits = 0
        self._total_cache_misses = 0
        self._total_errors = 0
        self._latencies: deque[float] = deque(maxlen=200)  # last 200 latencies

    # -- Publishing ----------------------------------------------------------

    async def publish(self, event: MindEvent) -> None:
        """Publish an event to all subscribers and the ring buffer."""
        self._counter += 1
        event.id = self._counter

        # Update aggregates
        self._update_aggregates(event)

        # Store in ring buffer
        self._history.append(event)

        # Fan-out to all SSE subscribers (non-blocking)
        dead: list[asyncio.Queue] = []
        for q in self._subscribers:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                dead.append(q)
        for q in dead:
            self._subscribers.discard(q)

    def publish_sync(self, event: MindEvent) -> None:
        """Publish from synchronous code (best-effort, fire-and-forget)."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.publish(event))
        except RuntimeError:
            # No running loop — just store in history
            self._counter += 1
            event.id = self._counter
            self._update_aggregates(event)
            self._history.append(event)

    # -- Subscribing ---------------------------------------------------------

    async def subscribe(self) -> AsyncIterator[MindEvent]:
        """Yield events as they arrive. Used by SSE endpoint."""
        q: asyncio.Queue[MindEvent] = asyncio.Queue(maxsize=100)
        self._subscribers.add(q)
        logger.info("mind_subscriber_connected", total=len(self._subscribers))
        try:
            while True:
                event = await q.get()
                yield event
        finally:
            self._subscribers.discard(q)
            logger.info("mind_subscriber_disconnected", total=len(self._subscribers))

    # -- State snapshot ------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        """Return current state for initial dashboard load."""
        total_cache = self._total_cache_hits + self._total_cache_misses
        hit_rate = (self._total_cache_hits / total_cache * 100) if total_cache > 0 else 0
        latency_list = list(self._latencies)
        avg_latency = sum(latency_list) / len(latency_list) if latency_list else 0
        p95_latency = sorted(latency_list)[int(len(latency_list) * 0.95)] if len(latency_list) > 1 else avg_latency

        return {
            "uptime_seconds": round(time.time() - self._start_time, 1),
            "total_requests": self._total_requests,
            "total_cache_hits": self._total_cache_hits,
            "total_cache_misses": self._total_cache_misses,
            "cache_hit_rate_pct": round(hit_rate, 1),
            "total_errors": self._total_errors,
            "avg_latency_ms": round(avg_latency, 1),
            "p95_latency_ms": round(p95_latency, 1),
            "latencies": latency_list[-50:],  # last 50 for sparkline
            "subscribers": len(self._subscribers),
            "history_size": len(self._history),
            "recent_events": [e.to_dict() for e in list(self._history)[-30:]],
        }

    # -- Internals -----------------------------------------------------------

    def _update_aggregates(self, event: MindEvent) -> None:
        if event.type == EVENT_RESPONSE:
            self._total_requests += 1
            latency = event.data.get("latency_ms", 0)
            if latency:
                self._latencies.append(latency)
        elif event.type == EVENT_CACHE_HIT:
            self._total_cache_hits += 1
        elif event.type == EVENT_CACHE_MISS:
            self._total_cache_misses += 1
        elif event.type == EVENT_ERROR:
            self._total_errors += 1


# ---------------------------------------------------------------------------
# Singleton instance
# ---------------------------------------------------------------------------

mind_bus = MindBus()
