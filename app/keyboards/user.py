from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


LANGUAGE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский", callback_data="set_lang:ru"),
            InlineKeyboardButton(text="English", callback_data="set_lang:en"),
            InlineKeyboardButton(text="Español", callback_data="set_lang:es"),
        ]
    ]
)
