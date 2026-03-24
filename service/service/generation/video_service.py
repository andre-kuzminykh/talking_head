"""
VideoService — video generation via Hedra API.

Full workflow:
1. GET /voices → pick voice_id
2. GET /models → pick model_id (character-3)
3. POST /assets → create image asset
4. POST /assets/{id}/upload → upload photo bytes
5. POST /generations → submit generation with inline TTS
6. Poll GET /generations/{id}/status until complete
7. Return video download URL

## Traceability
Feature: F007 — Video generation
Scenarios: SC010

## Dependencies
- Hedra API (https://api.hedra.com)
"""
import asyncio
import logging

import httpx

from core.config import config
from core.exceptions import ExternalServiceError, ValidationError

logger = logging.getLogger(__name__)

HEDRA_BASE = "https://api.hedra.com/web-app/public"
POLL_INTERVAL = 5  # seconds
MAX_POLL_ATTEMPTS = 120  # 10 minutes max


class VideoService:
    def __init__(self):
        self._api_key = config.HEDRA_API_KEY
        self._voice_name = config.TTS_VOICE

    def _headers(self) -> dict:
        return {"X-API-Key": self._api_key}

    async def generate_video(self, photo_url: str, audio_url: str) -> dict:
        """Generate a talking-head video.

        Args:
            photo_url: Telegram file_id — used to download the photo via
                       Telegram Bot API file_path stored in our DB, OR a
                       direct URL / file_id string.
            audio_url: Actually the speech text (passed through from
                       AudioService).  Hedra performs TTS inline.
        """
        speech_text = audio_url  # see AudioService — this is the raw text
        if not photo_url.strip():
            raise ValidationError("photo_url cannot be empty")
        if not speech_text.strip():
            raise ValidationError("speech_text cannot be empty")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 1. Resolve voice_id
                voice_id = await self._get_voice_id(client)
                logger.info("Using voice_id=%s", voice_id)

                # 2. Resolve model_id
                model_id = await self._get_model_id(client)
                logger.info("Using model_id=%s", model_id)

                # 3-4. Upload photo as asset
                photo_bytes = await self._download_telegram_photo(client, photo_url)
                asset_id = await self._upload_image_asset(client, photo_bytes)
                logger.info("Uploaded image asset_id=%s", asset_id)

                # 5. Create generation
                generation_id = await self._create_generation(
                    client, model_id, asset_id, voice_id, speech_text,
                )
                logger.info("Created generation_id=%s", generation_id)

            # 6. Poll for completion (with a longer timeout)
            async with httpx.AsyncClient(timeout=30.0) as client:
                video_url = await self._poll_generation(client, generation_id)
                logger.info("Generation complete, video_url=%s", video_url)

            return {"video_url": video_url}

        except (ValidationError, ExternalServiceError):
            raise
        except Exception as e:
            logger.error("Hedra generation failed: %s", e, exc_info=True)
            raise ExternalServiceError(f"Hedra API error: {e}")

    # ------------------------------------------------------------------
    # Hedra API helpers
    # ------------------------------------------------------------------

    async def _get_voice_id(self, client: httpx.AsyncClient) -> str:
        resp = await client.get(f"{HEDRA_BASE}/voices", headers=self._headers())
        resp.raise_for_status()
        voices = resp.json()
        # Try to find the configured voice by name
        for v in voices:
            name = v.get("name", "") or v.get("voice_name", "")
            if self._voice_name.lower() in name.lower():
                return v.get("id") or v.get("voice_id")
        # Fallback: use the first available voice
        if voices:
            return voices[0].get("id") or voices[0].get("voice_id")
        raise ExternalServiceError("No voices available in Hedra API")

    async def _get_model_id(self, client: httpx.AsyncClient) -> str:
        resp = await client.get(f"{HEDRA_BASE}/models", headers=self._headers())
        resp.raise_for_status()
        models = resp.json()
        # Prefer character-3
        for m in models:
            name = m.get("name", "") or m.get("model_name", "")
            if "character-3" in name.lower():
                return m.get("id") or m.get("model_id")
        if models:
            return models[0].get("id") or models[0].get("model_id")
        raise ExternalServiceError("No models available in Hedra API")

    async def _download_telegram_photo(self, client: httpx.AsyncClient, file_id: str) -> bytes:
        """Download photo from Telegram using the Bot API."""
        bot_token = config.BOT_TOKEN
        # Get file path
        resp = await client.get(
            f"https://api.telegram.org/bot{bot_token}/getFile",
            params={"file_id": file_id},
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            raise ExternalServiceError(f"Telegram getFile failed: {data}")
        file_path = data["result"]["file_path"]

        # Download file
        resp = await client.get(
            f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        )
        resp.raise_for_status()
        return resp.content

    async def _upload_image_asset(self, client: httpx.AsyncClient, photo_bytes: bytes) -> str:
        # Create asset
        resp = await client.post(
            f"{HEDRA_BASE}/assets",
            headers=self._headers(),
            json={"name": "photo.jpg", "type": "image"},
        )
        resp.raise_for_status()
        asset = resp.json()
        asset_id = asset.get("id") or asset.get("asset_id")

        # Upload file content
        resp = await client.post(
            f"{HEDRA_BASE}/assets/{asset_id}/upload",
            headers=self._headers(),
            files={"file": ("photo.jpg", photo_bytes, "image/jpeg")},
        )
        resp.raise_for_status()
        return asset_id

    async def _create_generation(
        self,
        client: httpx.AsyncClient,
        model_id: str,
        image_asset_id: str,
        voice_id: str,
        text: str,
    ) -> str:
        payload = {
            "type": "video",
            "ai_model_id": model_id,
            "start_keyframe_id": image_asset_id,
            "generated_video_inputs": {
                "text_prompt": "",
                "resolution": "1080p",
                "aspect_ratio": "1:1",
            },
            "audio_generation": {
                "type": "text_to_speech",
                "voice_id": voice_id,
                "text": text,
            },
        }
        resp = await client.post(
            f"{HEDRA_BASE}/generations",
            headers=self._headers(),
            json=payload,
        )
        logger.info("Create generation response %s: %s", resp.status_code, resp.text)
        resp.raise_for_status()
        data = resp.json()
        return data.get("id") or data.get("generation_id")

    async def _poll_generation(self, client: httpx.AsyncClient, generation_id: str) -> str:
        for attempt in range(MAX_POLL_ATTEMPTS):
            resp = await client.get(
                f"{HEDRA_BASE}/generations/{generation_id}/status",
                headers=self._headers(),
            )
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status", "")
            logger.info("Generation %s status: %s (attempt %d)", generation_id, status, attempt + 1)

            if status in ("completed", "complete", "done"):
                video_url = data.get("download_url") or data.get("video_url") or data.get("url")
                if video_url:
                    return video_url
                raise ExternalServiceError(f"Generation completed but no video URL in response: {data}")

            if status in ("failed", "error"):
                error_msg = data.get("error", "Unknown error")
                raise ExternalServiceError(f"Hedra generation failed: {error_msg}")

            await asyncio.sleep(POLL_INTERVAL)

        raise ExternalServiceError("Generation timed out after polling")
