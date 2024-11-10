from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

import requests

class MainWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 600, 500)

        # Main layout content
        main_layout = QWidget()
        main_vbox = QVBoxLayout()

        
        main_vbox.addWidget(QLabel("Welcome to the main window!"))
        # Button to start a new game
        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(self.start_new_game)
        main_vbox.addWidget(new_game_button)

        main_layout.setLayout(main_vbox)

        return main_layout

    def start_new_game(self):
        # When the button is clicked, switch to the game window
        self.controller.show_game()
