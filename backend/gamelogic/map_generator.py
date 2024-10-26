# utils/map_generator.py

from backend.gamelogic.models import Gem
import random

# Check if adding a gem creates a match of three in a row/column
def is_valid_choice(board, gem, row, col):
    if col >= 2 and board[row][col - 1] == gem and board[row][col - 2] == gem:
        return False
    if row >= 2 and board[row - 1][col] == gem and board[row - 2][col] == gem:
        return False
    return True

# Generate a game board with no initial matches
def generate_game_board(size: int = 6) -> list:
    gems = list(Gem)
    board = [[None for _ in range(size)] for _ in range(size)]

    for row in range(size):
        for col in range(size):
            gem = random.choice(gems)
            while not is_valid_choice(board, gem, row, col):
                gem = random.choice(gems)
            board[row][col] = gem

    return board
