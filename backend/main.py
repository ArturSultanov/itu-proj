from fastapi import FastAPI
from typing import Dict
import json

app = FastAPI()

# In-memory user session storage
user_sessions: Dict[str, dict] = {}

@app.get("/")
async def print_hello():
    message = "Hello, what are you looking for here? 🐸"
    return message

# Enter user_id
@app.get("/login/{user_id}")
async def login(user_id: str):
    pass

# Start new game
@app.post("/newgame/{user_id}")
async def newgame(user_id: str):
    pass

@app.get("/continuegame/{user_id}")
async def continuegame(user_id: str):
    pass


@app.get("/leaderboard/{page}")
async def show_leaderboard(page: int):
    pass

# @app.post("/start_level/{user_id}/{level_id}")
# async def start_level(user_id: str, level_id: int):
#     level_data = load_level(level_id)
#     # Initialize user session
#     user_sessions[user_id] = {
#         "current_level": level_id,
#         "score": 0,
#         "moves_left": level_data["max_moves"],
#         "board_state": level_data["initial_board"]
#     }
#     return {"message": f"Level {level_id} started for user {user_id}"}