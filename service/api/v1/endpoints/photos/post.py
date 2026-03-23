"""
POST endpoints for photos.

## Traceability
Feature: F003 — Photo storage
Scenarios: SC004
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_connect
from schema.photos.photo_schema import PhotoCreateSchema, PhotoResponseSchema
from service.photos.photo_service import PhotoService

router = APIRouter()
service = PhotoService()


@router.post("", response_model=PhotoResponseSchema, status_code=201)
async def create_photo(
    data: PhotoCreateSchema,
    session: AsyncSession = Depends(db_connect.get_session),
):
    return await service.create_photo(
        user_id=data.user_id,
        file_id=data.file_id,
        session=session,
        file_path=data.file_path,
    )
