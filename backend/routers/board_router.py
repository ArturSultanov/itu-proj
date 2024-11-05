from fastapi import APIRouter, status, HTTPException
from typing import List, Optional, Annotated, Tuple
from backend.database import cp_dependency, db_dependency
from backend.schemas import GameUpdateDTO, SwapGemsDTO, GemBase, GemPositionDTO
from backend.utils import swap_gems, generate_game_board, click_gem, synchronize_player
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from backend.database import PlayerOrm, cp_dependency, db_dependency, create_tables, delete_tables, current_player, CurrentPlayer
from backend.schemas import PlayerDTO

# from backend.utils.board_generator import generate_game_board

board_router = APIRouter(
    prefix="/board",
    tags=["board"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)


@board_router.post("/swap_gems", response_model=GameUpdateDTO | None, status_code=status.HTTP_200_OK)
async def swap_gems_route(swap_data: SwapGemsDTO, cp: cp_dependency, db: db_dependency):
    """
    Check if there are any matches,
    then update the player score,
    and decrease the moves number.
    """

    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    # Get the current game status
    player_data = cp.data
    # Get updated game
    updated_game= swap_gems(player_data, swap_data)
    await synchronize_player(cp.data, db)
    return updated_game if updated_game is not None else None


@board_router.post("/click_gem", response_model=GameUpdateDTO | None, status_code=status.HTTP_200_OK)
async def click_gem_route(click: GemPositionDTO, cp: cp_dependency, db: db_dependency):
    """
    Check if clicked gem was a Bomb or Heal.
    If so, then update a game status.
    """

    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    # Get the current game status
    player_data = cp.data
    # Get updated game
    updated_game= click_gem(player_data, click)
    await synchronize_player(cp.data, db)
    return updated_game if updated_game is not None else None


@board_router.post("/shuffle", response_model=List[List[int]], status_code=status.HTTP_200_OK)
async def shuffle_board(cp: cp_dependency, db: db_dependency):
    new_board = generate_game_board()
    cp.data.last_game.board_status = new_board
    await synchronize_player(cp.data, db)
    return new_board
