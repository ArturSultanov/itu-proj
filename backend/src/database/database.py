from typing import Annotated as typingAnnotated, Generator
from fastapi import Depends
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from config.settings import settings
from src.database.models import Player

import asyncio
from typing import Annotated

from sqlalchemy import String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings


# Type aliases for convenience
Str256 = typingAnnotated[str, String(256)]
Str2048 = typingAnnotated[str, String(2048)]

class Base(DeclarativeBase):
    type_annotation_map = {
        Str256: String(256),
        Str2048: String(2048)
    }


async_engine = create_async_engine(
    url=settings.database_url,
    echo=settings.SQL_ALCHEMY_DEBUG
)

session_factory = async_sessionmaker(bind=async_engine)


def get_db_session() -> Generator[Session, None, None]:
    """
    Generator to get a session from the session factory
    """
    db = session_factory()  # Creates a new session
    try:
        yield db  # Yields the session for use in the calling context
    finally:
        db.close()  # Ensures the session is closed after use


db_dependency = typingAnnotated[Session, Depends(get_db_session)]

async def create_tables():
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-core
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

