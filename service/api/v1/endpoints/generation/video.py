"""
Video generation endpoint.

## Traceability
Feature: F007 — Video generation
Scenarios: SC010
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field

from service.generation.video_service import VideoService

router = APIRouter()
service = VideoService()


class VideoRequest(BaseModel):
    photo_url: str = Field(..., min_length=1)
    audio_url: str = Field(..., min_length=1)


class VideoResponse(BaseModel):
    video_url: str


@router.post("/video", response_model=VideoResponse)
async def generate_video(data: VideoRequest):
    result = await service.generate_video(data.photo_url, data.audio_url)
    return result
