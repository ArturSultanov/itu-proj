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

@app.post("/make_move/{user_id}")
async def make_move(user_id: str, move: dict):
    # Example move: {"type": "swap", "position": [x, y], "direction": "left"}
    if user_id in user_sessions:
        # Update score, moves, and board state accordingly
        user_sessions[user_id]["moves_left"] -= 1
        # Update board state logic here...
        user_sessions[user_id]["score"] += 100  # Example score update

        return {"message": f"Move processed for user {user_id}"}
    else:
        return {"error": "User session not found"}

@app.post("/complete_level/{user_id}")
async def complete_level(user_id: str):
    if user_id in user_sessions:
        # Get user progress
        user_data = user_sessions[user_id]

        # Save progress to a JSON file (e.g., user progress file)
        with open(f"data/user_{user_id}_progress.json", "w") as f:
            json.dump(user_data, f)

        # Clear session from memory after saving
        del user_sessions[user_id]

        return {"message": f"Level {user_data['current_level']} completed for user {user_id}"}
    else:
        return {"error": "User session not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
