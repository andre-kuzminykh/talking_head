"""
SelectCode — saved photo selection logic.

## Traceability
Feature: F004 — Saved photo selection
Scenarios: SC005, SC006
"""
from aiogram.fsm.context import FSMContext

from service.api.photos_api import PhotosAPI
from state.generation_states import GenerationStates


class SelectCode:
    def __init__(self):
        self._photos_api = PhotosAPI()

    async def run(self, trigger_data: dict, state: FSMContext) -> dict:
        action = trigger_data.get("action", "list")

        if action == "list":
            photos = await self._photos_api.get_user_photos(trigger_data["user_id"])
            if not photos:
                return {
                    "answer_name": "no_photos",
                    "data": {},
                }
            return {
                "answer_name": "photo_list",
                "data": {"photos": photos},
            }

        # action == "pick"
        photo = await self._photos_api.get_photo(trigger_data["photo_id"])
        await state.update_data(selected_photo_id=photo["id"], file_id=photo["file_id"])
        await state.set_state(GenerationStates.waiting_for_text)

        return {
            "answer_name": "photo_selected",
            "data": {"photo_id": photo["id"]},
        }
