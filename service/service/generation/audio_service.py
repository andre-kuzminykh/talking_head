"""
AudioService — text-to-speech via ElevenLabs API + Hedra asset upload.

Flow:
1. Send text to ElevenLabs TTS → receive audio bytes (mp3)
2. Upload audio to Hedra as asset → receive asset_id
3. Return asset_id as audio_url for VideoService

## Traceability
Feature: F006 — Audio generation
Scenarios: SC009
"""
import httpx

from core.config import config
from core.exceptions import ExternalServiceError, ValidationError

HEDRA_BASE = "https://api.hedra.com/web-app/public"
ELEVENLABS_BASE = "https://api.elevenlabs.io/v1"


class AudioService:
    def __init__(self):
        self._hedra_api_key = config.HEDRA_API_KEY
        self._elevenlabs_api_key = config.ELEVENLABS_API_KEY
        self._voice_id = config.ELEVENLABS_VOICE_ID

    def _hedra_headers(self) -> dict:
        return {"X-API-Key": self._hedra_api_key}

    def _elevenlabs_headers(self) -> dict:
        return {
            "xi-api-key": self._elevenlabs_api_key,
            "Content-Type": "application/json",
        }

    async def generate_audio(self, text: str) -> dict:
        if not text.strip():
            raise ValidationError("Text cannot be empty")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 1. Generate audio via ElevenLabs
                audio_bytes = await self._elevenlabs_tts(client, text)
                print(f"[11LABS TTS] Generated audio ({len(audio_bytes)} bytes)")

                # 2. Upload audio to Hedra as asset
                asset_id = await self._upload_audio_asset(client, audio_bytes)
                print(f"[11LABS TTS] Uploaded to Hedra, asset_id={asset_id}")

                return {"audio_url": asset_id}

        except (ValidationError, ExternalServiceError):
            raise
        except Exception as e:
            print(f"[11LABS TTS] ERROR: {e}")
            raise ExternalServiceError(f"TTS error: {e}")

    async def _elevenlabs_tts(self, client: httpx.AsyncClient, text: str) -> bytes:
        resp = await client.post(
            f"{ELEVENLABS_BASE}/text-to-speech/{self._voice_id}",
            headers=self._elevenlabs_headers(),
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
            },
        )
        if resp.status_code != 200:
            print(f"[11LABS TTS] Error {resp.status_code}: {resp.text}")
            raise ExternalServiceError(
                f"ElevenLabs TTS failed ({resp.status_code}): {resp.text}"
            )
        return resp.content

    async def _upload_audio_asset(
        self, client: httpx.AsyncClient, audio_bytes: bytes
    ) -> str:
        # Create asset record in Hedra
        resp = await client.post(
            f"{HEDRA_BASE}/assets",
            headers=self._hedra_headers(),
            json={"name": "speech.mp3", "type": "audio"},
        )
        resp.raise_for_status()
        asset = resp.json()
        asset_id = asset["id"]

        # Upload audio file
        resp = await client.post(
            f"{HEDRA_BASE}/assets/{asset_id}/upload",
            headers=self._hedra_headers(),
            files={"file": ("speech.mp3", audio_bytes, "audio/mpeg")},
        )
        resp.raise_for_status()
        return asset_id
