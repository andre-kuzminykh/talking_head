"""
StartCode — welcome logic.

## Traceability
Feature: F001 — User greeting
Scenarios: SC001
"""
from aiogram.fsm.context import FSMContext


class StartCode:
    async def run(self, trigger_data: dict, state: FSMContext) -> dict:
        return {
            "answer_name": "welcome",
            "data": {
                "first_name": trigger_data.get("first_name", ""),
            },
        }
