"""
HTTP client for audio and video generation backend.

## Traceability
Feature: F006 — Audio generation
Feature: F007 — Video generation
Scenarios: SC009, SC010
"""
import httpx

from core.config import config


class GenerationAPI:
    def __init__(self, base_url: str | None = None):
        self._base_url = base_url or config.BACKEND_URL

    async def generate_audio(self, text: str) -> dict:
        async with httpx.AsyncClient(base_url=self._base_url, timeout=120.0) as client:
            resp = await client.post("/api/v1/generation/audio", json={"text": text})
            resp.raise_for_status()
            return resp.json()

    async def generate_video(self, photo_url: str, audio_url: str) -> dict:
        async with httpx.AsyncClient(base_url=self._base_url, timeout=600.0) as client:
            resp = await client.post(
                "/api/v1/generation/video",
                json={"photo_url": photo_url, "audio_url": audio_url},
            )
            resp.raise_for_status()
            return resp.json()
