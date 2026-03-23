"""
VideoService — video generation via Hedra Character 3.

## Traceability
Feature: F007 — Video generation
Scenarios: SC010

## Dependencies
- Hedra Character 3 API

## Business context
Generates talking head video with parameters:
- Aspect ratio: 1:1
- Quality: 1080p
- Max duration: 18 seconds
- Model: Hedra Character 3
"""
import httpx

from core.config import config
from core.exceptions import ExternalServiceError, ValidationError


class VideoService:
    def __init__(self):
        self._api_url = config.HEDRA_API_URL
        self._api_key = config.HEDRA_API_KEY

    async def generate_video(self, photo_url: str, audio_url: str) -> dict:
        if not photo_url.strip():
            raise ValidationError("photo_url cannot be empty")
        if not audio_url.strip():
            raise ValidationError("audio_url cannot be empty")

        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                resp = await client.post(
                    f"{self._api_url}/v1/characters",
                    headers={"X-API-Key": self._api_key},
                    json={
                        "photo_url": photo_url,
                        "audio_url": audio_url,
                        "aspect_ratio": "1:1",
                        "resolution": "1080p",
                        "model": "character-3",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                return {"video_url": data.get("video_url", "")}
        except httpx.HTTPError as e:
            raise ExternalServiceError(f"Hedra API error: {e}")
