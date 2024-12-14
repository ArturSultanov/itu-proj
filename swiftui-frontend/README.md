
# **Program Documentation**

## **Overview**
This SwiftUI application is a dynamic gem-matching game featuring user authentication, customizable settings, and real-time game board interactions. It is built with a modular architecture, separating concerns across views, state management, networking, and styling. Players can log in, manage settings, view leaderboards, and interact with the game board seamlessly.

---

## **Key Components**

### **1. Views**

#### **LoginView**
- **Purpose**: Handles user authentication by allowing players to log in.
- **Key Features**:
  - Input field for login names.
  - Disabled "Confirm" button until valid input is provided.
  - A "Quit Game" button with a confirmation alert.
- **Interconnections**:
  - Calls `NetworkManager.login()` to validate login credentials with the backend.
  - Updates `PlayerDataManager` upon successful login and navigates to `MainMenuView`.

#### **MainMenuView**
- **Purpose**: Acts as the main navigation hub.
- **Key Features**:
  - Displays user details, including login and highest score.
  - Options to start a new game, continue a previous game, access settings, view the leaderboard, or quit.
  - Dynamically disables unavailable options (e.g., "Continue" when no game exists).
  - Shows confirmation alerts for quitting or deleting a game.
- **Interconnections**:
  - Uses `PlayerDataManager` for user information.
  - Calls various `NetworkManager` methods for game session management.
  - Navigates to `GameBoardView`, `LeaderboardView`, or `SettingsView`.

#### **GameBoardView**
- **Purpose**: Represents the main game board for gem-matching.
- **Key Features**:
  - Displays a grid of gems rendered dynamically based on the board's state.
  - Allows gem swaps using drag gestures or clicking specific heart gems.
  - Includes buttons for shuffling the board and pausing the game.
  - Animates gem interactions and updates based on server responses.
- **Interconnections**:
  - Uses `PlayerDataManager` to fetch and update the game board state.
  - Sends actions like swaps or gem clicks to the backend via `NetworkManager`.
  - Displays a notification banner for scenarios like zero moves remaining.

#### **SettingsView**
- **Purpose**: Allows players to manage app preferences.
- **Key Features**:
  - Change login, switch user, or adjust difficulty.
  - Toggle between color palettes (e.g., tritanopia and normal).
  - Displays confirmation dialogs for sensitive actions like switching users.
  - Includes a sheet for editing login credentials.
- **Interconnections**:
  - Calls `NetworkManager` for login updates, difficulty changes, and user settings management.
  - Uses `PaletteManager` to manage the active color palette.

#### **LeaderboardView**
- **Purpose**: Displays a ranked list of top players.
- **Key Features**:
  - Fetches leaderboard data from the backend.
  - Highlights the top 3 players with a medal icon.
  - Renders the leaderboard dynamically in a list view.
- **Interconnections**:
  - Fetches data via `NetworkManager.fetchLeaderboard()`.

---

### **2. State Management**

#### **PlayerDataManager**
- **Purpose**: Centralizes user data management.
- **Key Features**:
  - Maintains player details, such as login, highest score, and game session.
  - Updates dynamically based on server responses.
- **Interconnections**:
  - Accessed by all views to display or modify player data.
  - Updated through `NetworkManager` actions like login, game updates, and settings changes.

#### **Gem**
- **Purpose**: Represents individual gems on the board.
- **Key Features**:
  - Encapsulates gem properties such as type, position (`x`, `y`), and a unique ID.
  - Implements `Codable` for seamless server communication.
- **Interconnections**:
  - Rendered in `GameBoardView` using `GemView`.
  - Updated in `PlayerDataManager` after server responses.

---

### **3. Networking**

#### **NetworkManager**
- **Purpose**: Manages all backend interactions.
- **Key Features**:
  - Singleton instance (`NetworkManager.shared`) for centralized networking.
  - Divided into functional extensions:
    - Login (`login()`)
    - Game management (`newGame()`, `continue_game()`, `deleteGame()`)
    - Board interactions (`swapGems()`, `clickGem()`, `shuffleBoard()`)
    - Settings (`updateLogin()`, `setDifficulty()`, `getDifficulty()`)
    - Utilities (`quitGame()`)
- **Interconnections**:
  - Handles backend communication and updates `PlayerDataManager`.
  - Provides error handling and banner notifications for failed requests.

---

### **4. Utilities**

#### **Button Styles**
- `MainMenuButtonStyle`: Applies consistent styling to primary buttons in the app.
- `SecondaryMenuButtonStyle`: Used for smaller, secondary actions (e.g., delete buttons).

#### **Enums**
- **Direction**: Represents movement directions (`up`, `down`, `left`, `right`) for gem swaps.
- **IconType**: Maps gem types to corresponding icons and colors.

#### **BannerManager**
- **Purpose**: Handles displaying notification banners for errors or messages.
- **Key Features**:
  - Displays a customizable message at the top of the screen.
  - Supports smooth transitions for showing and dismissing banners.

---

## **Workflow**

### **1. User Login**
1. The app starts at `LoginView`.
2. User enters a name and clicks "Confirm."
3. `NetworkManager.login()` sends the login request to the backend.
4. On success:
   - `PlayerDataManager` is updated with user details.
   - The app navigates to `MainMenuView`.

### **2. Main Menu**
1. **New Game**:
   - `NetworkManager.newGame()` initializes a new session.
   - Updates `PlayerDataManager.lastGame` and navigates to `GameBoardView`.
2. **Continue Game**:
   - Fetches the last session with `NetworkManager.continue_game()`.
   - Updates `PlayerDataManager` and navigates to `GameBoardView`.
3. **Delete Game**:
   - Deletes the last session via `NetworkManager.deleteGame()`.
   - Updates `PlayerDataManager.lastGame` to `nil`.
4. **Settings**:
   - Navigates to `SettingsView`.
5. **Leaderboard**:
   - Navigates to `LeaderboardView`.
6. **Quit Game**:
   - Shows a confirmation alert before closing the app.

### **3. Game Board**
1. **Render Board**:
   - The board is initialized based on `PlayerDataManager.lastGame`.
2. **Gem Interactions**:
   - Swapping gems triggers a backend request via `NetworkManager.swapGems()`.
   - Clicking heart gems sends a `NetworkManager.clickGem()` request.
3. **Shuffling Board**:
   - Clicking "Shuffle" calls `NetworkManager.shuffleBoard()` and updates the game state.
4. **Pausing**:
   - Clicking "Pause" displays a menu with options for resuming, opening settings, or quitting.

### **4. Settings**
1. **Change Login**:
   - Opens a sheet for editing the current login.
   - Sends the updated login via `NetworkManager.updateLogin()`.
2. **Change Difficulty**:
   - Displays a confirmation dialog for selecting a difficulty level.
   - Sends the updated difficulty to the backend with `NetworkManager.setDifficulty()`.
3. **Switch User**:
   - Shows a confirmation dialog for switching users.
   - Navigates back to `LoginView` on confirmation.

### **5. Leaderboard**
1. Fetches leaderboard data from the backend using `NetworkManager.fetchLeaderboard()`.
2. Dynamically displays the top players in a list format, highlighting the top 3 with medals.

---

## **How Components Interconnect**
- **Views** leverage **PlayerDataManager** for state and call **NetworkManager** for backend actions.
- **PlayerDataManager** maintains app-wide state and is updated dynamically based on user actions and network responses.
- **NetworkManager** ensures seamless communication with the backend, updating the app's state and handling errors gracefully.
