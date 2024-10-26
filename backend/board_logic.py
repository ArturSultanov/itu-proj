from typing import List, Tuple, Set
from models import Gem, GameState, BoardState
import random

# Check if adding a gem creates a match of three in a row/column
def is_valid_choice(board, gem, row, col):
    if col >= 2 and board[row][col - 1] == gem and board[row][col - 2] == gem:
        return False
    if row >= 2 and board[row - 1][col] == gem and board[row - 2][col] == gem:
        return False
    return True

# Generate a game board with no initial matches
def generate_game_board(size: int = 6) -> BoardState:
    gems = list(Gem)
    board = [[None for _ in range(size)] for _ in range(size)]

    for row in range(size):
        for col in range(size):
            gem = random.choice(gems)
            while not is_valid_choice(board, gem, row, col):
                gem = random.choice(gems)
            board[row][col] = gem

    # Return the board wrapped in a BoardState instance
    return BoardState(board_state=board)


# Check for matches of three or more
def find_matches(board: BoardState) -> Set[Tuple[int, int]]:
    """
    Find all gems matches on the board.

    Parameters:
        board (BoardState): The board to find matches on.

    Returns:
        List[Tuple[int, int]]: A list of coordinates where matches were found.
    """
    matches = set()  # Use a set to avoid duplicate matches
    board_state = board.board_state  # Access the matrix directly from the BoardState instance

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


