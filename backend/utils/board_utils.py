import random
from typing import Tuple, Set, Dict, List, Optional

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
def find_matches(board: BoardState) -> Set[Tuple[int, int]]:
    """
    Find all gems matches on the board.

    Parameters:
        board (BoardState): The board to find matches on.

    Returns:
        Set[Tuple[int, int]]: A Set of coordinates where matches were found.
    """
    matches = set()  # Use a set to avoid duplicate matches
    board_state = board # Access the matrix directly from the BoardState instance

    # Horizontal matches
    for row in range(len(board_state)):
        for col in range(len(board_state[0]) - 2):
            if board_state[row][col] == board_state[row][col + 1] == board_state[row][col + 2] != None:
                matches.update([(row, col), (row, col + 1), (row, col + 2)])
    
    # Vertical matches
    for col in range(len(board_state[0])):
        for row in range(len(board_state) - 2):
            if board_state[row][col] == board_state[row + 1][col] == board_state[row + 2][col] != None:
                matches.update([(row, col), (row + 1, col), (row + 2, col)])
    
    return matches



def _is_valid_choice(board: List[List[int]], gem: int, row: int, col: int) -> bool:
    """
    Checks if placing a gem at the given position does not create a three-in-a-row match
    horizontally or vertically, considering board boundaries.

    Parameters:
        board (List[List[int]]): The game board.
        gem (int): The gem to place.
        row (int): The row index for the placement.
        col (int): The column index for the placement.

    Returns:
        bool: True if the gem can be placed without creating a match, False otherwise.
    """
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



# Update matched gems with new random gems
def replace_gems(board: BoardState, matches: Set[Tuple[int, int]]) -> Dict[Tuple[int, int], int]:
    """
    Replace the matched gems with new gems.
    Ensures there are no new three-in-a-row matches after replacement.

    Parameters:
        board (BoardState): The board to update with new gems.
        matches (Set[Tuple[int, int]]): A set of coordinates where matches were found.

    Returns:
        Dict[Tuple[int, int], int]: A dictionary where keys are coordinates and values are new gem colors.
    """
    board_state = board.board_state
    new_gems = {}  # Dictionary to store new gems by their coordinates
    gem_types = list(int)

    # Replace matched gems with new random gems
    for row, col in matches:
        new_gem = random.choice(gem_types)
        # Ensure the new gem does not immediately form a three-in-a-row
        while not _is_valid_choice(board_state, new_gem, row, col):
            new_gem = random.choice(gem_types)
        
        board_state[row][col] = new_gem
        new_gems[(row, col)] = new_gem  # Record the new gem and its position

    return new_gems

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

