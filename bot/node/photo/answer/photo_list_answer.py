"""
PhotoListAnswer — shows list of saved photos.

## Traceability
Feature: F004 — Saved photo selection
Scenarios: SC005
"""
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from core.vocab import TEXTS
from callback.photo_callback import PhotoCallback


class PhotoListAnswer:
    async def run(self, event: Message | CallbackQuery, user_lang: str = "en", data: dict | None = None):
        photos = data.get("photos", []) if data else []
        buttons = []
        for photo in photos:
            buttons.append([
                InlineKeyboardButton(
                    text=f"Photo #{photo['id']}",
                    callback_data=PhotoCallback(action="pick", photo_id=photo["id"]).pack(),
                )
            ])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        text = TEXTS["photo_select_prompt"]
        if isinstance(event, CallbackQuery):
            await event.message.edit_text(text, reply_markup=keyboard)
        else:
            await event.answer(text, reply_markup=keyboard)
