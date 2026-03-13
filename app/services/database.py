from __future__ import annotations

from pathlib import Path
from typing import Any

import aiosqlite


class Database:
    def __init__(self, path: str) -> None:
        self.path = path

    def _ensure_parent_dir(self) -> None:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

    async def init(self) -> None:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            await db.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT NOT NULL,
                    language TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    first_message TEXT NOT NULL,
                    status TEXT NOT NULL,
                    assigned_admin_id INTEGER,
                    assigned_admin_username TEXT,
                    assigned_admin_name TEXT,
                    group_chat_id INTEGER,
                    group_message_id INTEGER,
                    created_at TEXT NOT NULL,
                    claimed_at TEXT,
                    closed_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                );

                CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON tickets (user_id);
                CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets (status);
                """
            )
            await db.commit()

    async def upsert_user(
        self,
        *,
        user_id: int,
        username: str | None,
        full_name: str,
        now_iso: str,
    ) -> None:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            await db.execute(
                """
                INSERT INTO users (user_id, username, full_name, language, created_at, updated_at)
                VALUES (?, ?, ?, NULL, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    username = excluded.username,
                    full_name = excluded.full_name,
                    updated_at = excluded.updated_at
                """,
                (user_id, username, full_name, now_iso, now_iso),
            )
            await db.commit()

    async def set_user_language(self, user_id: int, language: str, now_iso: str) -> None:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            await db.execute(
                "UPDATE users SET language = ?, updated_at = ? WHERE user_id = ?",
                (language, now_iso, user_id),
            )
            await db.commit()

    async def get_user(self, user_id: int) -> dict[str, Any] | None:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            cursor = await db.execute(
                "SELECT * FROM users WHERE user_id = ?",
                (user_id,),
            )
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def get_active_ticket_by_user(self, user_id: int) -> dict[str, Any] | None:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            cursor = await db.execute(
                """
                SELECT *
                FROM tickets
                WHERE user_id = ? AND status IN ('open', 'claimed')
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id,),
            )
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def create_ticket(
        self,
        *,
        user_id: int,
        language: str,
        first_message: str,
        created_at: str,
    ) -> int:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            cursor = await db.execute(
                """
                INSERT INTO tickets (
                    user_id,
                    language,
                    first_message,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, 'open', ?)
                """,
                (user_id, language, first_message, created_at),
            )
            await db.commit()
            return int(cursor.lastrowid)

    async def set_ticket_group_message(
        self,
        *,
        ticket_id: int,
        group_chat_id: int,
        group_message_id: int,
    ) -> None:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            await db.execute(
                """
                UPDATE tickets
                SET group_chat_id = ?, group_message_id = ?
                WHERE id = ?
                """,
                (group_chat_id, group_message_id, ticket_id),
            )
            await db.commit()

    async def get_ticket(self, ticket_id: int) -> dict[str, Any] | None:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            cursor = await db.execute(
                "SELECT * FROM tickets WHERE id = ?",
                (ticket_id,),
            )
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def claim_ticket(
        self,
        *,
        ticket_id: int,
        admin_id: int,
        admin_username: str | None,
        admin_name: str,
        claimed_at: str,
    ) -> bool:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            cursor = await db.execute(
                """
                UPDATE tickets
                SET
                    status = 'claimed',
                    assigned_admin_id = ?,
                    assigned_admin_username = ?,
                    assigned_admin_name = ?,
                    claimed_at = ?
                WHERE id = ? AND status = 'open'
                """,
                (admin_id, admin_username, admin_name, claimed_at, ticket_id),
            )
            await db.commit()
            return cursor.rowcount > 0

    async def close_ticket(
        self,
        *,
        ticket_id: int,
        admin_id: int,
        closed_at: str,
    ) -> bool:
        self._ensure_parent_dir()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys = ON")
            cursor = await db.execute(
                """
                UPDATE tickets
                SET status = 'closed', closed_at = ?
                WHERE id = ? AND assigned_admin_id = ? AND status = 'claimed'
                """,
                (closed_at, ticket_id, admin_id),
            )
            await db.commit()
            return cursor.rowcount > 0
