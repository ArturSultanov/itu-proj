# backend/src/routers/player_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from database.models import PlayerOrm
from database.database import db_dependency
from schemas.schemas import PlayerResponse
from typing import Dict

# In-memory cache to store player instances
player_cache: Dict[str, PlayerOrm] = {}

player_router = APIRouter(
    prefix="/player",
    tags=["player"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)

@player_router.get("/{login}", response_model=PlayerResponse)
async def get_or_create_player(login: str, db: AsyncSession = Depends(db_dependency)):
    """
    Get player by login. If the player does not exist, create a new player and return it.
    Cache the player instance in memory after the first retrieval.
    """
    # Check if the player is already cached
    if login in player_cache:
        return player_cache[login]  # Return the cached player

    # Query the database if the player is not cached
    result = await db.execute(
        select(PlayerOrm).where(PlayerOrm.login == login).options(selectinload(PlayerOrm.games))
    )
    player = result.scalars().first()

    if player:
        # Cache the player instance and return it
        player_cache[login] = player
        return player

    # If the player is not found, create a new one
    new_player = PlayerOrm(login=login, highest_score=0)
    db.add(new_player)
    try:
        await db.commit()
        await db.refresh(new_player)
        # Cache the newly created player
        player_cache[login] = new_player
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create new player due to a database error.")

    return new_player  # Return the newly created player
