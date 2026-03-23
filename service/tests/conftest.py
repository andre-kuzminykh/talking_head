"""
Global test fixtures for backend service.
"""
import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from model.base_model import Base
from core import app, db_connect


def _test_db_url() -> str:
    host = os.getenv("TEST_DB_HOST", os.getenv("DB_HOST", "localhost"))
    port = os.getenv("TEST_DB_PORT", os.getenv("DB_PORT", "5432"))
    user = os.getenv("TEST_DB_USER", os.getenv("DB_USER", "postgres"))
    password = os.getenv("TEST_DB_PASSWORD", os.getenv("DB_PASSWORD", "postgres"))
    name = os.getenv("TEST_DB_NAME", os.getenv("DB_NAME", "test_db"))
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


@pytest_asyncio.fixture
async def async_session():
    engine = create_async_engine(_test_db_url(), echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    sm = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with sm() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def client(async_session):
    import api.v1.include_router  # noqa: F401

    async def override():
        yield async_session

    app.dependency_overrides[db_connect.get_session] = override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
