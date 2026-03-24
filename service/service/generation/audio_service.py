"""
AudioService — validates text for TTS generation.

Hedra API does not have a standalone TTS endpoint — text-to-speech
is performed inline during video generation.  This service validates
the input and passes the text through so the video step can use it.

## Traceability
Feature: F006 — Audio generation
Scenarios: SC009
"""
import logging

from core.exceptions import ValidationError

logger = logging.getLogger(__name__)


class AudioService:
    async def generate_audio(self, text: str) -> dict:
        if not text.strip():
            raise ValidationError("Text cannot be empty")

        logger.info("Audio text accepted (%d chars), will be synthesised during video generation", len(text))
        # Return the text itself — the video service will send it to Hedra's
        # inline TTS when creating the generation.
        return {"audio_url": text}
