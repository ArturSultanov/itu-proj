from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.database import PlayerOrm
from backend.schemas import PlayerDTO


async def synchronize_player(player_data: PlayerDTO, db: AsyncSession):
    """
    Синхронизирует данные игрока из `player_data` с базой данных.

    Parameters:
        player_data (PlayerDTO): Текущие данные игрока.
        db (AsyncSession): Сессия базы данных.
    """
    player_id = player_data.id

    # Поиск игрока в базе данных по ID
    result = await db.execute(select(PlayerOrm).where(PlayerOrm.id == player_id))
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
