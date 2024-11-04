from fastapi import APIRouter, status
from typing import List, Optional, Annotated, Tuple
from backend.database import cp_dependency
from backend.schemas import BoardUpdateDTO

# from backend.utils.board_generator import generate_game_board

board_router = APIRouter(
    prefix="/board",
    tags=["board"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)



@board_router.post("/swap_gems", response_model=BoardUpdateDTO | None, status_code=status.HTTP_200_OK)
async def swap_gems(gems: Tuple[Tuple[int, int], Tuple[int, int]],cp: cp_dependency):
    board = cp.data.last_game.board_status




def use_bomb():
    pass

def use_heal():
    pass
