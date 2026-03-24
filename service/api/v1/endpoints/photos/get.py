"""
GET endpoints for photos.

## Traceability
Feature: F004 — Saved photo selection
Scenarios: SC005, SC006
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_connect
from schema.photos.photo_schema import PhotoResponseSchema
from service.photos.photo_service import PhotoService

router = APIRouter()
service = PhotoService()


@router.get("/", response_model=list[PhotoResponseSchema])
async def get_user_photos(
    user_id: int = Query(..., description="Telegram user ID"),
    session: AsyncSession = Depends(db_connect.get_session),
):
    return await service.get_user_photos(user_id, session)


@router.get("/{photo_id}", response_model=PhotoResponseSchema)
async def get_photo(
    photo_id: int,
    session: AsyncSession = Depends(db_connect.get_session),
):
    return await service.get_photo(photo_id, session)
