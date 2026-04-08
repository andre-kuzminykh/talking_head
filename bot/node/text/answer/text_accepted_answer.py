"""
TextAcceptedAnswer — confirms text received and shows generating status.

## Traceability
Feature: F005 — Speech text input
Scenarios: SC007
"""
from aiogram.types import Message

from core.vocab import TEXTS


class TextAcceptedAnswer:
    async def run(self, event: Message, user_lang: str = "en", data: dict | None = None):
        await event.answer(TEXTS["generating"])
