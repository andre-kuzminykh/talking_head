"""
UploadCode — photo upload logic and API call.

## Traceability
Feature: F002 — Photo upload
Feature: F003 — Photo storage
Scenarios: SC002, SC003, SC004
"""
from aiogram.fsm.context import FSMContext

from service.api.photos_api import PhotosAPI
from state.generation_states import GenerationStates


class UploadCode:
    def __init__(self):
        self._photos_api = PhotosAPI()

    async def run(self, trigger_data: dict, state: FSMContext) -> dict:
        if not trigger_data.get("has_photo"):
            return {
                "answer_name": "no_photo_error",
                "data": {},
            }

        photo = await self._photos_api.create_photo(
            user_id=trigger_data["user_id"],
            file_id=trigger_data["file_id"],
        )

        await state.update_data(selected_photo_id=photo["id"], file_id=photo["file_id"])
        await state.set_state(GenerationStates.waiting_for_text)

        return {
            "answer_name": "photo_saved",
            "data": {"photo_id": photo["id"]},
        }
