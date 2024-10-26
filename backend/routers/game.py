from fastapi import APIRouter
from backend.gamelogic.models import GameState
from backend.gamelogic.map_actions import load_game_state, save_game_state

router = APIRouter()

@router.get("/game/{user_id}", response_model=GameState)
async def get_game_state(user_id: str):
    return load_game_state(user_id)

@router.post("/game/update", response_model=GameState)
async def update_game_state(game_state: GameState):
    save_game_state(game_state)
    return game_state
