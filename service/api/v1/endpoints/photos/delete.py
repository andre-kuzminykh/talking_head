"""
DELETE endpoints for photos.

## Traceability
Feature: F003 — Photo storage
Scenarios: SC004
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_connect
from service.photos.photo_service import PhotoService

router = APIRouter()
service = PhotoService()


@router.delete("/{photo_id}", status_code=204)
async def delete_photo(
    photo_id: int,
    session: AsyncSession = Depends(db_connect.get_session),
):
    await service.delete_photo(photo_id, session)
