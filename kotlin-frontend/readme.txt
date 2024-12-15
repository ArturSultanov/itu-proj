androidApp
├── build.gradle.kts
└── src
    └── main
        ├── AndroidManifest.xml
        ├── java
        │ └── com
        │     └── example
        │         └── myapplication
        │             └── android
        │                 ├── Buttons.kt            // Predefined buttons for Screens
        │                 ├── MainActivity.kt       // Main Entry Point
        │                 ├── MyApplicationTheme.kt // Theme for the App, colors, typography
        │                 ├── NavigationGraph.kt    // Navigation Graph for the App, to ensure the flow of the app
        │                 ├── api       // API for the Game, wraps the HTTP calls
        │                 │ ├── ApiException.kt     // Custom Exception for API
        │                 │ ├── Game.kt             // Game Instance, to store the state of the game
        │                 │ ├── GameApi.kt          // Game API, to interact with the Game
        │                 │ ├── HTTP.kt             // HTTP Client, to make HTTP calls
        │                 │ ├── entries             // Data Classes for API
        │                 │ │ ├── BoardEntry.kt
        │                 │ │ ├── LeaderboardEntry.kt
        │                 │ │ └── UpdateEntry.kt
        │                 │ └── responses           // Data Classes for API Responses
        │                 │     ├── LoginResponse.kt
        │                 │     └── MoveResponse.kt
        │                 └── screen                // Particular Screen of the App
        │                     ├── AppScreen.kt              // Base Screen for the App, bone-fish for all the screens
        │                     ├── GameOverScreen.kt         // Game Over Screen, to show the result of the game
        │                     ├── GridElement.kt            // Grid Element, to represent the element of the grid
        │                     ├── LeaderBoardScreen.kt      // Leaderboard Screen, to show the leaderboard
        │                     ├── LoginScreen.kt            // Login Screen, to login to the game
        │                     ├── PauseScreen.kt            // Pause Screen, to pause the game
        │                     ├── PlaygroundScreen.kt       // Playground Screen, to play the game
        │                     ├── SettingsScreen.kt         // Settings Screen, to change the settings of the game
        │                     └── UserProfileScreen.kt      // User Profile, to show the user profile
        └── res  // Resources for the App
            ├── values
            │ └── styles.xml
            └── xml
                └── network_security_config.xml
