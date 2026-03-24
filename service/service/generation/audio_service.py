"""
AudioService — text-to-speech via Hedra API.

## Traceability
Feature: F006 — Audio generation
Scenarios: SC009
"""
import asyncio

import httpx

from core.config import config
from core.exceptions import ExternalServiceError, ValidationError

HEDRA_BASE = "https://api.hedra.com/web-app/public"
POLL_INTERVAL = 2
MAX_POLL_ATTEMPTS = 30  # 60 seconds


class AudioService:
    def __init__(self):
        self._api_key = config.HEDRA_API_KEY
        self._voice_name = config.TTS_VOICE

    def _headers(self) -> dict:
        return {"X-API-Key": self._api_key}

    async def generate_audio(self, text: str) -> dict:
        if not text.strip():
            raise ValidationError("Text cannot be empty")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 1. Resolve voice_id
                voice_id = await self._get_voice_id(client)
                print(f"[HEDRA TTS] Using voice_id={voice_id}")

                # 2. Create TTS generation
                resp = await client.post(
                    f"{HEDRA_BASE}/generations",
                    headers=self._headers(),
                    json={
                        "type": "text_to_speech",
                        "voice_id": voice_id,
                        "text": text,
                    },
                )
                print(f"[HEDRA TTS] Create response {resp.status_code}: {resp.text}")
                resp.raise_for_status()
                data = resp.json()
                generation_id = data["id"]
                asset_id = data.get("asset_id", "")

                # 3. Poll until TTS is done
                asset_id = await self._poll_tts(client, generation_id, asset_id)
                print(f"[HEDRA TTS] Done, asset_id={asset_id}")

                # Return asset_id as "audio_url" — VideoService will use it
                return {"audio_url": asset_id}

        except (ValidationError, ExternalServiceError):
            raise
        except Exception as e:
            print(f"[HEDRA TTS] ERROR: {e}")
            raise ExternalServiceError(f"TTS error: {e}")

    async def _get_voice_id(self, client: httpx.AsyncClient) -> str:
        resp = await client.get(f"{HEDRA_BASE}/voices", headers=self._headers())
        resp.raise_for_status()
        voices = resp.json()
        for v in voices:
            if self._voice_name.lower() in v.get("name", "").lower():
                return v["id"]
        if voices:
            return voices[0]["id"]
        raise ExternalServiceError("No voices available")

    async def _poll_tts(self, client: httpx.AsyncClient, generation_id: str, asset_id: str) -> str:
        for attempt in range(MAX_POLL_ATTEMPTS):
            resp = await client.get(
                f"{HEDRA_BASE}/generations/{generation_id}/status",
                headers=self._headers(),
            )
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status", "")
            print(f"[HEDRA TTS] Status: {status} (attempt {attempt + 1})")

            if status in ("completed", "complete", "done"):
                return data.get("asset_id", asset_id) or asset_id

            if status in ("failed", "error"):
                raise ExternalServiceError(f"TTS failed: {data.get('error', data)}")

            await asyncio.sleep(POLL_INTERVAL)

        raise ExternalServiceError("TTS timed out")
