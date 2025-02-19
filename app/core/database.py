from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


async_engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

async def aget_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
