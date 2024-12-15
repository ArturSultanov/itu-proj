from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

# Type aliases for convenience
Str256 = Annotated[str, String(256)]


class Base(DeclarativeBase):
    type_annotation_map = {Str256: String(256)}


# Create the async engine with debug echo set based on settings
async_engine = create_async_engine(settings.DATABASE_URL, echo=settings.SQL_ALCHEMY_DEBUG)

# Session factory for creating async sessions
session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for request handling."""
    async with session_factory() as session:
        yield session

# Dependency for FastAPI route injection
db_dependency = Annotated[AsyncSession, Depends(get_db_session)]


async def create_tables():
    """Create database tables based on the defined models."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
