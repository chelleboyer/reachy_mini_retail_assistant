"""Canonical event/entity store (SQLite baseline)."""
from __future__ import annotations

import sqlite3
from pathlib import Path


class CanonicalStore:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                domain TEXT,
                timestamp TEXT,
                payload TEXT,
                confidence REAL
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entities (
                entity_id TEXT PRIMARY KEY,
                entity_type TEXT,
                name TEXT,
                properties TEXT,
                created_at TEXT,
                updated_at TEXT
            )
            """
        )
        self.conn.commit()

    def save_event(self, event: dict) -> int:
        cur = self.conn.execute(
            "INSERT INTO events (event_type, domain, timestamp, payload, confidence) VALUES (?, ?, ?, ?, ?)",
            (
                event.get("event_type"),
                event.get("domain", "retail"),
                event.get("timestamp"),
                str(event),
                float(event.get("confidence", 1.0)),
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)
