from typing import List, Optional, Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints, NonNegativeInt, conlist, conint

from backend.config import Difficulty


class DifficultyDTO(BaseModel):
    difficulty: Difficulty


class GemPositionDTO(BaseModel):
    x: int
    y: int


class GemBase(GemPositionDTO):
    type: int


class SwapGemsDTO(BaseModel):
    gems: conlist(GemPositionDTO, min_length=2, max_length=2)


class GameBase(BaseModel):
    current_score: int
    moves_left: int


class GameUpdateDTO(GameBase):
    updated_gems: List[GemBase]


class BordStatusDTO(BaseModel):
    board_status: List[List[Annotated[int, conint(ge=0, le=5)]]]


class GameDTO(GameBase):
    model_config = ConfigDict(from_attributes=True)
    board_status: List[List[Annotated[int, conint(ge=0, le=5)]]]


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
