"""
GenerationErrorAnswer — informs user about generation failure.

## Traceability
Feature: F008 — Result delivery
Scenarios: SC012
"""
from aiogram.types import Message

from core.vocab import TEXTS


class GenerationErrorAnswer:
    async def run(self, event: Message, user_lang: str = "en", data: dict | None = None):
        await event.answer(TEXTS["generation_error"])
