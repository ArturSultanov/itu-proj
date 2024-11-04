from enum import Enum
from typing import Optional, Dict, Tuple

from pydantic_settings import BaseSettings
from backend.schemas import PlayerDTO, Gem

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

class CurrentPlayer:
    def __init__(self):
        self.data: Optional[PlayerDTO] = None  # Stores the current player's data

    def load_player(self, player_data: PlayerDTO):
        """Load the player data into the current player instance."""
        self.data = player_data

    def is_loaded(self) -> bool:
        """Check if the current player data is loaded."""
        return self.data is not None

    def update_board(self, new_gems: Dict[Tuple[int, int], Gem]):
        """Update the current player's game board with new gems."""
        if not self.is_loaded() or not self.data.games:
            raise ValueError("No current game data available.")

        current_game = self.data.games[0]  # Assuming only one active game at a time
        board = current_game.board_status.board_state  # Access the board state

        for (row, col), gem in new_gems.items():
            board[row][col] = gem

        # Update the modified board in the current player data
        current_game.board_status.board_state = board

    def sync_with_database(self, db_session):
        """Sync the current player data with the database."""
        if not self.is_loaded():
            raise ValueError("No current player data to sync.")

        # Convert PlayerDTO to the ORM model and save to the database
        # Example: Logic to update PlayerOrm using `db_session`
        # TODO
        pass

# Create a singleton-like instance of CurrentPlayer
current_player = CurrentPlayer()
