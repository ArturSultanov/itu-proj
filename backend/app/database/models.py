from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from .database import Base

# Таблица Player
class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    current_game = Column(Integer, ForeignKey('games.id'), nullable=True)
    highest_score = Column(Integer, default=0)

    # Связь с таблицей Game
    games = relationship('Game', back_populates='player')

# Таблица Game
class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    gamer_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    current_score = Column(Integer, default=0)
    moves_left = Column(Integer, default=0)
    board_status = Column(JSON, nullable=False)  # Хранение двумерного массива в формате JSON

    # Связь с таблицей Player
    player = relationship('Player', back_populates='games')
