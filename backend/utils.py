import os
import json
from models import Gem, GameState, BoardState


def get_file_path(user_id: str) -> str:
    return os.path.join("data", f"{user_id}.json")

def load_level(level_id):
    with open(f"levels/level_{level_id}.json", "r") as f:
        return json.load(f)
    

# # DEPRICATED Generate a game board with no initial matches
# def generate_game_board(size: int = 6) -> BoardState:
#     def is_valid_choice(board, gem, row, col):
#         if col >= 2 and board[row][col - 1] == gem and board[row][col - 2] == gem:
#             return False
#         if row >= 2 and board[row - 1][col] == gem and board[row - 2][col] == gem:
#             return False
#         return True
#     gems = list(Gem)
#     board = [[None for _ in range(size)] for _ in range(size)]

#     for row in range(size):
#         for col in range(size):
#             gem = random.choice(gems)
#             while not is_valid_choice(board, gem, row, col):
#                 gem = random.choice(gems)
#             board[row][col] = gem

#     # Return the board wrapped in a BoardState instance
#     return BoardState(board_state=board)