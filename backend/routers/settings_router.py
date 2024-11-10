from fastapi import APIRouter, status, HTTPException

from backend.config import Difficulty, set_difficulty, get_difficulty
from backend.database import cp_dependency, db_dependency
from backend.models import PlayerLoginDTO, DifficultyDTO, UpdateMessageDTO
from backend.utils import synchronize_player

settings_router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)

@settings_router.patch("/update_login", response_model=UpdateMessageDTO, status_code=status.HTTP_200_OK)
async def update_login(player: PlayerLoginDTO, cp: cp_dependency, db: db_dependency):
    cp.data.login = player.login  # Update the login of the current player
    await synchronize_player(cp.data, db)
    return UpdateMessageDTO(detail=f"Player login updated to {cp.data.login}")


@settings_router.patch("/set_difficulty", response_model=UpdateMessageDTO, status_code=status.HTTP_200_OK)
async def set_difficulty_route(data: DifficultyDTO):
    """
    Set the difficulty level
    """
    if data.difficulty not in Difficulty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid difficulty level."
        )

    set_difficulty(data.difficulty)
    return UpdateMessageDTO(detail=f"Difficulty set to {data.difficulty}")


@settings_router.get("/get_difficulty", response_model=DifficultyDTO, status_code=status.HTTP_200_OK)
async def get_difficulty_route():
    return {"difficulty": get_difficulty()}
