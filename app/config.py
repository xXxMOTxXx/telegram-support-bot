from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Settings:
    BOT_TOKEN: str
    ADMIN_GROUP_ID: int
    DB_PATH: str
    TIMEZONE: str

    @classmethod
    def from_env(cls) -> "Settings":
        bot_token = os.getenv("BOT_TOKEN", "").strip()
        admin_group_raw = os.getenv("ADMIN_GROUP_ID", "").strip()
        db_path = os.getenv("DB_PATH", "support_bot.db").strip() or "support_bot.db"
        timezone = os.getenv("TIMEZONE", "Europe/Berlin").strip() or "Europe/Berlin"

        if not bot_token:
            raise ValueError("BOT_TOKEN is not set")
        if not admin_group_raw:
            raise ValueError("ADMIN_GROUP_ID is not set")

        try:
            admin_group_id = int(admin_group_raw)
        except ValueError as exc:
            raise ValueError("ADMIN_GROUP_ID must be an integer") from exc

        return cls(
            BOT_TOKEN=bot_token,
            ADMIN_GROUP_ID=admin_group_id,
            DB_PATH=db_path,
            TIMEZONE=timezone,
        )


settings = Settings.from_env()
