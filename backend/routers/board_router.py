from fastapi import APIRouter, status, HTTPException
from typing import List, Optional, Annotated, Tuple
from backend.database import cp_dependency
from backend.schemas import BoardUpdateDTO
from backend.utils import swap_gems

# from backend.utils.board_generator import generate_game_board

board_router = APIRouter(
    prefix="/board",
    tags=["board"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)



@board_router.post("/swap_gems", response_model=BoardUpdateDTO | None, status_code=status.HTTP_200_OK)
async def swap_gems_route(gems: Tuple[Tuple[int, int], Tuple[int, int]], cp: cp_dependency):
    """
    Check if there are any matches,
    then update the player score,
    and decrease the moves number.
    """
    # Проверяем, что данные игрока загружены
    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    board = cp.data.last_game.board_status

    # Вызываем функцию swap_gems для обмена и поиска совпадений
    updated_gem, matches_number = swap_gems(board, gems[0], gems[1])

    if updated_gem and matches_number != 0:
        # Обновляем счёт и количество оставшихся ходов
        cp.data.last_game.current_score += matches_number * 10
        cp.data.last_game.moves_left -= 1

        # Возвращаем обновлённые данные в виде BoardUpdateDTO
        return BoardUpdateDTO(
            current_score=cp.data.last_game.current_score,
            moves_left=cp.data.last_game.moves_left,
            updated_gem=updated_gem
        )

    return None



def use_bomb():
    pass

def use_heal():
    pass
