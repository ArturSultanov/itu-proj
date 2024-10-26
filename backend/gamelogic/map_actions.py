from backend.gamelogic.models import Gem, GameState, BoardState
from backend.gamelogic.map_generator import generate_game_board
import random

# Swap two gems in the board
def swap_gems(board, pos1, pos2):
    (x1, y1), (x2, y2) = pos1, pos2
    board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]

# Check for matches of three or more
def find_matches(board):
    matches = []
    # Horizontal matches
    for row in range(len(board)):
        for col in range(len(board[0]) - 2):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] != None:
                matches.extend([(row, col), (row, col + 1), (row, col + 2)])
    
    # Vertical matches
    for col in range(len(board[0])):
        for row in range(len(board) - 2):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] != None:
                matches.extend([(row, col), (row + 1, col), (row + 2, col)])
    
    return list(set(matches))

# Remove matched stones and shift down remaining stones
def clear_matches_and_update_board(board, matches):
    for (x, y) in matches:
        board[x][y] = None  # Clear matched gems
    
    # Shift gems down to fill cleared spots
    for col in range(len(board[0])):
        empty_slots = [row for row in range(len(board)) if board[row][col] is None]
        filled_slots = [row for row in range(len(board)) if board[row][col] is not None]
        for i, row in enumerate(reversed(empty_slots)):
            if filled_slots:
                board[row][col] = filled_slots.pop()
            else:
                board[row][col] = random.choice(list(Gem))  # Fill top with new gems

    return board


def calculate_score(matches_count):
    # Each matched set of three increases score by 100 points
    return matches_count * 100
