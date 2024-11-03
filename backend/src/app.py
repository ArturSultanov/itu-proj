from fastapi import FastAPI
from typing import Dict
from src.database import Base, engine
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

Base.metadata.create_all(engine)
