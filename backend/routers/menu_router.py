
from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from backend.config import get_start_moves
from backend.database import PlayerOrm, cp_dependency, db_dependency
from backend.schemas import GameDTO, LeaderboardTDO
from backend.utils import generate_game_board, synchronize_player

menu_router = APIRouter(
    prefix="/menu",
    tags=["menu"],
    responses={404: {"description": "Not Found"}},
)


# Assuming generate_game_board returns a numpy array
@menu_router.get("/new_game", response_model=GameDTO | None, status_code=status.HTTP_200_OK)
async def create_new_game(cp: cp_dependency, db: db_dependency):
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
        moves_left=get_start_moves(),  # Set an initial value for moves_left
        board_status=new_board
    )
    # Update in-memory player
    cp.data.last_game = new_game
    await synchronize_player(cp.data, db)
    return new_game


# Assuming generate_game_board returns a numpy array
@menu_router.get("/continue", response_model=GameDTO | None, status_code=status.HTTP_200_OK)
async def continue_game(cp: cp_dependency):
    """
    Create a new game for the current player, store it in the database, and return it.
    """
    # Check if the current player is loaded
    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=404, detail="Current player's last game not found.")

    return cp.data.last_game


@menu_router.delete("/delete_game", status_code=status.HTTP_200_OK)
async def delete_continue(cp: cp_dependency, db: db_dependency):
    if not cp or not cp.data:
        raise HTTPException(status_code=404, detail="Current player's last game not found.")

    cp.data.last_game = None
    await synchronize_player(cp.data, db)
    return {"message": "Game deleted"}


@menu_router.get("/leaderboard", response_model=List[LeaderboardTDO], status_code=status.HTTP_200_OK)
async def leaderboard(limit: int, db: db_dependency):
    """
    Get the top 5 players based on highest_score, sorted in descending order.
    """
    result = await db.execute(
        select(PlayerOrm.login, PlayerOrm.highest_score)
        .order_by(PlayerOrm.highest_score.desc())
        .limit(limit)
    )

    top_players = [{"login": row[0], "highest_score": row[1]} for row in result.all()]

    return top_players
