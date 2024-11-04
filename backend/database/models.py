import datetime
from typing import Annotated, Optional, List, Dict

from sqlalchemy import ForeignKey, text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base, Str256

intpk = Annotated[int, mapped_column(primary_key=True, index=True)]

class PlayerOrm(Base):
    """
    Table for storing information about players.
    Each row represents a single player with their associated information.
    """
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)  # Unique player ID
    login: Mapped[Str256] = mapped_column(unique=True, nullable=False)  # Player's login name
    highest_score: Mapped[int] = mapped_column(default=0, nullable=False)  # Highest score achieved by the player
    last_game: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True)  # Last game details stored as JSON
