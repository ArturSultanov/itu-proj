from enum import Enum
import os
from pydantic_settings import BaseSettings


class Difficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    DEBUG = -1


HEART_RECOVERY_MOVES = {
    Difficulty.EASY: 20,
    Difficulty.NORMAL: 10,
    Difficulty.HARD: 5,
    Difficulty.DEBUG: 100,
}


START_MOVES = {
    Difficulty.EASY: 30,
    Difficulty.NORMAL: 25,
    Difficulty.HARD: 20,
    Difficulty.DEBUG: 100,
}


class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite+aiosqlite:///{os.path.abspath('./backend/database/game.db')}"
    WEB_HOST: str = "127.0.0.1"
    WEB_PORT: int = 8000
    SQL_ALCHEMY_DEBUG: bool = True
    GAME_DIFFICULTY: Difficulty = Difficulty.NORMAL

    class Config:
        env_file = ".env"


settings = Settings()


def get_heart_recovery_moves() -> int:
    return HEART_RECOVERY_MOVES[settings.GAME_DIFFICULTY]


def get_start_moves() -> int:
    return START_MOVES[settings.GAME_DIFFICULTY]


def set_difficulty(difficulty: Difficulty):
    settings.GAME_DIFFICULTY = difficulty


def get_difficulty() -> Difficulty:
    return settings.GAME_DIFFICULTY
