"""
WelcomeAnswer — renders welcome screen.

## Traceability
Feature: F001 — User greeting
Scenarios: SC001
"""
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from core.vocab import TEXTS, BUTTONS
from callback.photo_callback import PhotoCallback


class WelcomeAnswer:
    async def run(self, event: Message, user_lang: str = "en", data: dict | None = None):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=BUTTONS["upload_photo"],
                        callback_data=PhotoCallback(action="upload").pack(),
                    ),
                    InlineKeyboardButton(
                        text=BUTTONS["select_photo"],
                        callback_data=PhotoCallback(action="select").pack(),
                    ),
                ],
            ]
        )
        await event.answer(TEXTS["welcome"], reply_markup=keyboard)
