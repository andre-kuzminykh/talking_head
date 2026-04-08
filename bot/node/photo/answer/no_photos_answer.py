"""
NoPhotosAnswer — informs user has no saved photos.

## Traceability
Feature: F004 — Saved photo selection
Scenarios: SC006
"""
from aiogram.types import Message, CallbackQuery

from core.vocab import TEXTS


class NoPhotosAnswer:
    async def run(self, event: Message | CallbackQuery, user_lang: str = "en", data: dict | None = None):
        text = TEXTS["no_photos"]
        if isinstance(event, CallbackQuery):
            await event.message.edit_text(text)
        else:
            await event.answer(text)
