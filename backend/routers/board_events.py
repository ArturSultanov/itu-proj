from fastapi import APIRouter
from ..database.models import Gem, GameState, BoardState
# from backend.utils.board_generator import generate_game_board

game_router = APIRouter(
    prefix="/board",
    tags=["board"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)



# Swap two gems on the board
def swap_gems():
    pass

def use_bomb():
    pass

def use_heal():
    pass
