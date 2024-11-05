from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from backend.config import settings
from backend.database import create_tables, async_engine
from backend.routers import board_router, login_router, menu_router, settings_router, utils_router


@asynccontextmanager
async def lifespan(main: FastAPI):
    main.include_router(board_router)
    main.include_router(login_router)
    main.include_router(menu_router)
    main.include_router(settings_router)
    main.include_router(utils_router)

    # Initialization logic (e.g., creating tables or setting up connections)
    print("Starting up the app...")
    await create_tables()  # Ensures tables are created at startup
    
    try:
        yield  # Control is handed over to the FastAPI app at this point
    finally:
        # Cleanup logic (e.g., closing connections or other teardown activities)
        print("Shutting down the app...")
        await async_engine.dispose()  # Properly close the async engine

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"""This project is a game application API developed with FastAPI.
 
    It allows users to manage player data, sync game states, adjust game settings, 
    and perform game actions like clicking on gems or swapping them on the game board. 
    The backend uses SQLAlchemy with an SQLite database for persistence and supports various 
    levels of game difficulty."""}

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.WEB_HOST, port=settings.WEB_PORT, reload=True)
