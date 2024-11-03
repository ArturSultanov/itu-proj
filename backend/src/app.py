from fastapi import FastAPI
from typing import Dict
from src.database import Base, engine
import json

from contextlib import asynccontextmanager

# In-memory user session storage
user_sessions: Dict[str, dict] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
   # Create the database tables on startup
    Base.metadata.create_all()
    
    yield


@app.get("/")
async def index(request: Request, session: session_dependency):
    return templates.TemplateResponse("index.html", {"request": request, "user": session.user}, status_code=HTTP_200_OK)