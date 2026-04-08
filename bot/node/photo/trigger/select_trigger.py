"""
SelectTrigger — handles saved photo selection callback.

## Traceability
Feature: F004 — Saved photo selection
Scenarios: SC005, SC006
"""
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


class SelectTrigger:
    async def run(self, callback: CallbackQuery, state: FSMContext, photo_id: int) -> dict:
        await callback.answer()
        return {
            "user_id": callback.from_user.id,
            "photo_id": photo_id,
        }
