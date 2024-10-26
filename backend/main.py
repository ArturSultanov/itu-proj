from fastapi import FastAPI
from typing import Dict
import json

app = FastAPI()

# In-memory user session storage
user_sessions: Dict[str, dict] = {}

# Simulate loading a level
def load_level(level_id):
    with open(f"data/level_{level_id}.json", "r") as f:
        return json.load(f)
    
@app.get("/")
async def print_hello():
    return "Hello"

@app.post("/start_level/{user_id}/{level_id}")
async def start_level(user_id: str, level_id: int):
    level_data = load_level(level_id)
    # Initialize user session
    user_sessions[user_id] = {
        "current_level": level_id,
        "score": 0,
        "moves_left": level_data["max_moves"],
        "board_state": level_data["initial_board"]
    }
    return {"message": f"Level {level_id} started for user {user_id}"}