from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.settings import settings
from database.database import create_tables, async_engine
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.WEB_HOST, port=settings.WEB_PORT, reload=True)