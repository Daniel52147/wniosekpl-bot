import json
from typing import Any, Optional

import aiosqlite
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey

from src.config import DATABASE_PATH


class SQLiteStorage(BaseStorage):
    """Persist FSM state in SQLite across restarts."""

    def __init__(self, db_path=DATABASE_PATH) -> None:
        self.db_path = db_path

    @staticmethod
    def _key_id(key: StorageKey) -> str:
        return f"{key.bot_id}:{key.chat_id}:{key.user_id}:{key.destiny}"

    async def _ensure_table(self, db: aiosqlite.Connection) -> None:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS fsm_states (
                key_id TEXT PRIMARY KEY,
                state TEXT,
                data_json TEXT NOT NULL DEFAULT '{}',
                updated_at TEXT NOT NULL
            )
            """
        )

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        from src.database import _now

        kid = self._key_id(key)
        async with aiosqlite.connect(self.db_path) as db:
            await self._ensure_table(db)
            cur = await db.execute("SELECT data_json FROM fsm_states WHERE key_id = ?", (kid,))
            row = await cur.fetchone()
            data_json = row[0] if row else "{}"
            await db.execute(
                """
                INSERT INTO fsm_states (key_id, state, data_json, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(key_id) DO UPDATE SET state = excluded.state, updated_at = excluded.updated_at
                """,
                (kid, state.state if state else None, data_json, _now()),
            )
            await db.commit()

    async def get_state(self, key: StorageKey) -> Optional[str]:
        kid = self._key_id(key)
        async with aiosqlite.connect(self.db_path) as db:
            await self._ensure_table(db)
            cur = await db.execute("SELECT state FROM fsm_states WHERE key_id = ?", (kid,))
            row = await cur.fetchone()
            return row[0] if row else None

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        from src.database import _now

        kid = self._key_id(key)
        async with aiosqlite.connect(self.db_path) as db:
            await self._ensure_table(db)
            cur = await db.execute("SELECT state FROM fsm_states WHERE key_id = ?", (kid,))
            row = await cur.fetchone()
            state = row[0] if row else None
            await db.execute(
                """
                INSERT INTO fsm_states (key_id, state, data_json, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(key_id) DO UPDATE SET
                    data_json = excluded.data_json,
                    updated_at = excluded.updated_at
                """,
                (kid, state, json.dumps(data, ensure_ascii=False), _now()),
            )
            await db.commit()

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        kid = self._key_id(key)
        async with aiosqlite.connect(self.db_path) as db:
            await self._ensure_table(db)
            cur = await db.execute("SELECT data_json FROM fsm_states WHERE key_id = ?", (kid,))
            row = await cur.fetchone()
            if not row:
                return {}
            return json.loads(row[0])

    async def close(self) -> None:
        return None
