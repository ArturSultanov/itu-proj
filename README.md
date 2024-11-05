# Game Application API

This project is a game application API developed with **FastAPI**. It allows users to manage player data, sync game states, adjust game settings, and perform game actions like clicking on gems or swapping them on the game board. The backend uses **SQLAlchemy** with an SQLite database for persistence and supports various levels of game difficulty.

## Features

- **Game Difficulty Adjustment**: Set difficulty levels (Easy, Normal, Hard) that control gameplay parameters.
- **Game Actions**: Perform in-game actions, including gem clicks and swaps, with appropriate handling for different gem types.
- **Player Synchronization**: Synchronize player data between in-memory state and the database.
- **RESTful API Design**: Follows REST principles for ease of use and consistency.
