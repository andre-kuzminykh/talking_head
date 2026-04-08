"""
VideoService — talking-head video generation via Hedra Character 3.

Workflow:
1. Download photo from Telegram
2. Upload as Hedra image asset
3. Create video generation with image + audio asset
4. Poll until complete
5. Return video URL

## Traceability
Feature: F007 — Video generation
Scenarios: SC010
"""
import asyncio

import httpx

from core.config import config
from core.exceptions import ExternalServiceError, ValidationError

HEDRA_BASE = "https://api.hedra.com/web-app/public"
HEDRA_MODEL_ID = "d1dd37a3-e39a-4854-a298-6510289f9cf2"  # Hedra Character 3
POLL_INTERVAL = 5
MAX_POLL_ATTEMPTS = 120  # 10 minutes


class VideoService:
    def __init__(self):
        self._api_key = config.HEDRA_API_KEY

    def _headers(self) -> dict:
        return {"X-API-Key": self._api_key}

    async def generate_video(self, photo_url: str, audio_url: str) -> dict:
        """Generate a talking-head video.

        Args:
            photo_url: Telegram file_id for the photo.
            audio_url: Hedra audio asset_id (from AudioService).
        """
        audio_asset_id = audio_url
        if not photo_url.strip():
            raise ValidationError("photo_url cannot be empty")
        if not audio_asset_id.strip():
            raise ValidationError("audio_asset_id cannot be empty")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 1. Download photo from Telegram
                photo_bytes = await self._download_telegram_photo(client, photo_url)
                print(f"[HEDRA VIDEO] Downloaded photo ({len(photo_bytes)} bytes)")

                # 2. Upload photo as asset
                image_asset_id = await self._upload_image_asset(client, photo_bytes)
                print(f"[HEDRA VIDEO] Uploaded image asset_id={image_asset_id}")

                # 3. Create video generation
                generation_id = await self._create_generation(
                    client, image_asset_id, audio_asset_id,
                )
                print(f"[HEDRA VIDEO] Created generation_id={generation_id}")

            # 4. Poll for completion
            async with httpx.AsyncClient(timeout=30.0) as client:
                video_url = await self._poll_generation(client, generation_id)
                print(f"[HEDRA VIDEO] Complete, video_url={video_url}")

            return {"video_url": video_url}

        except (ValidationError, ExternalServiceError):
            raise
        except Exception as e:
            print(f"[HEDRA VIDEO] ERROR: {e}")
            raise ExternalServiceError(f"Hedra API error: {e}")

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
        resp.raise_for_status()
        asset = resp.json()
        asset_id = asset["id"]

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
        image_asset_id: str,
        audio_asset_id: str,
    ) -> str:
        payload = {
            "type": "video",
            "ai_model_id": HEDRA_MODEL_ID,
            "start_keyframe_id": image_asset_id,
            "audio_id": audio_asset_id,
            "generated_video_inputs": {
                "text_prompt": "",
                "resolution": "720p",
                "aspect_ratio": "1:1",
            },
        }
        resp = await client.post(
            f"{HEDRA_BASE}/generations",
            headers=self._headers(),
            json=payload,
        )
        print(f"[HEDRA VIDEO] Create generation response {resp.status_code}: {resp.text}")
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
            print(f"[HEDRA VIDEO] Status: {status} (attempt {attempt + 1})")

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
