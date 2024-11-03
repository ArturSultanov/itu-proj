from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.types import JSON
from .database import Base, Str256, Str2048
from typing import List, Annotated
import datetime
import json

intpk = Annotated[int, mapped_column(primary_key=True, index=True)]

class PlayerOrm(Base):
    """
    Table for storing information about players.
    Each row represents a single player with their associated information.

    columns:
        id (int): Unique identifier for the player.
        login (str): The login name of the player.
        higest_score (int): The highest score achieved by the player.
        current_game (int): The id of current game.
    """
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)  # Unique player ID
    login: Mapped[Str256] = mapped_column(unique=True, nullable=False)  # Player's login name
    highest_score: Mapped[int] = mapped_column(default=0, nullable=False)  # Highest score achieved by the player
    current_game: Mapped[int | None] = mapped_column(ForeignKey('games.id'), nullable=True)  # Current game ID (nullable)

    # Relationship with the Game table
    games: Mapped[List["GameOrm"]] = relationship('GameOrm', back_populates='player', order_by="GameOrm.created_at.desc()",)

class GameOrm(Base):
    """
    Table for storing information about games.
    Each row represents a single game with its associated state and metadata.
    """
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)  # Unique game ID
    current_score: Mapped[int] = mapped_column(default=0, nullable=False)  # Current score in the game
    moves_left: Mapped[int] = mapped_column(default=0, nullable=False)  # Remaining moves in the game
    board_status: Mapped[Str2048] = mapped_column(JSON, nullable=False)  # Game board status stored as JSON
    created_at: Mapped[datetime.datetime] = mapped_column(datetime.datetime, server_default=text("CURRENT_TIMESTAMP AT TIME ZONE 'UTC'"), nullable=False)  # Timestamp for game creation
    gamer_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))  # Associated player ID

    # Relationship with the Player table
    player: Mapped["PlayerOrm"] = relationship('PlayerOrm', back_populates='games')

    def set_board_status(self, board_state: List[List[int]]):
        """Set the board status as a JSON-encoded string."""
        self.board_status = json.dumps(board_state)

    def get_board_status(self) -> List[List[int]]:
        """Get the board status as a Python list."""
        return json.loads(self.board_status)
