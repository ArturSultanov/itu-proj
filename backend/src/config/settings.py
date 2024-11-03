from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./game.db"  # Full URL with async support
    WEB_HOST: str = "127.0.0.1"
    WEB_PORT: int = 8000
    SQL_ALCHEMY_DEBUG: bool = False
    GAME_DIFFICULTY: str = "normal"  # Difficulty level: 'easy', 'normal', 'hard'

    class Config:
        env_file = ".env"

settings = Settings()