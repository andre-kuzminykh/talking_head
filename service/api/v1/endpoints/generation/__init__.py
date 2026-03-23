"""
Generation API router.

## Traceability
Feature: F006 — Audio generation
Feature: F007 — Video generation
"""
from fastapi import APIRouter

from api.v1.endpoints.generation.audio import router as audio_router
from api.v1.endpoints.generation.video import router as video_router

router = APIRouter(prefix="/generation", tags=["generation"])
router.include_router(audio_router)
router.include_router(video_router)
