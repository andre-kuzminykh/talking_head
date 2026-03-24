"""
AudioService — text-to-speech generation using Andre AIT eng voice.

## Traceability
Feature: F006 — Audio generation
Scenarios: SC009

## Dependencies
- External TTS API
"""
import logging

import httpx

from core.config import config
from core.exceptions import ExternalServiceError, ValidationError

logger = logging.getLogger(__name__)


class AudioService:
    def __init__(self):
        self._api_url = config.TTS_API_URL
        self._api_key = config.HEDRA_API_KEY
        self._voice = config.TTS_VOICE

    async def generate_audio(self, text: str) -> dict:
        if not text.strip():
            raise ValidationError("Text cannot be empty")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{self._api_url}/v1/audio",
                    headers={"X-API-Key": self._api_key},
                    json={"text": text, "voice": self._voice},
                )
                logger.info("Hedra TTS response %s: %s", resp.status_code, resp.text)
                resp.raise_for_status()
                data = resp.json()
                return {"audio_url": data.get("audio_url", "")}
        except httpx.HTTPError as e:
            logger.error("TTS service error: %s", e)
            raise ExternalServiceError(f"TTS service error: {e}")
