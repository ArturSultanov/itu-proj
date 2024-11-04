from fastapi import APIRouter
from starlette import status

from backend.database import cp_dependency
from backend.schemas import PlayerLoginDTO

settings_router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    responses={404: {"description": "Not Found"}},  # Custom response descriptions
)


# Settings/Change name
@settings_router.post("/update_login/", status_code=status.HTTP_200_OK)
async def get_or_create_player(player: PlayerLoginDTO, cp: cp_dependency):
    cp.data.login = player.login  # Update the login of the current player
    return {"msg": f"Player login updated to {cp.data.login}"}

# Settings/Difficulty level



