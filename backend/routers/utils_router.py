from typing import Optional

from fastapi import APIRouter, HTTPException, status

from backend.database import cp_dependency, db_dependency, create_tables, delete_tables, current_player
from backend.models import PlayerDTO, UpdateMessageDTO
from backend.utils import synchronize_player

utils_router = APIRouter(
    prefix="/utils",
    tags=["utils"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)


@utils_router.get("/reboot_db", response_model=UpdateMessageDTO, status_code=status.HTTP_200_OK)
async def reboot_db():
    await delete_tables()
    await create_tables()
    return UpdateMessageDTO(detail="Database rebooted.")


@utils_router.post("/sync", response_model=UpdateMessageDTO, status_code=status.HTTP_200_OK)
async def sync_player(cp: cp_dependency, db: db_dependency):
    if not cp.data:
        raise HTTPException(status_code=500, detail="No player data found in current player instance.")

    await synchronize_player(cp.data, db)
    return UpdateMessageDTO(detail="Player data synchronized successfully")


@utils_router.get("/current_player", status_code=status.HTTP_200_OK, response_model=Optional[PlayerDTO])
async def get_current_player(cp: cp_dependency):
    """
    Retrieve the currently loaded player from memory.
    """
    return cp.data


@utils_router.post("/exit", status_code=status.HTTP_200_OK)
async def exit_app(db: db_dependency):
    if current_player and current_player.data:
        await synchronize_player(current_player.data, db)
        current_player.data = None

        return UpdateMessageDTO(detail="Player data synchronized and current player cleared.")
    else:
        return UpdateMessageDTO(detail="No current player to synchronize. Current player cleared.")
