import asyncio

import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from db.base import Base


TEST_DATABASE_URL = (
    "postgresql+asyncpg://user:password@localhost:5432/flowforge_test"
)


@pytest_asyncio.fixture
async def db_session():

    engine = create_async_engine(
        TEST_DATABASE_URL,
        future=True,
    )

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with session_factory() as session:

        yield session

    await engine.dispose()