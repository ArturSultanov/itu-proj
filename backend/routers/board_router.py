from fastapi import APIRouter, status, HTTPException
from typing import List, Optional, Annotated, Tuple
from backend.database import cp_dependency, db_dependency
from backend.schemas import GameUpdateDTO, SwapGemsDTO, GemBase, GemPositionDTO
from backend.utils import swap_gems, generate_game_board, click_gem
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


@board_router.post("/swap_gems", response_model=GameUpdateDTO | None, status_code=status.HTTP_200_OK)
async def swap_gems_route(swap_data: SwapGemsDTO, cp: cp_dependency, db: db_dependency):
    """
    Check if there are any matches,
    then update the player score,
    and decrease the moves number.
    """
    # Проверяем, что данные игрока загружены
    # if not cp or not cp.data or not cp.data.last_game:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")
    #
    # board = cp.data.last_game.board_status
    #
    # # Вызываем функцию swap_gems для обмена и поиска совпадений
    # updated_gems, matches_number = swap_gems(board,
    #                                             (swap_data.gems[0].x, swap_data.gems[0].y),
    #                                             (swap_data.gems[1].x, swap_data.gems[1].y)
    #                                             )
    #
    # if updated_gems:
    #     # Обновляем счёт и количество оставшихся ходов
    #     cp.data.last_game.current_score += matches_number * 10
    #     cp.data.last_game.moves_left -= 1
    #
    #     # Обновление highest_score, если current_score превышает текущее значение highest_score
    #     if cp.data.last_game.current_score > (cp.data.highest_score or 0):
    #         cp.data.highest_score = int(cp.data.last_game.current_score)
    #
    #     # updated_gems = {GemBase(x=x, y=y, type=gem_type) for x, y, gem_type in updated_gem_set}
    #
    #     # Возвращаем обновлённые данные в виде BoardUpdateDTO
    #     return GameUpdateDTO(
    #         current_score=cp.data.last_game.current_score,
    #         moves_left=cp.data.last_game.moves_left,
    #         updated_gems=updated_gems
    #     )
    #
    # return None

    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    # Get the current game status
    current_game = cp.data.last_game
    # Get updated game
    updated_game= swap_gems(current_game, swap_data)

    return updated_game if updated_game is not None else None


@board_router.post("/click_gem", response_model=GameUpdateDTO | None, status_code=status.HTTP_200_OK)
async def click_gem_route(click: GemPositionDTO, cp: cp_dependency):
    """
    Check if clicked gem was a Bomb or Heal.
    If so, then update a game status.
    """

    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    # Get the current game status
    current_game = cp.data.last_game
    # Get updated game
    updated_game= click_gem(current_game, click)

    return updated_game if updated_game is not None else None


@board_router.post("/shuffle", response_model=List[List[int]], status_code=status.HTTP_200_OK)
async def shuffle_board(cp: cp_dependency):
    new_board = generate_game_board()
    cp.data.last_game.board_status = new_board
    return new_board
