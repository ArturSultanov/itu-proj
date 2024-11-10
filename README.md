# Game Application API

This project is a game application API developed with **FastAPI**. It allows users to manage player data, sync game states, adjust game settings, and perform game actions like clicking on gems or swapping them on the game board. The backend uses **SQLAlchemy** with an SQLite database for persistence and supports various levels of game difficulty.

## Features

- **Game Difficulty Adjustment**: Set difficulty levels (Easy, Normal, Hard) that control gameplay parameters.
- **Game Actions**: Perform in-game actions, including gem clicks and swaps, with appropriate handling for different gem types.
- **Player Synchronization**: Synchronize player data between in-memory state and the database.
- **RESTful API Design**: Follows REST principles for ease of use and consistency.

## Gem types:

- 0 - Standard gem 0
- 1 - Standard gem 1 
- 2 - Standard gem 1 
- 3 - Standard gem 1 
- 4 - Heal gem

## Run Application

To run application for frontend just run the [run_server.sh](run_server.sh) script.
It will automatically build and run docker image.

### Run command:

```bash
./run_server.sh
```

### Expected out:

```bash
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Run without Docker

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## Documentation for API
Documentation can be found at [http://0.0.0.0:8000/docs#](http://0.0.0.0:8000/docs#) after application startup.
