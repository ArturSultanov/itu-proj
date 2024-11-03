import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from config.state_manager import settings
from database.database import create_tables, async_engine
from routers.player_routes import player_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.include_router(player_router)

    #app.mount(settings.APP_STATIC_PATH, StaticFiles(directory="static"), name="static")

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
    return {"Hello!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.WEB_HOST, port=settings.WEB_PORT, reload=True)