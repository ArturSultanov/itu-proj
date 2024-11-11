# frontend/view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit

class LoginScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Login")

        self.layout = QVBoxLayout()

        self.label = QLabel("Please log in")
        self.layout.addWidget(self.label)

        self.username_input = QLineEdit(self)
        
        self.layout.addWidget(self.username_input)
        
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.on_login_button_click)
        
        self.layout.addWidget(self.login_button)
        
        self.setLayout(self.layout)

    def on_login_button_click(self):
        username = self.username_input.text()
        
        # Send login request to backend
        response = self.controller.login(username)
        if response:
            self.controller.show_main_menu()  # Pass player name to the main menu
        else:
            self.label.setText("Login failed! Try again.")
