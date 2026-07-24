"""
storage.py
Tiny SQLite wrapper that remembers each Telegram user's preferred target
language, set via /setlang. SQLite is a single file (config.DB_PATH) --
fine for an MVP, but note that Railway's filesystem is ephemeral: a fresh
deploy (not a restart) wipes it. If you outgrow that, swap this module
for Railway's Postgres add-on and the rest of the bot doesn't need to change.
"""

import sqlite3
import threading

from config import DB_PATH, DEFAULT_TARGET_LANG

_lock = threading.Lock()


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            target_lang TEXT NOT NULL
        )
        """
    )
    return conn


def get_target_lang(user_id: int) -> str:
    with _lock, _get_conn() as conn:
        row = conn.execute(
            "SELECT target_lang FROM user_settings WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return row[0] if row else DEFAULT_TARGET_LANG


def set_target_lang(user_id: int, lang_code: str) -> None:
    with _lock, _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO user_settings (user_id, target_lang)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET target_lang = excluded.target_lang
            """,
            (user_id, lang_code),
        )
        conn.commit()
