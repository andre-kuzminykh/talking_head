"""
Widget: Upload photo.

## Traceability
Feature: F002 — Photo upload
Feature: F003 — Photo storage
Scenarios: SC002, SC003, SC004
SC002 — photo sent → saved → answer: photo_saved
SC003 — non-photo sent → answer: no_photo_error
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from callback.photo_callback import PhotoCallback
from node.photo.trigger.upload_trigger import UploadTrigger
from node.photo.code.upload_code import UploadCode
from node.photo.answer.photo_saved_answer import PhotoSavedAnswer
from node.photo.answer.no_photo_error_answer import NoPhotoErrorAnswer
from state.generation_states import GenerationStates

upload_photo_router = Router(name="upload_photo")

ANSWER_REGISTRY = {
    "photo_saved": PhotoSavedAnswer(),
    "no_photo_error": NoPhotoErrorAnswer(),
}


@upload_photo_router.callback_query(PhotoCallback.filter(F.action == "upload"))
async def handle_upload_prompt(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(GenerationStates.waiting_for_photo)
    await callback.message.edit_text("Please send me a photo.")


@upload_photo_router.message(GenerationStates.waiting_for_photo, F.photo)
async def handle_photo_upload(message: Message, state: FSMContext):
    trigger = UploadTrigger()
    trigger_data = await trigger.run(message, state)

    code = UploadCode()
    code_result = await code.run(trigger_data, state)

    answer = ANSWER_REGISTRY[code_result["answer_name"]]
    await answer.run(event=message, user_lang="en", data=code_result["data"])


@upload_photo_router.message(GenerationStates.waiting_for_photo)
async def handle_non_photo(message: Message, state: FSMContext):
    trigger = UploadTrigger()
    trigger_data = await trigger.run(message, state)

    code = UploadCode()
    code_result = await code.run(trigger_data, state)

    answer = ANSWER_REGISTRY[code_result["answer_name"]]
    await answer.run(event=message, user_lang="en", data=code_result["data"])
