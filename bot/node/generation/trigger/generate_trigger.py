"""
GenerateTrigger — collects generation data from FSM state.

## Traceability
Feature: F006 — Audio generation
Feature: F007 — Video generation
Feature: F008 — Result delivery
Scenarios: SC009, SC010, SC011
"""
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class GenerateTrigger:
    async def run(self, message: Message, state: FSMContext) -> dict:
        data = await state.get_data()
        return {
            "user_id": message.from_user.id,
            "file_id": data.get("file_id", ""),
            "speech_text": data.get("speech_text", ""),
        }
