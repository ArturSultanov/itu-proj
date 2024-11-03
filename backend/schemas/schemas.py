from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import datetime

# Enum for types of gems
class Gem(Enum):
    GEM1 = 0
    GEM2 = 1
    GEM3 = 2
    GEM4 = 3
    BOMB = 4
    HEART = 5

# Schema for board state
class BoardState(BaseModel):
    board_state: List[List[Gem]]  # Matrix representing the game board

# Schema for game data transfer object
class GameDTO(BaseModel):
    id: int
    current_score: int
    moves_left: int
    board_status: BoardState
    created_at: datetime.datetime
    gamer_id: int  # Should be an int, representing the foreign key to PlayerOrm

    class Config:
        from_attributes = True

# Schema for adding a new player
class PlayerAddDTO(BaseModel):
    login: str

# Schema for player data transfer object
class PlayerDTO(PlayerAddDTO):
    id: int
    highest_score: int
    games: Optional[List[GameDTO]]  # Optional list of games associated with the player

    class Config:
        from_attributes = True
