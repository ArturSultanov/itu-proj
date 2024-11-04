from typing import Annotated
from typing import Optional
from fastapi import HTTPException, Depends, status
from backend.schemas import PlayerDTO


class CurrentPlayer:
    def __init__(self):
        self.data: Optional[PlayerDTO] = None  # Stores the current player's data

    def load_player(self, player_data: PlayerDTO):
        """Load the player data into the current player instance."""
        self.data = player_data

    def is_loaded(self) -> bool:
        """Check if the current player data is loaded."""
        return self.data is not None

current_player = CurrentPlayer()

# Dependency function to check if current player is loaded
def get_current_player() -> CurrentPlayer:
    if not current_player.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Current player not found"
        )
    return current_player

# Annotated dependency for use in routes
cp_dependency = Annotated[CurrentPlayer, Depends(get_current_player)]