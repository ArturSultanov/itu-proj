# **Program Documentation**

## **Overview**
This SwiftUI application is a gem-matching game with user authentication and dynamic gameplay mechanics. It consists of multiple views, state management classes, and networking extensions. The application allows players to log in, start new games, continue or delete previous games, adjust settings, and interact with the game board in real time.

---

## **Key Components**

### **1. Views**
#### **LoginView**
- **Purpose**: Allows users to log in to the application.
- **Key Features**:
  - Displays a text field for entering the login name.
  - Enables the "Confirm" button only when a valid login name is provided.
  - Includes a "Quit Game" button that shows a confirmation alert before exiting.
- **Interconnections**:
  - On successful login, updates `PlayerDataManager` with user details and navigates to `MainMenuView`.
  - Uses `NetworkManager.login()` to send login data to the backend.

#### **MainMenuView**
- **Purpose**: Serves as the central hub for accessing other parts of the application.
- **Key Features**:
  - Displays user information, including login and highest score.
  - Buttons to start a new game, continue a previous game, access settings, view the leaderboard, and quit the game.
  - Handles confirmation alerts for quitting and deleting the last game.
  - Dynamically disables buttons for actions that are not available (e.g., "Continue" when no game exists).
- **Interconnections**:
  - Navigates to `GameBoardView`, `LeaderboardView`, or `SettingsView`.
  - Uses `NetworkManager` for actions like starting a new game, continuing a game, or deleting a game.

#### **GameBoardView**
- **Purpose**: Displays the game board where users interact with gems.
- **Key Features**:
  - Dynamically renders the gem layout based on the board state in `PlayerDataManager`.
  - Allows swapping gems with drag gestures or clicking specific heart gems.
  - Animates gem movements and updates the board after server responses.
- **Interconnections**:
  - Updates the board and score using `PlayerDataManager.updateGameSession()` after network responses.
  - Sends gem actions to the backend using `NetworkManager.swapGems()` or `NetworkManager.clickGem()`.

#### **SettingsView**
- **Purpose**: Provides options to manage user preferences.
- **Key Features**:
  - Allows changing the login, switching users, and adjusting the difficulty level.
  - Displays the current login and difficulty at the top.
  - Shows confirmation dialogs for user switching and difficulty selection.
  - Includes a sheet for editing the login.
- **Interconnections**:
  - Fetches and updates settings via `NetworkManager.getDifficulty()`, `NetworkManager.updateLogin()`, and `NetworkManager.setDifficulty()`.

#### **LeaderboardView**
- **Purpose**: Displays the top players and their highest scores.
- **Key Features**:
  - Fetches and shows the leaderboard data from the backend.
  - Highlights the top 3 players with a medal icon.
  - Uses a `List` to render dynamic content.
- **Interconnections**:
  - Fetches data using `NetworkManager.fetchLeaderboard()`.

---

### **2. State Management**
#### **PlayerDataManager**
- **Purpose**: Manages player data, including login, highest score, and current game session.
- **Key Features**:
  - Provides a single source of truth for the application state.
  - Updates dynamically with server responses.
- **Interconnections**:
  - Used by all views to fetch and update user data.
  - Modified by `NetworkManager` functions (e.g., login, game updates).

#### **Gem**
- **Purpose**: Represents individual gems on the game board.
- **Key Features**:
  - Includes properties for type, position (`x`, `y`), and unique ID.
  - Implements `Codable` for server communication.
- **Interconnections**:
  - Rendered in `GameBoardView` using `GemView`.
  - Updated in `PlayerDataManager` after server responses.

---

### **3. Networking**
#### **NetworkManager**
- **Purpose**: Handles all backend communication.
- **Key Features**:
  - Provides singleton access (`NetworkManager.shared`).
  - Implements various functions for logging in, starting new games, continuing games, updating settings, and interacting with the board.
- **Extensions**:
  - Divided into functional areas:
    - Login (`login()`)
    - Game management (`newGame()`, `continue_game()`, `deleteGame()`)
    - Board interactions (`swapGems()`, `clickGem()`)
    - Settings (`updateLogin()`, `setDifficulty()`, `getDifficulty()`)
    - Utilities (`quitGame()`)
- **Interconnections**:
  - Called by views to send or fetch data from the backend.
  - Updates `PlayerDataManager` with server responses.

---

### **4. Utilities**
#### **Button Styles**
- `MainMenuButtonStyle`: Customizes the appearance of buttons in the main menu and other views.
- `SecondaryMenuButtonStyle`: Used for secondary actions like the trash icon in `MainMenuView`.

#### **Enums**
- **Direction**: Represents directions (`up`, `down`, `left`, `right`) for gem swapping.
- **IconType**: Maps gem types to their respective colors and SF Symbols.

---

## **Workflow**

### **1. User Login**
1. The application starts with `LoginView`.
2. The user enters their login name and presses "Confirm."
3. `NetworkManager.login()` sends the login data to the backend.
4. On success:
   - The app updates `PlayerDataManager` with user data.
   - The user is navigated to `MainMenuView`.

### **2. Main Menu Navigation**
1. **New Game**:
   - `NetworkManager.newGame()` initializes a new game session on the server.
   - Updates `PlayerDataManager` with the new session.
   - Navigates to `GameBoardView`.
2. **Continue Game**:
   - If a previous game exists, `NetworkManager.continue_game()` fetches it from the server.
   - Updates `PlayerDataManager` and navigates to `GameBoardView`.
3. **Delete Game**:
   - Shows a confirmation alert.
   - On confirmation, `NetworkManager.deleteGame()` deletes the game session on the server.
   - Sets `lastGame` to `nil` in `PlayerDataManager`.
4. **Settings**:
   - Navigates to `SettingsView`.
5. **Leaderboard**:
   - Navigates to `LeaderboardView`.
6. **Quit Game**:
   - Shows a confirmation alert.
   - On confirmation, `NetworkManager.quitGame()` sends a quit request, and the app terminates.

### **3. Game Board Interactions**
1. Renders the game board dynamically based on the current `PlayerDataManager.lastGame`.
2. Swapping gems:
   - Dragging a gem sends a request to the backend (`NetworkManager.swapGems()`).
   - The server validates and returns updated board data.
   - Updates the board and score in `PlayerDataManager`.
3. Clicking heart gems:
   - Sends a click action to the backend (`NetworkManager.clickGem()`).
   - Updates the board and score based on the server response.

### **4. Settings Management**
1. Fetches the current difficulty from the backend when the view appears.
2. Allows users to:
   - **Change Login**:
     - Opens a sheet to edit the login.
     - Sends the updated login to the backend (`NetworkManager.updateLogin()`).
   - **Switch User**:
     - Shows a confirmation alert.
     - Navigates back to `LoginView` on confirmation.
   - **Change Difficulty**:
     - Opens a dialog for selecting a new difficulty level.
     - Sends the updated difficulty to the backend (`NetworkManager.setDifficulty()`).

### **5. Leaderboard**
1. Fetches the top players from the backend using `NetworkManager.fetchLeaderboard()`.
2. Displays the leaderboard in a list with dynamic styling for the top 3 players.

---

## **How Components Interconnect**
- **Views** interact with **PlayerDataManager** for state management and use **NetworkManager** to communicate with the backend.
- **PlayerDataManager** serves as the single source of truth, updated dynamically by views or network responses.
- **NetworkManager** ensures seamless interaction with the backend and updates the state in `PlayerDataManager`.

