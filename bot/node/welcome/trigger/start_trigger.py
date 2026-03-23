"""
StartTrigger — handles /start command input.

## Traceability
Feature: F001 — User greeting
Scenarios: SC001
"""
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class StartTrigger:
    async def run(self, message: Message, state: FSMContext) -> dict:
        await state.clear()
        return {
            "user_id": message.from_user.id,
            "username": message.from_user.username or "",
            "first_name": message.from_user.first_name or "",
        }
