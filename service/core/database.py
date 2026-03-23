"""
Async database engine and session management.
"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import config


class DatabaseConnect:
    def __init__(self):
        self.engine = create_async_engine(config.database_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self):
        async with self.async_session() as session:
            yield session


db_connect = DatabaseConnect()
