from datetime import datetime

from fastapi import APIRouter, status

from backend.database import db_dependency
from backend.schemas import GameDTO
from fastapi import APIRouter, status

from backend.database import db_dependency
from backend.schemas import GameDTO

from typing import Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from starlette import status

from backend.database import PlayerOrm, cp_dependency, db_dependency, create_tables, delete_tables, current_player, CurrentPlayer
from backend.schemas import PlayerDTO
from backend.utils import generate_game_board


"""
NEW GAME
CONTINUE
LEADERBOARD
"""
menu_router = APIRouter(
    prefix="/menu",
    tags=["menu"],
    responses={404: {"description": "Not Found"}},
)


# Assuming generate_game_board returns a numpy array
@menu_router.post("/new_game", response_model=GameDTO | None, status_code=status.HTTP_201_CREATED)
async def create_new_game(cp: cp_dependency):
    """
    Create a new game for the current player, store it in the database, and return it.
    """
    # Check if the current player is loaded
    if not cp or not cp.data:
        raise HTTPException(status_code=400, detail="Current player not found.")

    # Generate a new game board
    new_board = generate_game_board()

    # Create a new game instance
    new_game = GameDTO(
        current_score=0,
        moves_left=30,  # Set an initial value for moves_left
        board_status=new_board,
        created_at=datetime.now()
    )

    cp.data.last_game = new_game

    return new_game