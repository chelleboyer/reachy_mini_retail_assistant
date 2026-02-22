"""Knowledge graph relationships (SQLite baseline)."""
import sqlite3
from pathlib import Path


class KnowledgeGraph:
    def __init__(self, db_path: str):
        db = Path(db_path)
        db.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db))
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS relationships (
                subject_id TEXT,
                predicate TEXT,
                object_id TEXT,
                weight REAL,
                created_at TEXT
            )
            """
        )
        self.conn.commit()

    def add_relationship(self, subject_id: str, predicate: str, object_id: str, weight: float = 1.0) -> None:
        self.conn.execute(
            "INSERT INTO relationships (subject_id, predicate, object_id, weight, created_at) VALUES (?, ?, ?, ?, datetime('now'))",
            (subject_id, predicate, object_id, weight),
        )
        self.conn.commit()
