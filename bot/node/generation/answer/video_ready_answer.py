"""
VideoReadyAnswer — sends generated video to user.

## Traceability
Feature: F008 — Result delivery
Scenarios: SC011
"""
from aiogram.types import Message, URLInputFile

from core.vocab import TEXTS


class VideoReadyAnswer:
    async def run(self, event: Message, user_lang: str = "en", data: dict | None = None):
        video_url = data.get("video_url", "") if data else ""
        if video_url:
            video = URLInputFile(video_url)
            await event.answer_video(video=video, caption=TEXTS["video_ready"])
        else:
            await event.answer(TEXTS["generation_error"])
