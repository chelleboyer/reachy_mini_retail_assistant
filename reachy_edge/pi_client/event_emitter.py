"""Event emitter for sending events to π backend."""
import asyncio
import httpx
import logging
from typing import Dict, Any, List
from datetime import datetime
import json

from config import settings
from models.events import Event, EventType

logger = logging.getLogger(__name__)


class EventEmitter:
    """Batched event emitter to π backend."""
    
    def __init__(
        self,
        pi_url: str = None,
        pi_api_key: str = None,
        batch_size: int = None,
        batch_interval_s: int = None,
        enabled: bool = None
    ):
        self.pi_url = pi_url or settings.pi_url
        self.pi_api_key = pi_api_key or settings.pi_api_key
        self.batch_size = batch_size or settings.event_batch_size
        self.batch_interval_s = batch_interval_s or settings.event_batch_interval_s
        self.enabled = enabled if enabled is not None else settings.pi_enabled
        
        self._queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue()
        self._batch: List[Dict[str, Any]] = []
        self._last_flush = datetime.utcnow()
        self._running = False
        self._task: asyncio.Task = None
        
        self._events_sent = 0
        self._events_failed = 0
        
        if not self.enabled:
            logger.info("π client disabled (pi_enabled=False)")
    
    async def emit(self, event_data: Dict[str, Any]) -> None:
        """Queue an event for batched sending."""
        if not self.enabled:
            logger.debug("Event not emitted (π client disabled)")
            return
        
        await self._queue.put(event_data)
    
    async def worker(self) -> None:
        """Background worker that batches and sends events."""
        if not self.enabled:
            logger.info("Event worker not started (π client disabled)")
            return
        
        self._running = True
        logger.info(f"Event emitter worker started (batch_size={self.batch_size}, interval={self.batch_interval_s}s)")
        
        while self._running:
            try:
                # Wait for events with timeout
                try:
                    event_data = await asyncio.wait_for(
                        self._queue.get(),
                        timeout=self.batch_interval_s
                    )
                    self._batch.append(event_data)
                except asyncio.TimeoutError:
                    # Timeout - flush if we have events
                    pass
                
                # Flush if batch is full or interval elapsed
                should_flush = (
                    len(self._batch) >= self.batch_size or
                    (datetime.utcnow() - self._last_flush).total_seconds() >= self.batch_interval_s
                )
                
                if should_flush and self._batch:
                    await self._flush_batch()
            
            except Exception as e:
                logger.error(f"Error in event worker: {e}", exc_info=True)
                await asyncio.sleep(1)  # Prevent tight loop on errors
    
    async def _flush_batch(self) -> None:
        """Send batched events to π."""
        if not self._batch:
            return
        
        batch_to_send = self._batch.copy()
        self._batch.clear()
        self._last_flush = datetime.utcnow()
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{self.pi_url}/events/batch",
                    json={"events": batch_to_send},
                    headers={"Authorization": f"Bearer {self.pi_api_key}"}
                )
                
                if response.status_code == 200:
                    self._events_sent += len(batch_to_send)
                    logger.info(f"Sent {len(batch_to_send)} events to π")
                else:
                    self._events_failed += len(batch_to_send)
                    logger.error(f"Failed to send events: {response.status_code} {response.text}")
        
        except Exception as e:
            self._events_failed += len(batch_to_send)
            logger.error(f"Error sending events to π: {e}")
    
    async def flush(self) -> None:
        """Manually flush remaining events."""
        if self._batch:
            logger.info(f"Flushing {len(self._batch)} remaining events")
            await self._flush_batch()
    
    def stop(self) -> None:
        """Stop the worker."""
        self._running = False
        logger.info("Event emitter worker stopped")
    
    def stats(self) -> Dict[str, Any]:
        """Get emitter statistics."""
        return {
            "enabled": self.enabled,
            "queue_size": self._queue.qsize(),
            "batch_size": len(self._batch),
            "events_sent": self._events_sent,
            "events_failed": self._events_failed,
            "success_rate_pct": round(
                (self._events_sent / (self._events_sent + self._events_failed) * 100)
                if (self._events_sent + self._events_failed) > 0
                else 100,
                2
            )
        }
