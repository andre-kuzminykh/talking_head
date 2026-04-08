"""
UploadTrigger — extracts photo data from user message.

## Traceability
Feature: F002 — Photo upload
Scenarios: SC002, SC003
"""
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class UploadTrigger:
    async def run(self, message: Message, state: FSMContext) -> dict:
        if not message.photo:
            return {"has_photo": False}

        photo = message.photo[-1]  # highest resolution
        return {
            "has_photo": True,
            "user_id": message.from_user.id,
            "file_id": photo.file_id,
            "file_unique_id": photo.file_unique_id,
        }
