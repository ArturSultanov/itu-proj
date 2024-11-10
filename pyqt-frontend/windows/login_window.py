from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import requests
import time

class LoginWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 600, 500)

        # Login layout
        login_layout = QWidget()
        login_vbox = QVBoxLayout()

        label = QLabel("Enter your name")
        label.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Player1")

        

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.confirm_clicked)

        quit_button = QPushButton("Quit Game")
        quit_button.clicked.connect(self.close)

        login_vbox.addWidget(label)
        login_vbox.addWidget(self.name_input)
        login_vbox.addWidget(confirm_button)
        login_vbox.addWidget(quit_button)

        login_layout.setLayout(login_vbox)

        # Return the layout to be added to the stacked widget later
        return login_layout

    def confirm_clicked(self):
        player_name = self.name_input.text()
        if player_name:
            print(f"Player Name: {player_name}")
            url = "http://localhost:8000/login"
            headers = {
                "accept": "application/json",
            }
            response = requests.get(url, headers=headers, params={"login": player_name})
            
            url = "http://localhost:8000/utils/current_player"
            headers = {
                "accept": "application/json",
            }
            response = requests.get(url, headers=headers)
            login = response.json().get("login")
            print(f"Back Player Name: {login}")

            self.controller.show_main()  # Show main window layout
