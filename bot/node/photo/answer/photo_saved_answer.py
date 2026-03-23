"""
PhotoSavedAnswer — confirms photo was saved.

## Traceability
Feature: F002 — Photo upload
Feature: F003 — Photo storage
Scenarios: SC002, SC004
"""
from aiogram.types import Message

from core.vocab import TEXTS


class PhotoSavedAnswer:
    async def run(self, event: Message, user_lang: str = "en", data: dict | None = None):
        await event.answer(TEXTS["photo_saved"])
