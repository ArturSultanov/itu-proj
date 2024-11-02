from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_PATH: str = "sqlite:///./game.db"  # Путь к базе данных SQLite
    WEB_HOST: str = "127.0.0.1"
    WEB_PORT: int = 8000
    SQL_ALCHEMY_DEBUG: bool = False
    GAME_DIFFICULTY: str = "normal"  # Уровень сложности: 'easy', 'normal', 'hard'


    @property
    def database_url(self) -> str:
        return self.DB_PATH

    class Config:
        env_file = ".env"

# Создание экземпляра настроек
settings = Settings()
