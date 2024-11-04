import datetime
from enum import Enum
from typing import List, Optional, Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints, NonNegativeInt


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
    model_config = ConfigDict(from_attributes=True)
    id: NonNegativeInt
    current_score: NonNegativeInt
    moves_left: NonNegativeInt
    board_status: List[List[int]]
    created_at: datetime.datetime
    player_id: NonNegativeInt  # Should be an int, representing the foreign key to PlayerOrm
    player: NonNegativeInt

# Schema for adding a new player
class PlayerLoginDTO(BaseModel):
    """
        Attributes:
            login: Annotated[str, StringConstraints(max_length=256)]
    """
    model_config = ConfigDict(from_attributes=True)
    login: Annotated[str, StringConstraints(max_length=256)]

# Schema for player data transfer object
class PlayerDTO(PlayerLoginDTO):
    """
    Attributes:
        login: Annotated[str, StringConstraints(max_length=256)]
        id: NonNegativeInt
        highest_score: NonNegativeInt
        last_game: Optional[GameDTO]
    """
    id: Optional[NonNegativeInt]
    highest_score: Optional[NonNegativeInt]
    last_game: Optional[GameDTO]  # Optional list of games associated with the player
