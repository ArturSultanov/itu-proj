from enum import Enum

from pydantic_settings import BaseSettings

class Difficulty(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./database/game.db"  # Full URL with async support
    WEB_HOST: str = "127.0.0.1"
    WEB_PORT: int = 8000
    SQL_ALCHEMY_DEBUG: bool = True
    GAME_DIFFICULTY: Difficulty = Difficulty.NORMAL

    class Config:
        env_file = ".env"

settings = Settings()
