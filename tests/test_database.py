import asyncio
import tempfile
from pathlib import Path

from app.services.database import Database


async def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = str(Path(tmp_dir) / "test.db")
        db = Database(db_path)
        await db.init()

        await db.upsert_user(
            user_id=1,
            username="userone",
            full_name="User One",
            now_iso="2026-03-12T12:00:00+01:00",
        )
        await db.set_user_language(1, "en", "2026-03-12T12:00:01+01:00")
        user = await db.get_user(1)
        assert user is not None
        assert user["language"] == "en"

        ticket_id = await db.create_ticket(
            user_id=1,
            language="en",
            first_message="Help me",
            created_at="2026-03-12T12:00:02+01:00",
        )
        assert ticket_id == 1

        active = await db.get_active_ticket_by_user(1)
        assert active is not None
        assert active["status"] == "open"

        claimed = await db.claim_ticket(
            ticket_id=ticket_id,
            admin_id=99,
            admin_username="agent",
            admin_name="Agent Smith",
            claimed_at="2026-03-12T12:00:03+01:00",
        )
        assert claimed is True

        claimed_again = await db.claim_ticket(
            ticket_id=ticket_id,
            admin_id=100,
            admin_username="other",
            admin_name="Other Agent",
            claimed_at="2026-03-12T12:00:04+01:00",
        )
        assert claimed_again is False

        closed = await db.close_ticket(
            ticket_id=ticket_id,
            admin_id=99,
            closed_at="2026-03-12T12:00:05+01:00",
        )
        assert closed is True

        active_after_close = await db.get_active_ticket_by_user(1)
        assert active_after_close is None


if __name__ == "__main__":
    asyncio.run(main())
