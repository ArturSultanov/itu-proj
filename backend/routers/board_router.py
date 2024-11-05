from fastapi import APIRouter, status, HTTPException
from typing import List, Optional, Annotated, Tuple
from backend.database import cp_dependency, db_dependency
from backend.schemas import GameBoardUpdateDTO, SwapGemsInDTO, GemBase
from backend.utils import swap_gems, generate_game_board
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from backend.database import PlayerOrm, cp_dependency, db_dependency, create_tables, delete_tables, current_player, CurrentPlayer
from backend.schemas import PlayerDTO

# from backend.utils.board_generator import generate_game_board

board_router = APIRouter(
    prefix="/board",
    tags=["board"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)


@board_router.post("/swap_gems", response_model=GameBoardUpdateDTO | None, status_code=status.HTTP_200_OK)
async def swap_gems_route(swap_data: SwapGemsInDTO, cp: cp_dependency, db: db_dependency):
    """
    Check if there are any matches,
    then update the player score,
    and decrease the moves number.
    """
    # Проверяем, что данные игрока загружены
    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    board = cp.data.last_game.board_status

    # Извлекаем позиции из DTO и преобразуем в формат ((x1, y1), (x2, y2))
    pos1 = (swap_data.gems[0].x, swap_data.gems[0].y)
    pos2 = (swap_data.gems[1].x, swap_data.gems[1].y)

    # Вызываем функцию swap_gems для обмена и поиска совпадений
    updated_gem_set, matches_number = swap_gems(board, pos1, pos2)

    if updated_gem_set and matches_number != 0:
        # Обновляем счёт и количество оставшихся ходов
        cp.data.last_game.current_score += matches_number * 10
        cp.data.last_game.moves_left -= 1

        # Обновление highest_score, если current_score превышает текущее значение highest_score
        if cp.data.last_game.current_score > (cp.data.highest_score or 0):
            cp.data.highest_score = int(cp.data.last_game.current_score)

        updated_gems = {GemBase(x=x, y=y, type=gem_type) for x, y, gem_type in updated_gem_set}

        # Возвращаем обновлённые данные в виде BoardUpdateDTO
        return GameBoardUpdateDTO(
            current_score=cp.data.last_game.current_score,
            moves_left=cp.data.last_game.moves_left,
            updated_gem=updated_gems
        )

    return None

@board_router.post("/shuffle", response_model=List[List[int]], status_code=status.HTTP_200_OK)
async def shuffle_board(cp: cp_dependency):
    new_board = generate_game_board()
    cp.data.last_game.board_status = new_board
    return new_board


def use_bomb():
    # TODO
    pass

def use_heal():
    # TODO
    pass
