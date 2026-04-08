"""
TextInputCode — validates speech text and transitions to generation.

## Traceability
Feature: F005 — Speech text input
Scenarios: SC007, SC008
"""
from aiogram.fsm.context import FSMContext

from state.generation_states import GenerationStates


class TextInputCode:
    async def run(self, trigger_data: dict, state: FSMContext) -> dict:
        text = trigger_data.get("text", "").strip()

        if not text:
            return {
                "answer_name": "text_empty",
                "data": {},
            }

        await state.update_data(speech_text=text)
        await state.set_state(GenerationStates.generating)

        return {
            "answer_name": "text_accepted",
            "data": {"text": text},
        }
