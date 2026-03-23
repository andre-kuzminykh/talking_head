"""
Audio generation endpoint.

## Traceability
Feature: F006 — Audio generation
Scenarios: SC009
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field

from service.generation.audio_service import AudioService

router = APIRouter()
service = AudioService()


class AudioRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class AudioResponse(BaseModel):
    audio_url: str


@router.post("/audio", response_model=AudioResponse)
async def generate_audio(data: AudioRequest):
    result = await service.generate_audio(data.text)
    return result
