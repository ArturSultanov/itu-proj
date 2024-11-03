from typing import Annotated as typingAnnotated
from fastapi import Depends
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from config.settings import settings
from src.database.models import Player

engine = create_engine(
    url=settings.database_url,
    echo=settings.SQL_ALCHEMY_DEBUG,
    pool_size=10,
    max_overflow=10
)

Str256 = typingAnnotated[str, String(256)]

Str2048 = typingAnnotated[str, String(2048)]

class Base(DeclarativeBase):
    type_annotation_map = {
        Str256: String(256),
        Str2048: String(2048)
    }

class DBSession:
    def __init__(self) -> None:
        self.session_factory = sessionmaker(bind=engine)
    
    def update_player_login(player_id: int, new_login: Str256):
        with self.session_factory() as session:
            player = session.get(Player, player_id)
            player.login = new_login
            session.refresh(player)
            session.commit()
