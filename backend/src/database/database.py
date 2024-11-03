from typing import Annotated as typingAnnotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


# Type aliases for convenience
Str256 = typingAnnotated[str, String(256)]
Str2048 = typingAnnotated[str, String(2048)]

class Base(DeclarativeBase):
    type_annotation_map = {
        Str256: String(256),
        Str2048: String(2048)
    }

async_engine = create_async_engine(settings.database_url)

session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session

db_dependency = typingAnnotated[AsyncSession, Depends(get_db_session)]

async def create_tables():
    # Schema creation with async engine
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
