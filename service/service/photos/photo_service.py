"""
PhotoService — photo management business logic.

## Traceability
Feature: F003 — Photo storage
Scenarios: SC004, SC005, SC006

## Dependencies
- PhotoRepository
"""
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError, ValidationError
from repository.photos.photo_repository import PhotoRepository


class PhotoService:
    def __init__(self):
        self._repo = PhotoRepository()

    async def create_photo(
        self,
        user_id: int,
        file_id: str,
        session: AsyncSession,
        file_path: str | None = None,
    ):
        if not file_id.strip():
            raise ValidationError("file_id cannot be empty")
        return await self._repo.create(
            session, user_id=user_id, file_id=file_id, file_path=file_path
        )

    async def get_user_photos(self, user_id: int, session: AsyncSession):
        return await self._repo.get_by_user_id(session, user_id)

    async def get_photo(self, photo_id: int, session: AsyncSession):
        photo = await self._repo.get_by_id(session, photo_id)
        if photo is None:
            raise NotFoundError(f"Photo {photo_id} not found")
        return photo

    async def delete_photo(self, photo_id: int, session: AsyncSession):
        deleted = await self._repo.delete(session, photo_id)
        if not deleted:
            raise NotFoundError(f"Photo {photo_id} not found")
        return True
