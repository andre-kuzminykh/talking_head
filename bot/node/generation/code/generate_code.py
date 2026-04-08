"""
GenerateCode — orchestrates audio + video generation pipeline.

## Traceability
Feature: F006 — Audio generation
Feature: F007 — Video generation
Feature: F008 — Result delivery
Scenarios: SC009, SC010, SC011, SC012
"""
import logging

from aiogram.fsm.context import FSMContext

from service.api.generation_api import GenerationAPI

logger = logging.getLogger(__name__)


class GenerateCode:
    def __init__(self):
        self._generation_api = GenerationAPI()

    async def run(self, trigger_data: dict, state: FSMContext) -> dict:
        try:
            # Step 1: Generate audio
            audio_result = await self._generation_api.generate_audio(
                trigger_data["speech_text"]
            )
            audio_url = audio_result.get("audio_url", "")

            # Step 2: Generate video
            video_result = await self._generation_api.generate_video(
                photo_url=trigger_data["file_id"],
                audio_url=audio_url,
            )
            video_url = video_result.get("video_url", "")

            await state.clear()

            return {
                "answer_name": "video_ready",
                "data": {"video_url": video_url},
            }

        except Exception as e:
            logger.error(f"Generation error: {e}")
            await state.clear()
            return {
                "answer_name": "generation_error",
                "data": {"error": str(e)},
            }
