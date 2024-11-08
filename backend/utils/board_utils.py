import random
from enum import Enum
from typing import Tuple, Set, List, Optional

from backend.config import get_heart_recovery_moves
from backend.schemas import GemPositionDTO, GameUpdateDTO, GemBase, PlayerDTO, SwapGemsDTO


class GemType(Enum):
    GEM0 = 0
    GEM1 = 1
    GEM2 = 2
    GEM3 = 3
    HEART = 4


# Schema for board state
BoardState = List[List[int]]


# Check for matches of three or more
def find_matches(board: BoardState) -> Optional[Set[Tuple[int, int]]]:
    """
    Find all gem matches on the board.

    Parameters:
        board (BoardState): The board to find matches on.

    Returns:
        Optional[Set[Tuple[int, int]]]: A set of coordinates where matches were found, or None if no matches.
    """
    matches: Set[Tuple[int, int]] = set()

    # Horizontal matches
    for row in range(len(board)):
        for col in range(len(board[0]) - 2):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] is not None:
                matches.update({(row, col), (row, col + 1), (row, col + 2)})

    # Vertical matches
    for col in range(len(board[0])):
        for row in range(len(board) - 2):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] is not None:
                matches.update({(row, col), (row + 1, col), (row + 2, col)})

    return matches if matches else None


def _is_valid_choice(board: BoardState, gem: GemType, row: int, col: int) -> bool:
    """
    Check if placing a gem at the given position does not create a three-in-a-row match
    horizontally or vertically, considering board boundaries.

    Parameters:
        board (BoardState): The game board.
        gem (GemType): The gem to place.
        row (int): The row index for the placement.
        col (int): The column index for the placement.

    Returns:
        bool: True if the gem can be placed without creating a match, False otherwise.
    """
    if gem == GemType.HEART:
        for r in board:
            if GemType.HEART.value in r:
                return False  # HEART exists on the board

    rows, cols = len(board), len(board[0])

    # Horizontal matches check
    if col >= 2 and board[row][col - 1] == gem.value and board[row][col - 2] == gem.value:
        return False
    if col < cols - 2 and board[row][col + 1] == gem.value and board[row][col + 2] == gem.value:
        return False
    if 0 < col < cols - 1 and board[row][col - 1] == gem.value and board[row][col + 1] == gem.value:
        return False

    # Vertical matches check
    if row >= 2 and board[row - 1][col] == gem.value and board[row - 2][col] == gem.value:
        return False
    if row < rows - 2 and board[row + 1][col] == gem.value and board[row + 2][col] == gem.value:
        return False
    if 0 < row < rows - 1 and board[row - 1][col] == gem.value and board[row + 1][col] == gem.value:
        return False

    return True


# Replace matched gems with new gems
def replace_gems(board: BoardState, matches: Set[Tuple[int, int]]) -> List[GemBase]:
    """
    Replace the matched gems with new gems.
    Ensures there are no new three-in-a-row matches after replacement.

    Parameters:
        board (BoardState): The board to update with new gems.
        matches (Set[Tuple[int, int]]): A set of coordinates where matches were found.

    Returns:
        List[GemBase]: A list of GemBase objects with the updated gems' positions and types.
    """
    new_gems: Set[Tuple[int, int, GemType]] = set()

    for row, col in matches:
        new_gem = random.choice(list(GemType))
        while not _is_valid_choice(board, new_gem, row, col):
            new_gem = random.choice(list(GemType))

        board[row][col] = int(new_gem.value)
        new_gems.add((row, col, new_gem))

    updated_gems = [GemBase(x=x, y=y, type=gem_type) for y, x, gem_type in new_gems]
    return updated_gems


def _update_game_status(player_data: PlayerDTO, moves: int, matches_number: int, replaced_gems: List[GemBase]) \
        -> GameUpdateDTO:
    player_data.last_game.moves_left += moves
    player_data.last_game.current_score += matches_number * 10

    if player_data.last_game.current_score > (player_data.highest_score or 0):
        player_data.highest_score = int(player_data.last_game.current_score)

    return GameUpdateDTO(
        current_score=player_data.last_game.current_score,
        moves_left=player_data.last_game.moves_left,
        updated_gems=replaced_gems
    )


# Swap two gems on the board
def swap_gems(player_data: PlayerDTO, swap_data: SwapGemsDTO) -> Optional[GameUpdateDTO]:

    board = player_data.last_game.board_status
    replaced_gems: Optional[List[GemBase]] = None
    moves = 0
    matches_number = 0

    (x1, y1), (x2, y2) = (swap_data.gems[0].x, swap_data.gems[0].y), (swap_data.gems[1].x, swap_data.gems[1].y)

    # Ensure positions are within bounds
    if (
            0 <= x1 < len(board) and 0 <= y1 < len(board[0]) and
            0 <= x2 < len(board) and 0 <= y2 < len(board[0])
    ):
        # Swap the gems
        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]
    else:
        raise ValueError("Swap positions are out of board bounds")

    matches = find_matches(board)

    if matches:
        moves = -1
        matches_number = len(matches)
        replaced_gems = replace_gems(board, matches)
    else:
        # Swap the gems
        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]

    if replaced_gems:
        return _update_game_status(player_data, moves, matches_number, replaced_gems)
    return None

# User clicked at some gem


def click_gem(player_data: PlayerDTO, pos: GemPositionDTO) -> Optional[GameUpdateDTO]:

    board = player_data.last_game.board_status
    clicked_gem = GemType(board[pos.x][pos.y])
    replaced_gems: Optional[List[GemBase]] = None
    moves = 0
    matches_number = 0

    match clicked_gem:
        case GemType.HEART:
            moves = get_heart_recovery_moves()
            matches_number = 1
            replaced_gems = replace_gems(board, {(pos.x, pos.y)})
        case _:
            pass

    if replaced_gems:
        return _update_game_status(player_data, moves, matches_number, replaced_gems)
    return None


def generate_game_board(size: int = 6) -> BoardState:
    """
    Generate a new game board of specified size with no initial matches.

    Parameters:
        size (int): The size of the board (size x size).

    Returns:
        BoardState: A board filled with random gems, ensuring no three-in-a-row matches.
    """
    # Initialize an empty board
    board: List[List[Optional[int]]] = [[None for _ in range(size)] for _ in range(size)]

    # Fill the board with gems ensuring no initial matches
    for row in range(size):
        for col in range(size):
            new_gem = random.choice(list(GemType))
            while not _is_valid_choice(board, new_gem, row, col):
                new_gem = random.choice(list(GemType))

            board[row][col] = new_gem.value

    return board
