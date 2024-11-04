__all__ = [
    "player_router", "board_router", "game_router"
]

from .player_login import player_router
from .board_events import board_router
from .game_events import game_router