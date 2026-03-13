from __future__ import annotations

from aiogram import html


def format_group_ticket_message(*, ticket_id: int, created_at: str, language: str, first_message: str) -> str:
    return (
        "<b>New support ticket</b>\n\n"
        f"<b>Ticket ID:</b> #{ticket_id}\n"
        f"<b>Opened at:</b> {html.quote(created_at)}\n"
        f"<b>Language:</b> {html.quote(language.upper())}\n\n"
        f"<b>First message:</b>\n{html.quote(first_message)}"
    )


def format_claimed_group_ticket_message(
    *,
    ticket_id: int,
    created_at: str,
    language: str,
    first_message: str,
    admin_name: str,
    admin_username: str | None,
) -> str:
    admin_line = html.quote(admin_name)
    if admin_username:
        admin_line += f" (@{html.quote(admin_username)})"

    return (
        "<b>Ticket claimed</b>\n\n"
        f"<b>Ticket ID:</b> #{ticket_id}\n"
        f"<b>Opened at:</b> {html.quote(created_at)}\n"
        f"<b>Language:</b> {html.quote(language.upper())}\n"
        f"<b>Assigned to:</b> {admin_line}\n\n"
        f"<b>First message:</b>\n{html.quote(first_message)}"
    )


def format_closed_group_ticket_message(
    *,
    ticket_id: int,
    created_at: str,
    language: str,
    first_message: str,
    admin_name: str | None,
    admin_username: str | None,
) -> str:
    admin_line = html.quote(admin_name or "Unknown")
    if admin_username:
        admin_line += f" (@{html.quote(admin_username)})"

    return (
        "<b>Ticket closed</b>\n\n"
        f"<b>Ticket ID:</b> #{ticket_id}\n"
        f"<b>Opened at:</b> {html.quote(created_at)}\n"
        f"<b>Language:</b> {html.quote(language.upper())}\n"
        f"<b>Handled by:</b> {admin_line}\n\n"
        f"<b>First message:</b>\n{html.quote(first_message)}"
    )


def format_admin_private_ticket_message(
    *,
    ticket_id: int,
    user_id: int,
    username: str | None,
    full_name: str,
    language: str,
    first_message: str,
) -> str:
    username_line = f"@{html.quote(username)}" if username else "—"
    return (
        f"<b>New assigned ticket #{ticket_id}</b>\n\n"
        f"<b>User:</b> {html.quote(full_name)}\n"
        f"<b>Username:</b> {username_line}\n"
        f"<b>User ID:</b> <code>{user_id}</code>\n"
        f"<b>Language:</b> {html.quote(language.upper())}\n\n"
        f"<b>First message:</b>\n{html.quote(first_message)}"
    )
