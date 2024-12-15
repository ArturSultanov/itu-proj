from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import PlayerOrm
from models import PlayerDTO


async def synchronize_player(player_data: PlayerDTO, db: AsyncSession):
    """
    Synchronized data from in-memory `player_data` with database `db`.

    Parameters:
        player_data (PlayerDTO): Current player data.
        db (AsyncSession): Database session.
    """
    player_id = player_data.id

    result = await db.execute(select(PlayerOrm).where(PlayerOrm.id == player_id))
    player_result = result.scalars().first()

    if not player_result:
        raise HTTPException(status_code=404, detail="Player not found for synchronization.")

    if player_data.login:
        player_result.login = player_data.login
    else:
        raise HTTPException(status_code=500, detail="Player login not found for synchronization.")

    player_result.highest_score = player_data.highest_score if player_data.highest_score is not None else 0
    player_result.last_game = player_data.last_game.model_dump() if player_data.last_game else None

    db.add(player_result)

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to synchronize player data: {str(e)}")
