"""
NoPhotoErrorAnswer — asks user to send a photo.

## Traceability
Feature: F002 — Photo upload
Scenarios: SC003
"""
from aiogram.types import Message

from core.vocab import TEXTS


class NoPhotoErrorAnswer:
    async def run(self, event: Message, user_lang: str = "en", data: dict | None = None):
        await event.answer(TEXTS["awaiting_photo"])
