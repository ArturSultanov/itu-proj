from typing import Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from starlette import status

from backend.database import PlayerOrm, cp_dependency, db_dependency, create_tables, delete_tables, current_player, CurrentPlayer
from backend.schemas import PlayerDTO


utils_router = APIRouter(
    prefix="/utils",
    tags=["utils"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)

@utils_router.get("/reboot_db")
async def reboot_db():
    await delete_tables()
    await create_tables()
    return {"detail": "Database rebooted."}


@utils_router.post("/sync", status_code=status.HTTP_200_OK)
async def sync_player(cp: cp_dependency, db: db_dependency):
    # Проверка, что cp.data содержит данные игрока
    if not cp.data:
        raise HTTPException(status_code=500, detail="No player data found in current player instance.")

    player_data = cp.data
    player_id = player_data.id

    # Поиск игрока в базе данных по ID
    result = await db.execute(
        select(PlayerOrm).where(PlayerOrm.id == player_id)
    )
    player_result = result.scalars().first()

    if not player_result:
        raise HTTPException(status_code=404, detail="Player not found for synchronization.")

    # Обновление полей игрока, исключая `id`
    if player_data.login:
        player_result.login = player_data.login
    else:
        raise HTTPException(status_code=500, detail="Player login not found for synchronization.")

    player_result.highest_score = player_data.highest_score if player_data.highest_score is not None else 0
    player_result.last_game = player_data.last_game.dict() if player_data.last_game else {}

    db.add(player_result)

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to synchronize player data: {str(e)}")

    return {"detail": "Player data synchronized successfully."}


@utils_router.get("/current_player", status_code=status.HTTP_200_OK, response_model=Optional[PlayerDTO])
async def get_current_player(cp: cp_dependency):
    """
    Retrieve the currently loaded player from memory.
    """
    return cp.data


@utils_router.post("/exit", status_code=status.HTTP_200_OK)
async def exit_app(db: db_dependency):
    # Проверка, есть ли данные текущего игрока перед синхронизацией
    if current_player and current_player.data:
        # Синхронизация данных игрока с базой данных
        await sync_player(current_player, db)
        # Очистка текущего игрока
        current_player.data = None  # Очищаем данные игрока, чтобы сбросить текущего пользователя
        return {"detail": "Player data synchronized and current player cleared."}
    else:
        return {"detail": "No current player to synchronize. Current player cleared."}




