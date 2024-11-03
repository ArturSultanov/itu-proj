from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from database.models import GameOrm, PlayerOrm
from database.database import db_dependency
from schemas.schemas import GameDTO, BoardState
from utils.board import generate_game_board
from config.state_manager import current_player

# Create a new router for game logic
game_router = APIRouter(
    prefix="/game",
    tags=["game"],
    responses={404: {"description": "Not Found"}},
)

@game_router.post("/new", response_model=GameDTO, status_code=status.HTTP_201_CREATED)
async def create_new_game(db: db_dependency):
    """
    Create a new game for the current player, store it in the database, and return it.
    """
    # Ensure a current player is loaded
    if not current_player or not current_player.is_loaded():
        raise HTTPException(status_code=400, detail="No current player is loaded.")

    player_id = current_player.data.id

    # Generate a new game board
    new_board = generate_game_board()

    # Create a new game instance
    new_game = GameOrm(
        current_score=0,
        moves_left=30,  # Initial number of moves (adjust as needed)
        board_status=new_board,
        created_at=datetime.now(timezone.utc),
        gamer_id=player_id,
    )
    # new_game.set_board_status(new_board)

    # Add the new game to the database
    db.add(new_game)
    try:
        await db.commit()
        await db.refresh(new_game)  # Refresh to get the ID and other database-generated fields

        # Convert the game to GameDTO
        game_dto = GameDTO.model_validate(new_game)
        return game_dto
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create new game due to a database error.")
