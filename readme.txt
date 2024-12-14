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
│   │       ├── 16.png
│   │       ├── 256.png
│   │       └── ...
│   ├── Banners                         In-app notifications logic
│   │   ├── BannerManager.swift
│   │   └── NotificationBanner.swift
│   ├── Models                          Models for BE API requests
│   │   └── ModelsManager.swift
│   ├── Network                         Methofs for BE API interaction
│   │   └── NetworkManager.swift
│   ├── Styles                          Styles for GUI parts
│   │   ├── ButtonStyle.swift
│   │   ├── ColorPalette.swift
│   │   └── PaletteManager.swift
│   ├── Views                           Screens of application
│   │   ├── GameBoardView.swift
│   │   ├── GemView.swift
│   │   ├── LeaderBoardView.swift
│   │   ├── LoginView.swift
│   │   ├── MainMenuView.swift
│   │   └── SettingsView.swift
│   ├── swiftui_frontendApp.swift       The entry point of the app
│   └── README.md
│
