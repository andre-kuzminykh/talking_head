"""
PhotoRepository — data access for photos.

## Traceability
Feature: F003 — Photo storage
Scenarios: SC004, SC005, SC006
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.photos.photo_model import PhotoModel
from repository.base_repository import BaseRepository


class PhotoRepository(BaseRepository[PhotoModel]):
    def __init__(self):
        super().__init__(PhotoModel)

    async def get_by_user_id(
        self, session: AsyncSession, user_id: int
    ) -> list[PhotoModel]:
        result = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return list(result.scalars().all())
