from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from backend.database import PlayerOrm
from backend.database import current_player
from backend.database import db_dependency
from backend.schemas import PlayerDTO, PlayerLoginDTO

login_router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)


@login_router.post("", status_code=status.HTTP_200_OK, response_model=PlayerDTO | None)
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
        current_player.load_player(player_dto)
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
