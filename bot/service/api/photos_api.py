"""
HTTP client for the photos backend.

## Traceability
Feature: F003 — Photo storage
Feature: F004 — Saved photo selection
Scenarios: SC004, SC005, SC006
"""
import httpx

from core.config import config


class PhotosAPI:
    def __init__(self, base_url: str | None = None):
        self._base_url = base_url or config.BACKEND_URL

    async def create_photo(self, user_id: int, file_id: str, file_path: str | None = None) -> dict:
        async with httpx.AsyncClient(base_url=self._base_url) as client:
            payload = {"user_id": user_id, "file_id": file_id}
            if file_path:
                payload["file_path"] = file_path
            resp = await client.post("/api/v1/photos", json=payload)
            resp.raise_for_status()
            return resp.json()

    async def get_user_photos(self, user_id: int) -> list[dict]:
        async with httpx.AsyncClient(base_url=self._base_url) as client:
            resp = await client.get("/api/v1/photos", params={"user_id": user_id})
            resp.raise_for_status()
            return resp.json()

    async def get_photo(self, photo_id: int) -> dict:
        async with httpx.AsyncClient(base_url=self._base_url) as client:
            resp = await client.get(f"/api/v1/photos/{photo_id}")
            resp.raise_for_status()
            return resp.json()
