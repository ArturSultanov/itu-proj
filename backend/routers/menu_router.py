
from backend.schemas import GameDTO, LeaderboardTDO

from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from sqlalchemy.future import select
from backend.database import PlayerOrm, cp_dependency, db_dependency, create_tables, delete_tables, current_player, CurrentPlayer
from backend.utils import generate_game_board


menu_router = APIRouter(
    prefix="/menu",
    tags=["menu"],
    responses={404: {"description": "Not Found"}},
)


# Assuming generate_game_board returns a numpy array
@menu_router.post("/new_game", response_model=GameDTO | None, status_code=status.HTTP_200_OK)
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
        board_status=new_board
    )
    # Update in-memory player
    cp.data.last_game = new_game
    return new_game


# Assuming generate_game_board returns a numpy array
@menu_router.post("/continue", response_model=GameDTO | None, status_code=status.HTTP_200_OK)
async def continue_game(cp: cp_dependency):
    """
    Create a new game for the current player, store it in the database, and return it.
    """
    # Check if the current player is loaded
    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=404, detail="Current player's last game not found.")

    return cp.data.last_game

@menu_router.post("/delete_continue", status_code=status.HTTP_200_OK)
async def delete_continue(cp: cp_dependency):
    if not cp or not cp.data:
        raise HTTPException(status_code=404, detail="Current player's last game not found.")

    cp.data.last_game = None


@menu_router.get("/leaderboard", response_model=List[LeaderboardTDO], status_code=status.HTTP_200_OK)
async def leaderboard(db: db_dependency):
    """
    Get the top 5 players based on highest_score, sorted in descending order.
    """
    # Запрос на выборку 5 лучших игроков по убыванию highest_score
    result = await db.execute(
        select(PlayerOrm.login, PlayerOrm.highest_score)
        .order_by(PlayerOrm.highest_score.desc())
        .limit(5)
    )

    # Получаем результаты в виде списка словарей
    top_players = [{"login": row[0], "highest_score": row[1]} for row in result.all()]

    return top_players
