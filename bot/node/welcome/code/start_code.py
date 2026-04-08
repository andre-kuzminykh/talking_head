"""
StartCode — welcome logic.

## Traceability
Feature: F001 — User greeting
Scenarios: SC001

## Flow
/start immediately sets waiting_for_photo state so the user can
send a photo right away. A "Select saved photo" button is also shown.
"""
from aiogram.fsm.context import FSMContext

from state.generation_states import GenerationStates


class StartCode:
    async def run(self, trigger_data: dict, state: FSMContext) -> dict:
        await state.set_state(GenerationStates.waiting_for_photo)
        return {
            "answer_name": "welcome",
            "data": {
                "first_name": trigger_data.get("first_name", ""),
            },
        }
