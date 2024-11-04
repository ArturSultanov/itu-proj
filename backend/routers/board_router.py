from fastapi import APIRouter

# from backend.utils.board_generator import generate_game_board

board_router = APIRouter(
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
