import random
from typing import Tuple, Set, List, Optional

# # Enum for types of gems
# class int(Enum):
#     GEM0 = 0
#     GEM1 = 1
#     GEM2 = 2
#     GEM3 = 3
#     BOMB = 4
#     HEART = 5

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


# Check for valid gem placement without immediate match
def _is_valid_choice(board: BoardState, gem: int, row: int, col: int) -> bool:
    rows, cols = len(board), len(board[0])

    # Horizontal check
    if col >= 2 and board[row][col - 1] == gem and board[row][col - 2] == gem:
        return False
    if col < cols - 2 and board[row][col + 1] == gem and board[row][col + 2] == gem:
        return False
    if 0 < col < cols - 1 and board[row][col - 1] == gem and board[row][col + 1] == gem:
        return False

    # Vertical check
    if row >= 2 and board[row - 1][col] == gem and board[row - 2][col] == gem:
        return False
    if row < rows - 2 and board[row + 1][col] == gem and board[row + 2][col] == gem:
        return False
    if 0 < row < rows - 1 and board[row - 1][col] == gem and board[row + 1][col] == gem:
        return False

    return True


# Replace matched gems with new gems
def replace_gems(board: BoardState, matches: Set[Tuple[int, int]]) -> Set[Tuple[int, int, int]]:
    """
    Replace the matched gems with new gems.
    Ensures there are no new three-in-a-row matches after replacement.

    Parameters:
        board (BoardState): The board to update with new gems.
        matches (Set[Tuple[int, int]]): A set of coordinates where matches were found.

    Returns:
        Set[Tuple[int, int, int]]: A set of tuples with the format (row, col, new_gem).
    """
    new_gems: Set[Tuple[int, int, int]] = set()

    for row, col in matches:
        new_gem = random.randint(0, 3)
        while not _is_valid_choice(board, new_gem, row, col):
            new_gem = random.randint(0, 3)

        board[row][col] = new_gem
        new_gems.add((row, col, new_gem))

    return new_gems


# Swap two gems on the board
def swap_gems(board: BoardState, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> Tuple[Optional[Set[Tuple[int, int, int]]], int]:
    """
    Swap two gems on the board and replace matched gems if any.

    Parameters:
        board (BoardState): The board to update.
        pos1 (Tuple[int, int]): First position (row, col).
        pos2 (Tuple[int, int]): Second position (row, col).

    Returns:
        Tuple[Optional[Set[Tuple[int, int, int]]], int]: New gems after replacing matches and count of matches, or (None, 0) if no matches were found.
    """
    (x1, y1), (x2, y2) = pos1, pos2

    # Ensure positions are within bounds
    if (
            0 <= x1 < len(board) and 0 <= y1 < len(board[0]) and
            0 <= x2 < len(board) and 0 <= y2 < len(board[0])
    ):
        # Swap the gems
        board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]
    else:
        raise ValueError("Swap positions are out of board bounds")

    matches = find_matches(board)
    if matches:
        return replace_gems(board, matches), len(matches)

    return None, 0


# Generate a game board with no initial matches
def generate_game_board(size: int = 6) ->  BoardState:
    def check_gems(c_board: List[List[Optional[int]]], c_gem: int, c_row: int, c_col: int) -> bool:
        """Check if placing the current gem would create a match of three."""
        # Check for horizontal matches
        if c_col >= 2 and c_board[c_row][c_col - 1] == c_gem and c_board[c_row][c_col - 2] == c_gem:
            return False
        # Check for vertical matches
        if c_row >= 2 and c_board[c_row - 1][c_col] == c_gem and c_board[c_row - 2][c_col] == c_gem:
            return False
        return True

    # Initialize an empty board
    board: List[List[Optional[int]]] = [[None for _ in range(size)] for _ in range(size)]

    # Fill the board with gems ensuring no initial matches
    for row in range(size):
        for col in range(size):
            gem: int = random.randint(0, 3)
            while not check_gems(board, gem, row, col):
                gem = random.randint(0, 3)
            board[row][col] = gem
    return board

