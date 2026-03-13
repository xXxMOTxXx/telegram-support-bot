from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def accept_ticket_keyboard(ticket_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Accept ticket", callback_data=f"accept_ticket:{ticket_id}")]
        ]
    )



def close_ticket_keyboard(ticket_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Close ticket", callback_data=f"close_ticket:{ticket_id}")]
        ]
    )
