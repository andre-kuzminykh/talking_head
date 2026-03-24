"""
VideoService — talking-head video generation via Hedra Avatar API.

Full workflow:
1. Upload photo as image asset
2. Create generation with Hedra Avatar model + inline TTS
3. Poll until complete
4. Return video download URL

## Traceability
Feature: F007 — Video generation
Scenarios: SC010
"""
import asyncio
import logging

import httpx

from core.config import config
from core.exceptions import ExternalServiceError, ValidationError

logger = logging.getLogger(__name__)

HEDRA_BASE = "https://api.hedra.com/web-app/public"
HEDRA_AVATAR_MODEL_ID = "d1dd37a3-e39a-4854-a298-6510289f9cf2"  # Hedra Character 3
POLL_INTERVAL = 5
MAX_POLL_ATTEMPTS = 120  # 10 minutes


class VideoService:
    def __init__(self):
        self._api_key = config.HEDRA_API_KEY
        self._voice_name = config.TTS_VOICE

    def _headers(self) -> dict:
        return {"X-API-Key": self._api_key}

    async def generate_video(self, photo_url: str, audio_url: str) -> dict:
        """Generate a talking-head video.

        Args:
            photo_url: Telegram file_id for the photo.
            audio_url: Speech text (passed through from AudioService).
        """
        speech_text = audio_url
        if not photo_url.strip():
            raise ValidationError("photo_url cannot be empty")
        if not speech_text.strip():
            raise ValidationError("speech_text cannot be empty")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 1. Resolve voice_id
                voice_id = await self._get_voice_id(client)
                logger.info("Using voice_id=%s", voice_id)

                # 2. Download photo from Telegram
                photo_bytes = await self._download_telegram_photo(client, photo_url)
                logger.info("Downloaded photo (%d bytes)", len(photo_bytes))

                # 3. Upload photo as asset
                asset_id = await self._upload_image_asset(client, photo_bytes)
                logger.info("Uploaded image asset_id=%s", asset_id)

                # 4. Create generation
                generation_id = await self._create_generation(
                    client, asset_id, voice_id, speech_text,
                )
                logger.info("Created generation_id=%s", generation_id)

            # 5. Poll for completion
            async with httpx.AsyncClient(timeout=30.0) as client:
                video_url = await self._poll_generation(client, generation_id)
                logger.info("Generation complete, video_url=%s", video_url)

            return {"video_url": video_url}

        except (ValidationError, ExternalServiceError):
            raise
        except Exception as e:
            logger.error("Hedra generation failed: %s", e, exc_info=True)
            raise ExternalServiceError(f"Hedra API error: {e}")

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

    async def _download_telegram_photo(self, client: httpx.AsyncClient, file_id: str) -> bytes:
        bot_token = config.BOT_TOKEN
        resp = await client.get(
            f"https://api.telegram.org/bot{bot_token}/getFile",
            params={"file_id": file_id},
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            raise ExternalServiceError(f"Telegram getFile failed: {data}")
        file_path = data["result"]["file_path"]
        resp = await client.get(
            f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        )
        resp.raise_for_status()
        return resp.content

    async def _upload_image_asset(self, client: httpx.AsyncClient, photo_bytes: bytes) -> str:
        resp = await client.post(
            f"{HEDRA_BASE}/assets",
            headers=self._headers(),
            json={"name": "photo.jpg", "type": "image"},
        )
        logger.info("Create asset response %s: %s", resp.status_code, resp.text)
        resp.raise_for_status()
        asset = resp.json()
        asset_id = asset["id"]

        resp = await client.post(
            f"{HEDRA_BASE}/assets/{asset_id}/upload",
            headers=self._headers(),
            files={"file": ("photo.jpg", photo_bytes, "image/jpeg")},
        )
        logger.info("Upload asset response %s: %s", resp.status_code, resp.text)
        resp.raise_for_status()
        return asset_id

    async def _create_generation(
        self,
        client: httpx.AsyncClient,
        image_asset_id: str,
        voice_id: str,
        text: str,
    ) -> str:
        payload = {
            "type": "video",
            "ai_model_id": HEDRA_AVATAR_MODEL_ID,
            "start_keyframe_id": image_asset_id,
            "generated_video_inputs": {
                "text_prompt": "",
                "resolution": "720p",
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
        return data["id"]

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
                video_url = (
                    data.get("download_url")
                    or data.get("video_url")
                    or data.get("url")
                )
                if video_url:
                    return video_url
                raise ExternalServiceError(
                    f"Generation completed but no video URL: {data}"
                )

            if status in ("failed", "error"):
                raise ExternalServiceError(
                    f"Hedra generation failed: {data.get('error', data)}"
                )

            await asyncio.sleep(POLL_INTERVAL)

        raise ExternalServiceError("Generation timed out")
