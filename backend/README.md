# Direcrory structure


- **main.py**: The main file where the FastAPI application will be launched. Contains the initialization of the application and the connection of routers.
- **models.py**: Data models used by Pydantic to describe the data schema (e.g. GameState).

- **routers/**: A folder for storing files with routes that process API requests. This helps to separate the query processing logic from the main logic.
- **services/**: Business logic is located here, for example, functions for downloading and updating the user's game state. This allows you to separate the logic of working with data from routes.
- **utils/**: A folder for auxiliary utilities, for example, for working with files, reading and writing JSON data.
