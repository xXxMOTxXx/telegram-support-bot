import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.handlers.admin import router as admin_router
from app.handlers.user import router as user_router
from app.services.database import Database


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    db = Database(settings.DB_PATH)
    await db.init()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(admin_router)

    try:
        await dp.start_polling(bot, db=db, settings=settings)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
