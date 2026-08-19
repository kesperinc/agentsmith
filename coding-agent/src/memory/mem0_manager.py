"""
Mem0 Long-Term Memory & Developer Profile Management Module
Stores persistent developer preferences, coding rules, and context in .agentsmith/
"""

import os
import json
import sqlite3
import datetime
from typing import Dict, Any, List, Optional

MEM_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".agentsmith", "mem0_memory.db")

class Mem0Manager:
    def __init__(self, db_path: str = MEM_DB_PATH):
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
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT, -- 'coding_style', 'project_rule', 'preference', 'tech_stack'
                key TEXT,
                value TEXT,
                confidence REAL DEFAULT 1.0,
                created_at TEXT,
                updated_at TEXT
            )
            """)
            conn.commit()

            # 초기 기본 기억 주입
            cursor.execute("SELECT COUNT(*) as cnt FROM memories")
            if cursor.fetchone()["cnt"] == 0:
                now = datetime.datetime.now(datetime.timezone.utc).isoformat()
                defaults = [
                    ("coding_style", "language_rule", "코드 주석과 모든 설명은 한국어로만 작성", 1.0, now, now),
                    ("project_rule", "virtualenv", "가상환경은 uv를 사용하며 .venv 디렉터리에 격리", 1.0, now, now),
                    ("project_rule", "encoding", "모든 생성/수정 파일은 2바이트 다국어 보장을 위해 UTF-8 BOM-less 강제", 1.0, now, now),
                    ("tech_stack", "backend_framework", "FastAPI 기반 고성능 비동기 REST API 아키텍처", 0.95, now, now),
                    ("project_rule", "triad", "작업 시 [작업계획서]-[개발코드]-[상세명세서] 1:1:1 트라이어드 준수", 1.0, now, now)
                ]
                cursor.executemany(
                    "INSERT INTO memories (category, key, value, confidence, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    defaults
                )
                conn.commit()

    def list_memories(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM memories ORDER BY category ASC, id ASC")
            return [dict(r) for r in cursor.fetchall()]

    def add_memory(self, category: str, key: str, value: str, confidence: float = 1.0) -> int:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memories (category, key, value, confidence, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (category, key, value, confidence, now, now)
            )
            conn.commit()
            return cursor.lastrowid

    def delete_memory(self, memory_id: int):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()

    def get_system_prompt_context(self) -> str:
        memories = self.list_memories()
        if not memories:
            return ""
        lines = ["[Mem0 장기 기억 프로필 (Persistent Developer Profile)]"]
        for m in memories:
            lines.append(f"• [{m['category']}] {m['key']}: {m['value']}")
        return "\n".join(lines)
