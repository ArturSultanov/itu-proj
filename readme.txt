Tile Match Game 

Each member of the team build the own FE in the individual technogoly.
The directories are named by technogoly that was used for implementation.

tkinter-frontend/   Author: Lilit Movsesian (xmovse00)
swiftui-frontend/   Author: Artur Sultanov (xsutla01)
pyqt-frontend/      Author: Tatiana Fedorova (xfedor14)
kotlin-frontend/    Author: Kirill Shchetiniuk (xshche05)

01_xfedor14_xmovse00_xshche05_xsulta01_source/
│
├── backend/...                                                     Unified BE for all FEs
│
├── readme.txt
│
├── tkinter-frontend/                                               Author: xmovse00
│   ├── src/
│   │   ├── __init__.py
│   │   ├── login_page.py
│   │   ├── menu_page.py
│   │   ├── game_page.py
│   │   ├── change_login_page.py
│   │   ├── difficulty_page.py
│   │   ├── leader_page.py
│   │   ├── pause_page.py
│   │   └── settings_page.py
│   ├── main.py
│   ├── README.md
│   ├── requirements.txt
│   └── assets/
│       └── images/
│           └── ...
│
├── swiftui-frontend/                                               Author: xsulta01
│   ├── Assets.xcassets                                             Application assests
│   │   ├── AccentColor.colorset    
│   │   └── AppIcon.appiconset
│   │       ├── 1024.png
│   │       ├── 128.png
│   │       └── ...
|   ├── Info.plist                                                  Metadata for the app
│   ├── Banners
│   │   ├── BannerManager.swift                                     Manages to display in-app notification
│   │   └── NotificationBanner.swift                                Predefined view for notification
│   ├── Models                          
│   │   └── ModelsManager.swift                                     Models for BE API requests
│   ├── Network                         
│   │   └── NetworkManager.swift                                    Methods for BE API interaction
│   ├── Styles
│   │   ├── ButtonStyle.swift                                       Predefined buttons styles
│   │   ├── ColorPalette.swift                                      Normal and adaptive color palettes
│   │   └── PaletteManager.swift                                    Manager to switch palettes
│   ├── Views
│   │   ├── GameBoardView.swift                                     Game board with the grid of gems view
│   │   ├── GemView.swift                                           Represents individual gem
│   │   ├── LeaderBoardView.swift                                   Top players leaderboard view
│   │   ├── LoginView.swift                                         User login view
│   │   ├── MainMenuView.swift                                      Main navigation menu view
│   │   └── SettingsView.swift                                      App settings view
|   ├── swiftui_frontend.entitlements                               Defines the app permissions and capabilities 
│   ├── swiftui_frontendApp.swift                                   The entry point of the app
|   ├── swiftui-frontend.xcodeproj                                  App build settings, dependencies, and target definitions
|   │   ├── project.pbxproj
|   │   ├── project.xcworkspace
│   │   └── ...
│   └── README.md
│
├── kotlin-frontend                                                 Author: xshche05
│   ├── androidApp
│   │   ├── build.gradle.kts
│   │   └── src
│   │       └── main
│   │           ├── AndroidManifest.xml
│   │           ├── java.com.expample.myapplication.android
│   │           │   ├── api
│   │           │   │   ├── ApiException.kt             Custom Exception for API
│   │           │   │   ├── entries                     Data Classes for API
│   │           │   │   │   ├── BoardEntry.kt
│   │           │   │   │   ├── LeaderboardEntry.kt
│   │           │   │   │   └── UpdateEntry.kt
│   │           │   │   ├── GameApi.kt                  Game API, to interact with the Game
│   │           │   │   ├── Game.kt                     Game Instance, to store the state of the game
│   │           │   │   ├── HTTP.kt                     HTTP Client, to make HTTP calls
│   │           │   │   └── responses                   Data Classes for API Responses
│   │           │   │       ├── LoginResponse.kt
│   │           │   │       └── MoveResponse.kt
│   │           │   ├── Buttons.kt                      Predefined buttons for Screens
│   │           │   ├── MainActivity.kt                 Main Entry Point
│   │           │   ├── MyApplicationTheme.kt           Theme for the App, colors, typography
│   │           │   ├── NavigationGraph.kt              Navigation Graph for the App, to ensure the flow of the app
│   │           │   └── screen                          Particular Screen of the App
│   │           │       ├── AppScreen.kt                Base Screen for the App, bone-fish for all the screens
│   │           │       ├── GameOverScreen.kt           Game Over Screen, to show the result of the game
│   │           │       ├── GridElement.kt              Grid Element, to represent the element of the grid
│   │           │       ├── LeaderBoardScreen.kt        Leaderboard Screen, to show the leaderboard
│   │           │       ├── LoginScreen.kt              Login Screen, to login to the game
│   │           │       ├── PauseScreen.kt              Pause Screen, to pause the game
│   │           │       ├── PlaygroundScreen.kt         Playground Screen, to play the game
│   │           │       ├── SettingsScreen.kt           Settings Screen, to change the settings of the game
│   │           │       └── UserProfileScreen.kt        User Profile, to show the user profile
│   │           └── res                                                 Resources for the App
│   │               ├── values
│   │               │   └── styles.xml
│   │               └── xml
│   │                   └── network_security_config.xml
│   └── ...
│