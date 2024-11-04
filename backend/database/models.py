import datetime
from typing import Annotated, Optional, List

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

    # Relationship with the Game table
    last_game: Mapped[Optional["GameOrm"]] = relationship('GameOrm', back_populates='player')

class GameOrm(Base):
    """
    Table for storing information about games.
    Each row represents a single game with its associated state and metadata.
    """
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)  # Unique game ID
    current_score: Mapped[int] = mapped_column(default=0, nullable=False)  # Current score in the game
    moves_left: Mapped[int] = mapped_column(default=0, nullable=False)  # Remaining moves in the game
    board_status: Mapped[List[List[int]]] = mapped_column(JSON, nullable=False)  # Game board status stored as JSON
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), unique=True)

    # Relationship with the Player table
    player: Mapped["PlayerOrm"] = relationship('PlayerOrm', back_populates='last_game')

