"""
Generic base repository with CRUD operations.
"""
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    async def get_by_id(self, session: AsyncSession, entity_id: int) -> T | None:
        return await session.get(self.model, entity_id)

    async def get_all(self, session: AsyncSession) -> list[T]:
        result = await session.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, **kwargs) -> T:
        instance = self.model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        instance = await self.get_by_id(session, entity_id)
        if instance is None:
            return False
        await session.delete(instance)
        await session.commit()
        return True
