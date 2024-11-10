from fastapi import APIRouter, HTTPException, status

from backend.database import cp_dependency, db_dependency
from backend.models import GameUpdateDTO, SwapGemsDTO, GemPositionDTO, BordStatusDTO, UpdateMessageDTO, GameDTO
from backend.utils import swap_gems, generate_game_board, click_gem, synchronize_player, swap_gems_fullboard, \
    click_gem_fullboard

# from backend.utils.board_generator import generate_game_board

board_router = APIRouter(
    prefix="/board",
    tags=["board"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)


@board_router.post("/swap_gems_fullboard", response_model=GameDTO | UpdateMessageDTO, status_code=status.HTTP_200_OK)
async def swap_gems_fullboard_route(swap_data: SwapGemsDTO, cp: cp_dependency, db: db_dependency):
    """
    Check if there are any matches,
    then update the player score,
    and decrease the moves number.
    Return the whole board.
    """
    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    # Get the current game status
    player_data = cp.data

    if player_data.last_game.moves_left == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No moves left.")

    # Get updated game
    updated_board = swap_gems_fullboard(player_data, swap_data)
    await synchronize_player(cp.data, db)
    if updated_board is not None:
        return updated_board
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No board found.")


@board_router.post("/click_gem_fullboard", response_model=GameDTO | UpdateMessageDTO, status_code=status.HTTP_200_OK)
async def click_gem_fullboard_route(click: GemPositionDTO, cp: cp_dependency, db: db_dependency):
    """
    Check if clicked gem was a Bomb or Heal.
    If so, then update a game status.
    """
    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    # Get the current game status
    player_data = cp.data

    if player_data.last_game.moves_left == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No moves left.")

    # Get updated game
    updated_board = click_gem_fullboard(player_data, click)
    await synchronize_player(cp.data, db)

    # return updated_board if updated_board is not None else UpdateMessageDTO(detail="No clickable gems found.")

    if updated_board is not None:
        return updated_board
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No clickable gems found.")



@board_router.post("/swap_gems", response_model=GameUpdateDTO | UpdateMessageDTO, status_code=status.HTTP_200_OK)
async def swap_gems_route(swap_data: SwapGemsDTO, cp: cp_dependency, db: db_dependency):
    """
    Check if there are any matches,
    then update the player score,
    and decrease the moves number.
    Return only updated gems.
    """
    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    # Get the current game status
    player_data = cp.data

    if player_data.last_game.moves_left == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No moves left.")

    # Get updated game
    updated_game = swap_gems(player_data, swap_data)
    await synchronize_player(cp.data, db)


    if updated_game is not None:
        return updated_game
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No matches found.")


@board_router.post("/click_gem", response_model=GameUpdateDTO | UpdateMessageDTO, status_code=status.HTTP_200_OK)
async def click_gem_route(click: GemPositionDTO, cp: cp_dependency, db: db_dependency):
    """
    Check if clicked gem was a Bomb or Heal.
    If so, then update a game status.
    """

    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    # Get the current game status
    player_data = cp.data

    if player_data.last_game.moves_left == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No moves left.")

    # Get updated game
    updated_game = click_gem(player_data, click)
    await synchronize_player(cp.data, db)
    if updated_game is not None:
        return updated_game
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No clickable gems found.")


@board_router.get("/shuffle", response_model=BordStatusDTO, status_code=status.HTTP_200_OK)
async def shuffle_board(cp: cp_dependency, db: db_dependency):
    if not cp or not cp.data or not cp.data.last_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current game data not found.")

    new_board = generate_game_board()
    cp.data.last_game.board_status = new_board
    await synchronize_player(cp.data, db)
    return BordStatusDTO(board_status=new_board)
