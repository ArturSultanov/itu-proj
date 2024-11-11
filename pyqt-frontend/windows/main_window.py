from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class MainMenuScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Main Menu")

        # Set the window size (you can adjust it if needed)
        self.resize(600, 400)

        # Create the layout
        self.layout = QVBoxLayout()

        # Create the "Hi, player_name" text label
        self.greeting_label = QLabel("Hi, Player!", self)
        self.layout.addWidget(self.greeting_label, alignment=Qt.AlignCenter)

        # Add spacer to center the widgets vertically
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        # Create buttons
        self.new_game_button = QPushButton("New Game", self)
        self.new_game_button.clicked.connect(self.on_new_game_button_click)
        self.layout.addWidget(self.new_game_button)

        self.continue_button = QPushButton("Continue", self)
        self.continue_button.clicked.connect(self.on_continue_button_click)
        self.layout.addWidget(self.continue_button)

        self.settings_button = QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.on_settings_button_click)
        self.layout.addWidget(self.settings_button)

        self.leaderboard_button = QPushButton("Leaderboard", self)
        self.leaderboard_button.clicked.connect(self.on_leaderboard_button_click)
        self.layout.addWidget(self.leaderboard_button)

        # Add another spacer to push the buttons towards the top, centering them
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer_bottom)

        # Set the layout for the main window
        self.setLayout(self.layout)

    def update_player_info(self, player_name):
        """Update the UI with the current player's name."""
        self.greeting_label.setText(f"Hi, {player_name}!")

    def on_new_game_button_click(self):
        """Handle the 'New Game' button click."""
        print("Starting a new game...")
        self.controller.show_game_screen()

    def on_continue_button_click(self):
        """Handle the 'Continue' button click."""
        print("Continuing the game...")
        # Implement continue game functionality here

    def on_settings_button_click(self):
        """Handle the 'Settings' button click."""
        print("Opening settings...")
        # Implement settings screen functionality here

    def on_leaderboard_button_click(self):
        """Handle the 'Leaderboard' button click."""
        print("Opening leaderboard...")
        # Implement leaderboard functionality here
