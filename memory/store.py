"""SQLite persistence backend for user/session research memory.

Uses a real SQL database file (not browser storage). The path can be overridden
with MEMORY_DB_PATH so a volume or /data mount survives process restarts.
"""
from __future__ import annotations

import os
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_DB = ROOT / "data" / "memory.db"
_lock = threading.RLock()
_initialized_for: str | None = None


def db_path() -> Path:
    raw = os.getenv("MEMORY_DB_PATH", "").strip()
    if raw:
        return Path(raw)
    # Hugging Face persistent disk, when present
    data_dir = Path("/data")
    if data_dir.is_dir() and os.access(data_dir, os.W_OK):
        return data_dir / "memory.db"
    return _DEFAULT_DB


def configure(path: str | Path) -> None:
    """Point the store at a different file (used by tests)."""
    global _initialized_for
    os.environ["MEMORY_DB_PATH"] = str(path)
    _initialized_for = None
    init_db()


def _connect() -> sqlite3.Connection:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


@contextmanager
def get_conn() -> Iterator[sqlite3.Connection]:
    init_db()
    with _lock:
        conn = _connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def init_db() -> None:
    global _initialized_for
    path = str(db_path())
    if _initialized_for == path:
        return
    with _lock:
        if _initialized_for == path:
            return
        conn = _connect()
        try:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL DEFAULT 'New research session',
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS memory_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT,
                    kind TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_sessions_user
                    ON sessions(user_id, updated_at);
                CREATE INDEX IF NOT EXISTS idx_messages_session
                    ON messages(user_id, session_id, id);
                CREATE INDEX IF NOT EXISTS idx_memory_user_kind
                    ON memory_items(user_id, kind, created_at);
                """
            )
            conn.commit()
            _initialized_for = path
        finally:
            conn.close()
