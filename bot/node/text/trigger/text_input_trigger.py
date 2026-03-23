"""
TextInputTrigger — extracts speech text from user message.

## Traceability
Feature: F005 — Speech text input
Scenarios: SC007, SC008
"""
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class TextInputTrigger:
    async def run(self, message: Message, state: FSMContext) -> dict:
        return {
            "user_id": message.from_user.id,
            "text": message.text or "",
        }
