import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "hantawatch.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS live_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  source_name TEXT NOT NULL,
  source_url TEXT NOT NULL UNIQUE,
  published_at TEXT,
  summary TEXT,
  matched_keywords TEXT,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS refresh_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  refreshed_at TEXT NOT NULL,
  status TEXT NOT NULL,
  items_found INTEGER DEFAULT 0,
  error TEXT
);
"""

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn

def insert_live_item(item: dict) -> bool:
    conn = connect()
    try:
        conn.execute(
            """
            INSERT OR IGNORE INTO live_items
            (title, source_name, source_url, published_at, summary, matched_keywords, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["title"], item["source_name"], item["source_url"], item.get("published_at"),
                item.get("summary"), ",".join(item.get("matched_keywords", [])),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        changed = conn.total_changes > 0
        conn.commit()
        return changed
    finally:
        conn.close()

def get_live_items(limit: int = 50):
    conn = connect()
    try:
        rows = conn.execute(
            "SELECT * FROM live_items ORDER BY COALESCE(published_at, created_at) DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) | {"matched_keywords": [k for k in (r["matched_keywords"] or "").split(",") if k]} for r in rows]
    finally:
        conn.close()

def log_refresh(status: str, items_found: int = 0, error: str | None = None):
    conn = connect()
    try:
        conn.execute(
            "INSERT INTO refresh_log (refreshed_at, status, items_found, error) VALUES (?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), status, items_found, error),
        )
        conn.commit()
    finally:
        conn.close()

def latest_refresh():
    conn = connect()
    try:
        row = conn.execute("SELECT * FROM refresh_log ORDER BY refreshed_at DESC LIMIT 1").fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
