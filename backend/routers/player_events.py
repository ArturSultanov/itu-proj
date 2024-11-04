from typing import Optional, Union

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from starlette import status

from backend.database import current_player, cp_dependency
from backend.database import db_dependency
from backend.database import PlayerOrm
from backend.schemas import PlayerDTO, PlayerLoginDTO

player_router = APIRouter(
    prefix="/player",
    tags=["player"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)

@player_router.post("/", status_code=status.HTTP_200_OK, response_model=PlayerDTO | None)
async def get_or_create_player(player: PlayerLoginDTO, db: db_dependency):
    """
    Get player by login. If the player does not exist, create a new player and return it.
    Cache the player instance in memory after the first retrieval.
    """

    login = player.login  # Extract the login from PlayerAddDTO

    # Query the database if the player is not cached
    result = await db.execute(
        select(PlayerOrm).where(PlayerOrm.login == login)
    )
    player_result = result.scalars().first()

    if player_result:
        player_dto = PlayerDTO.model_validate(player_result)
        return player_dto

    # If the player is not found, create a new one
    new_player = PlayerOrm(login=login, highest_score=0)
    db.add(new_player)
    try:
        await db.commit()
        await db.refresh(new_player)

        result = await db.execute(
            select(PlayerOrm).where(PlayerOrm.login == login)
        )
        player_result = result.scalars().first()

        if not player_result:
            raise HTTPException(status_code=500, detail="Failed to load the new player after commit.")

        player_dto = PlayerDTO.model_validate(player_result)
        current_player.load_player(player_dto)
        return new_player
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create new player due to a database error.")


@player_router.post("/update_login/", status_code=status.HTTP_200_OK)
async def get_or_create_player(player: PlayerLoginDTO, cp: cp_dependency):
    cp.data.login = player.login  # Update the login of the current player
    return {"msg": f"Player login updated to {cp.data.login}"}


# @player_router.post("/sync", status_code=status.HTTP_200_OK)
# async def get_or_create_player(cp: cp_dependency, db: db_dependency):
#     data = cp.data
#
#     login = data.login
#
#     result = await db.execute(
#         select(PlayerOrm).where(PlayerOrm.login == login)
#     )
#     player_result = result.scalars().first()
#     if not player_result:
#         raise HTTPException(status_code=500, detail="Failed to load the player for sync.")

    # return {"msg": f"Player login updated to {cp.data.login}"}


@player_router.post("/sync", status_code=status.HTTP_200_OK)
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




@player_router.get("/current_player", status_code=status.HTTP_200_OK, response_model=Optional[PlayerDTO])
async def get_current_player():
    """
    Retrieve the currently loaded player from memory.
    """
    if current_player.data is None:
        raise HTTPException(status_code=404, detail="No current player is loaded.")
    return current_player.data


# @player_router.get("/all", status_code=status.HTTP_200_OK, response_model=list[PlayerDTO])
# async def get_all_players(db: db_dependency):
#     """
#     Retrieve all players from the database with their associated games.
#     """
#     result = await db.execute(
#         select(PlayerOrm).options(selectinload(PlayerOrm.last_game))
#     )
#     players = result.scalars().all()
#     return players