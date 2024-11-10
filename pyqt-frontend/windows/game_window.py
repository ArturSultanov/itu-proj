from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class GameWindow1(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Game Window")
        self.setGeometry(200, 200, 600, 500)

        # Game window content (simple grid for example)
        game_layout = QWidget()
        game_vbox = QVBoxLayout()

        game_vbox.addWidget(QLabel("This is the game screen!"))

        # Button to go back to main menu
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.confirm_clicked)  # Close the game window to return to main
        game_vbox.addWidget(back_button)

        game_layout.setLayout(game_vbox)

        # Return the layout to be added to the stacked widget later
        return game_layout

    def confirm_clicked(self):
        self.controller.show_main()