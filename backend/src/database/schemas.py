from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# Определение перечисления статусов игры
class GameStatusEnum(Enum):
    IN_GAME = "in_game"
    OUT_GAME = "out_game"
    PAUSED = "paused"

# Определение перечисления типов драгоценных камней
class Gem(Enum):
    GEM1 = 0
    GEM2 = 1
    GEM3 = 2
    GEM4 = 3
    BOMB = 4
    HEART = 5

# Модель состояния игрового поля
class BoardState(BaseModel):
    board_state: List[List[Gem]]

# Схема для модели игрока
class PlayerBase(BaseModel):
    login: str
    highest_score: int

class PlayerCreate(PlayerBase):
    pass

class PlayerResponse(PlayerBase):
    id: int
    current_game: Optional[int]

    class Config:
        orm_mode = True

# Схема для модели игры
class GameBase(BaseModel):
    current_score: int
    moves_left: int
    board_status: BoardState

class GameCreate(GameBase):
    gamer_id: int

class GameResponse(GameBase):
    id: int
    gamer_id: int

    class Config:
        orm_mode = True
