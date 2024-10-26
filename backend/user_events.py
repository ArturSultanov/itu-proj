from .models import Gem, GameState, BoardState
# from backend.utils.board_generator import generate_game_board

# Swap two gems on the board
def swap_gems(board: BoardState, pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
    """
    Swap two gems on the board.

    Parameters:
        board (BoardState): The BoardState instance representing the game board.
        pos1 (Tuple[int, int]): Coordinates of the first gem to swap (row, col).
        pos2 (Tuple[int, int]): Coordinates of the second gem to swap (row, col).
    """
    (x1, y1), (x2, y2) = pos1, pos2
    board_state = board.board_state  # Access the board matrix

    # Validate that positions are within board bounds
    if (
        0 <= x1 < len(board_state) and 0 <= y1 < len(board_state[0]) and
        0 <= x2 < len(board_state) and 0 <= y2 < len(board_state[0])
    ):
        # Swap the gems at the specified positions
        board_state[x1][y1], board_state[x2][y2] = board_state[x2][y2], board_state[x1][y1]
    else:
        raise ValueError("Swap positions are out of board bounds")

def use_bomb():
    pass

def use_heal():
    pass
