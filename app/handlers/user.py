from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from app.config import Settings
from app.keyboards.user import LANGUAGE_KEYBOARD
from app.locales.texts import SUPPORTED_LANGUAGES, t
from app.services.database import Database
from app.services.tickets import format_group_ticket_message
from app.keyboards.admin import accept_ticket_keyboard
from app.utils.time import display_time, now_iso

router = Router(name=__name__)


@router.message(CommandStart(), F.chat.type == "private")
async def start_private(message: Message, db: Database, settings: Settings) -> None:
    user = message.from_user
    if user is None:
        return

    current_time = now_iso(settings.TIMEZONE)
    await db.upsert_user(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        now_iso=current_time,
    )

    record = await db.get_user(user.id)
    if not record or not record.get("language"):
        await message.answer(t("en", "choose_language"), reply_markup=LANGUAGE_KEYBOARD)
        return

    active_ticket = await db.get_active_ticket_by_user(user.id)
    if active_ticket:
        await message.answer(
            t(record["language"], "ticket_already_exists", ticket_id=active_ticket["id"])
        )
        return

    await message.answer(t(record["language"], "send_issue"))


@router.callback_query(F.data.startswith("set_lang:"))
async def set_language(callback: CallbackQuery, db: Database, settings: Settings) -> None:
    user = callback.from_user
    if user is None:
        await callback.answer()
        return

    language = callback.data.split(":", 1)[1]
    if language not in SUPPORTED_LANGUAGES:
        await callback.answer()
        return

    current_time = now_iso(settings.TIMEZONE)
    await db.upsert_user(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        now_iso=current_time,
    )
    await db.set_user_language(user.id, language, current_time)

    await callback.message.edit_text(t(language, "language_saved"))
    await callback.answer()


@router.message(F.chat.type == "private", ~F.text)
async def reject_non_text_messages(message: Message, db: Database, settings: Settings) -> None:
    user = message.from_user
    if user is None:
        return

    current_time = now_iso(settings.TIMEZONE)
    await db.upsert_user(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        now_iso=current_time,
    )
    record = await db.get_user(user.id)
    language = (record or {}).get("language") or "en"
    await message.answer(t(language, "unsupported_message"))


@router.message(F.chat.type == "private", F.text)
async def create_ticket(message: Message, db: Database, settings: Settings) -> None:
    user = message.from_user
    if user is None:
        return

    current_time = now_iso(settings.TIMEZONE)
    await db.upsert_user(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        now_iso=current_time,
    )

    record = await db.get_user(user.id)
    language = (record or {}).get("language")
    if not language:
        await message.answer(t("en", "language_not_selected"), reply_markup=LANGUAGE_KEYBOARD)
        return

    active_ticket = await db.get_active_ticket_by_user(user.id)
    if active_ticket:
        await message.answer(t(language, "ticket_already_exists", ticket_id=active_ticket["id"]))
        return

    text = (message.text or "").strip()
    if not text:
        await message.answer(t(language, "unsupported_message"))
        return

    ticket_id = await db.create_ticket(
        user_id=user.id,
        language=language,
        first_message=text,
        created_at=current_time,
    )

    admin_message = await message.bot.send_message(
        chat_id=settings.ADMIN_GROUP_ID,
        text=format_group_ticket_message(
            ticket_id=ticket_id,
            created_at=display_time(current_time),
            language=language,
            first_message=text,
        ),
        reply_markup=accept_ticket_keyboard(ticket_id),
    )

    await db.set_ticket_group_message(
        ticket_id=ticket_id,
        group_chat_id=admin_message.chat.id,
        group_message_id=admin_message.message_id,
    )

    await message.answer(t(language, "ticket_created", ticket_id=ticket_id))
