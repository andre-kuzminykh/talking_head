"""
Widget: Select saved photo.

## Traceability
Feature: F004 — Saved photo selection
Scenarios: SC005, SC006
SC005 — has photos → answer: photo_list → pick → answer: photo_selected
SC006 — no photos → answer: no_photos
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from callback.photo_callback import PhotoCallback
from node.photo.code.select_code import SelectCode
from node.photo.answer.photo_list_answer import PhotoListAnswer
from node.photo.answer.no_photos_answer import NoPhotosAnswer
from node.photo.answer.photo_selected_answer import PhotoSelectedAnswer

select_photo_router = Router(name="select_photo")

ANSWER_REGISTRY = {
    "photo_list": PhotoListAnswer(),
    "no_photos": NoPhotosAnswer(),
    "photo_selected": PhotoSelectedAnswer(),
}


@select_photo_router.callback_query(PhotoCallback.filter(F.action == "select"))
async def handle_select_prompt(callback: CallbackQuery, state: FSMContext):
    code = SelectCode()
    code_result = await code.run(
        {"user_id": callback.from_user.id, "action": "list"},
        state,
    )

    answer = ANSWER_REGISTRY[code_result["answer_name"]]
    await answer.run(event=callback, user_lang="en", data=code_result["data"])


@select_photo_router.callback_query(PhotoCallback.filter(F.action == "pick"))
async def handle_pick_photo(
    callback: CallbackQuery,
    callback_data: PhotoCallback,
    state: FSMContext,
):
    code = SelectCode()
    code_result = await code.run(
        {
            "user_id": callback.from_user.id,
            "action": "pick",
            "photo_id": callback_data.photo_id,
        },
        state,
    )

    answer = ANSWER_REGISTRY[code_result["answer_name"]]
    await answer.run(event=callback, user_lang="en", data=code_result["data"])
