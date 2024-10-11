from models import Gem
import random

# Функция для проверки, можно ли добавить камень в эту позицию
def is_valid_choice(board, gem, row, col):
    # Проверка на больше чем два одинаковых камня по горизонтали
    if col >= 2 and board[row][col - 1] == gem and board[row][col - 2] == gem:
        return False
    # Проверка на больше чем два одинаковых камня по вертикали
    if row >= 2 and board[row - 1][col] == gem and board[row - 2][col] == gem:
        return False
    return True

# Функция генерации игрового поля с проверкой
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

# Вспомогательная функция для печати игрового поля
def print_game_board(board: list):
    for row in board:
        print(" | ".join(gem.name for gem in row))

# Генерация игрового поля 6x6
game_board = generate_game_board()

# Печать игрового поля
print_game_board(game_board)
