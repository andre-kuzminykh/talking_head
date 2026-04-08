"""
PhotoSelectedAnswer — confirms photo was selected.

## Traceability
Feature: F004 — Saved photo selection
Scenarios: SC005
"""
from aiogram.types import CallbackQuery

from core.vocab import TEXTS


class PhotoSelectedAnswer:
    async def run(self, event: CallbackQuery, user_lang: str = "en", data: dict | None = None):
        await event.message.edit_text(TEXTS["awaiting_text"])
