import sqlite3
from pathlib import Path

from ..exceptions import RepositoryError
from ..models import ResearchResult
from .base import ResearchRepository


class SQLiteRepository(ResearchRepository):
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS research_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                summary TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def save(self, result: ResearchResult) -> int:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute(
                "INSERT INTO research_results (topic, summary, created_at) VALUES (?, ?, ?)",
                (result.topic, result.summary, result.created_at),
            )
            conn.commit()
            row_id = cursor.lastrowid
            conn.close()
            return row_id
        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to save result: {e}") from e

    def get_history(self, limit: int = 10) -> list[ResearchResult]:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT topic, summary, created_at FROM research_results ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()
        return [ResearchResult(topic=r[0], summary=r[1], created_at=r[2]) for r in rows]
