Tile Match Game 

Each member of the team build the own FE in the individual technogoly.
The directories are named by technogoly that was used for implementation.

tkinter-frontend    Author: Lilit Movsesian (xmovse00)
swiftui-frontend    Author: Artur Sultanov (xsutla01)
pyqt-frontend       Author: Tatiana Fedorova (xfedor14)

01_xfedor14_xmovse00_xshche05_xsulta01_source/
│
├── backend/...                         Unified BE for all FEs
├── readme.txt
├── tkinter-frontend/                   Author: xmovse00
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
├── swiftui-frontend/                   Author: xsulta01
│   ├── Assets.xcassets                 Application assests
│   │   ├── AccentColor.colorset    
│   │   └── AppIcon.appiconset
│   │       ├── 1024.png
│   │       ├── 128.png
│   │       └── ...
│   ├── Banners
│   │   ├── BannerManager.swift         Manages to display in-app notification
│   │   └── NotificationBanner.swift    Predefined view for notification
│   ├── Models                          
│   │   └── ModelsManager.swift         Models for BE API requests
│   ├── Network                         
│   │   └── NetworkManager.swift        Methods for BE API interaction
│   ├── Styles
│   │   ├── ButtonStyle.swift           Predefined buttons styles
│   │   ├── ColorPalette.swift          Normal and adaptive color palettes
│   │   └── PaletteManager.swift        Manager to switch palettes
│   ├── Views
│   │   ├── GameBoardView.swift         Game board with the grid of gems view
│   │   ├── GemView.swift               Represents individual gem
│   │   ├── LeaderBoardView.swift       Top players leaderboard view
│   │   ├── LoginView.swift             User login view
│   │   ├── MainMenuView.swift          Main navigation menu view
│   │   └── SettingsView.swift          App settings view
│   ├── swiftui_frontendApp.swift       The entry point of the app
│   └── README.md
│
