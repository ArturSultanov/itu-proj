from typing import List, Optional, Annotated, Tuple, Set
from pydantic import BaseModel, ConfigDict, StringConstraints, NonNegativeInt, conlist, conset


class GemPosition(BaseModel):
    x: int
    y: int

class GemBase(GemPosition):
    type: int

class SwapGemsInDTO(BaseModel):
    gems: conlist(GemPosition, min_length=2, max_length=2)

class GameBase(BaseModel):
    current_score: int
    moves_left: int

class GameBoardUpdateDTO(GameBase):
    updated_gems: Set[GemBase]

class GameDTO(GameBase):
    model_config = ConfigDict(from_attributes=True)
    board_status: List[List[int]]

class LeaderboardTDO(BaseModel):
    login: str
    highest_score: int

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
