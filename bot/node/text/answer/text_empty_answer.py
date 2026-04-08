"""
TextEmptyAnswer — asks user for non-empty text.

## Traceability
Feature: F005 — Speech text input
Scenarios: SC008
"""
from aiogram.types import Message

from core.vocab import TEXTS


class TextEmptyAnswer:
    async def run(self, event: Message, user_lang: str = "en", data: dict | None = None):
        await event.answer(TEXTS["text_empty"])
