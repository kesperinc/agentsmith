"""
Agent Smith Session & Multi-File Diff Management Database (SQLite)
Handles UUID Sessions, Message History, Artifacts, and Multi-File Diffs with Rollback
"""

import os
import sqlite3
import uuid
import datetime
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".agentsmith", "sessions.db")

class SessionManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            # 1. Sessions Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                title TEXT,
                model_id TEXT,
                mode TEXT,
                created_at TEXT,
                updated_at TEXT
            )
            """)

            # 2. Messages Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                data_json TEXT,
                created_at TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
            """)

            # 3. Artifacts Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS artifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                filename TEXT,
                path TEXT,
                type TEXT,
                summary TEXT,
                created_at TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
            """)

            # 4. Multi-File Diff History Table (Rollback Support)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS diff_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                file_path TEXT,
                original_content TEXT,
                modified_content TEXT,
                status TEXT DEFAULT 'pending', -- pending, accepted, rejected, rolled_back
                created_at TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
            """)
            conn.commit()

    def create_session(self, title: str = "새 세션", model_id: str = "google/gemini-2.0-flash", mode: str = "planning") -> Dict[str, Any]:
        session_id = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (id, title, model_id, mode, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (session_id, title, model_id, mode, now, now)
            )
            conn.commit()
        return {
            "id": session_id,
            "title": title,
            "model_id": model_id,
            "mode": mode,
            "created_at": now
        }

    def list_sessions(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessions ORDER BY updated_at DESC LIMIT 30")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
            session = cursor.fetchone()
            if not session:
                return None
            
            # Messages
            cursor.execute("SELECT role, content, data_json, created_at FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
            messages = [dict(r) for r in cursor.fetchall()]

            # Artifacts
            cursor.execute("SELECT filename, path, type, summary, created_at FROM artifacts WHERE session_id = ? ORDER BY id ASC", (session_id,))
            artifacts = [dict(r) for r in cursor.fetchall()]

            # Diffs
            cursor.execute("SELECT id, file_path, original_content, modified_content, status, created_at FROM diff_history WHERE session_id = ? ORDER BY id DESC", (session_id,))
            diffs = [dict(r) for r in cursor.fetchall()]

            return {
                "session": dict(session),
                "messages": messages,
                "artifacts": artifacts,
                "diffs": diffs
            }

    def save_message(self, session_id: str, role: str, content: str, data_json: Optional[str] = None):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (session_id, role, content, data_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (session_id, role, content, data_json, now)
            )
            # Update session timestamp & auto-title
            if role == "user":
                title_snippet = content[:30] + ("..." if len(content) > 30 else "")
                cursor.execute(
                    "UPDATE sessions SET title = ?, updated_at = ? WHERE id = ? AND title = '새 세션'",
                    (title_snippet, now, session_id)
                )
            else:
                cursor.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (now, session_id))
            conn.commit()

    def record_diff(self, session_id: str, file_path: str, original_content: str, modified_content: str) -> int:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO diff_history (session_id, file_path, original_content, modified_content, status, created_at) VALUES (?, ?, ?, ?, 'pending', ?)",
                (session_id, file_path, original_content, modified_content, now)
            )
            conn.commit()
            return cursor.lastrowid

    def update_diff_status(self, diff_id: int, status: str):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE diff_history SET status = ? WHERE id = ?", (status, diff_id))
            conn.commit()

    def delete_session(self, session_id: str):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM artifacts WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM diff_history WHERE session_id = ?", (session_id,))
            conn.commit()
