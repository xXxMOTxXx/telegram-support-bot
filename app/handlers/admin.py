from __future__ import annotations

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import CallbackQuery

from app.config import Settings
from app.keyboards.admin import close_ticket_keyboard
from app.locales.texts import t
from app.services.database import Database
from app.services.tickets import (
    format_admin_private_ticket_message,
    format_claimed_group_ticket_message,
    format_closed_group_ticket_message,
)
from app.utils.time import display_time, now_iso

router = Router(name=__name__)


@router.callback_query(F.data.startswith("accept_ticket:"))
async def accept_ticket(callback: CallbackQuery, db: Database, settings: Settings) -> None:
    if callback.message is None:
        await callback.answer()
        return

    ticket_id = int(callback.data.split(":", 1)[1])
    ticket = await db.get_ticket(ticket_id)
    if not ticket:
        await callback.answer("Ticket not found", show_alert=True)
        return

    if ticket["status"] != "open":
        await callback.answer("Ticket already claimed or closed", show_alert=True)
        return

    admin = callback.from_user
    claimed = await db.claim_ticket(
        ticket_id=ticket_id,
        admin_id=admin.id,
        admin_username=admin.username,
        admin_name=admin.full_name,
        claimed_at=now_iso(settings.TIMEZONE),
    )
    if not claimed:
        await callback.answer("Ticket already claimed", show_alert=True)
        return

    ticket = await db.get_ticket(ticket_id)
    user = await db.get_user(ticket["user_id"])

    try:
        await callback.message.edit_text(
            format_claimed_group_ticket_message(
                ticket_id=ticket_id,
                created_at=display_time(ticket["created_at"]),
                language=ticket["language"],
                first_message=ticket["first_message"],
                admin_name=admin.full_name,
                admin_username=admin.username,
            )
        )
    except TelegramBadRequest:
        pass

    if user:
        try:
            await callback.bot.send_message(
                chat_id=admin.id,
                text=format_admin_private_ticket_message(
                    ticket_id=ticket_id,
                    user_id=user["user_id"],
                    username=user.get("username"),
                    full_name=user["full_name"],
                    language=ticket["language"],
                    first_message=ticket["first_message"],
                ),
                reply_markup=close_ticket_keyboard(ticket_id),
            )
        except TelegramForbiddenError:
            await callback.message.answer(
                f"Ticket #{ticket_id} claimed, but I could not send you the user details in private. Start the bot in private first."
            )

        admin_display = (
            t(ticket["language"], "assigned_user_with_username", admin_name=admin.full_name, admin_username=admin.username)
            if admin.username
            else t(ticket["language"], "assigned_user_no_username", admin_name=admin.full_name)
        )
        try:
            await callback.bot.send_message(
                chat_id=user["user_id"],
                text=t(ticket["language"], "ticket_claimed_user", ticket_id=ticket_id, admin_display=admin_display),
            )
        except TelegramForbiddenError:
            pass

    await callback.answer("Ticket accepted")


@router.callback_query(F.data.startswith("close_ticket:"), F.message.chat.type == "private")
async def close_ticket(callback: CallbackQuery, db: Database, settings: Settings) -> None:
    if callback.message is None:
        await callback.answer()
        return

    ticket_id = int(callback.data.split(":", 1)[1])
    ticket = await db.get_ticket(ticket_id)
    if not ticket:
        await callback.answer("Ticket not found", show_alert=True)
        return

    closed = await db.close_ticket(
        ticket_id=ticket_id,
        admin_id=callback.from_user.id,
        closed_at=now_iso(settings.TIMEZONE),
    )
    if not closed:
        await callback.answer("You cannot close this ticket", show_alert=True)
        return

    ticket = await db.get_ticket(ticket_id)
    user = await db.get_user(ticket["user_id"])

    if user:
        try:
            await callback.bot.send_message(
                chat_id=user["user_id"],
                text=t(ticket["language"], "ticket_closed_user", ticket_id=ticket_id),
            )
        except TelegramForbiddenError:
            pass

    if ticket.get("group_chat_id") and ticket.get("group_message_id"):
        try:
            await callback.bot.edit_message_text(
                chat_id=ticket["group_chat_id"],
                message_id=ticket["group_message_id"],
                text=format_closed_group_ticket_message(
                    ticket_id=ticket_id,
                    created_at=display_time(ticket["created_at"]),
                    language=ticket["language"],
                    first_message=ticket["first_message"],
                    admin_name=ticket.get("assigned_admin_name"),
                    admin_username=ticket.get("assigned_admin_username"),
                ),
            )
        except TelegramBadRequest:
            pass

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Ticket closed")
    await callback.message.answer(f"Ticket #{ticket_id} closed successfully.")
