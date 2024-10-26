from pydantic import BaseModel
from typing import List
from enum import Enum

class GameState(Enum):
    IN_GAME = "in_game"
    OUT_GAME = "out_game"
    PAUSED = "paused"

class Gem(Enum):
    GEM1 = 0
    GEM2 = 1
    GEM3 = 2
    GEM4 = 3
    BOMB = 4
    HEART = 5

# Модель для состояния игрового поля
class BoardState(BaseModel):
    board_state: List[List[Gem]]  # Матрица, представляющая игровое поле

# Основная модель для описания состояния игры пользователя
class GameState(BaseModel):
    user_id: str  # Уникальный идентификатор пользователя
    current_state: GameState  # Текущее состояние игры (например, "in_game", "paused")
    highest_score: int  # Рекордный счет
    current_level: int  # Текущий уровень
    score: int  # Текущий счет
    moves_left: int  # Количество оставшихся ходов
    board_state: BoardState  # Состояние игрового поля (двумерный массив)

# Пример данных, которые можно валидировать через Pydantic
game_data = {
    "user_id": "Artur",
    "current_state": "in_game",
    "highest_score": 2700,
    "current_level": 3,
    "score": 2500,
    "moves_left": 15,
    "board_state": [
        [1, 2, 3, 4, 1, 0],
        [3, 2, 1, 4, 3, 0],
        [3, 2, 1, 4, 3, 0],
        [3, 2, 1, 4, 3, 0],
        [3, 2, 1, 4, 3, 0],
        [3, 2, 1, 4, 3, 0]
    ]
}

# Создание экземпляра модели и валидация данных
game_state = GameState(**game_data)
print(game_state)
