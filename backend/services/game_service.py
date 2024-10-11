import json
from models import GameState
from utils.file_utils import get_file_path

def load_game_state(user_id: str) -> GameState:
    file_path = get_file_path(user_id)
    with open(file_path, "r") as file:
        data = json.load(file)
    return GameState(**data)

def save_game_state(game_state: GameState):
    file_path = get_file_path(game_state.user_id)
    with open(file_path, "w") as file:
        json.dump(game_state.dict(), file)
