# ------------------------------------------------------------
# Author: Tatiana Fedorova (xfedor14)
# Subject: ITU
# Year: 2024
# ------------------------------------------------------------

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class MainMenuScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Main Menu")
        main_layout = QVBoxLayout()

        # add side image
        self.right_img = QLabel(self)
        self.right_img.setPixmap(QPixmap("assets/icons/screen_pic/main_pic.png")) 
        self.right_img.setObjectName("mainPic")
        main_layout.addWidget(self.right_img, alignment=Qt.AlignHCenter)

        # add welcome label
        self.label = QLabel("Hi, Player!", self)
        self.label.setObjectName("welcomeTextLabel")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.mousePressEvent = self.on_username_label_click
        main_layout.addWidget(self.label, alignment=Qt.AlignHCenter)

        # add menu buttons
        self.new_game_btn = QPushButton("New Game", self)
        self.new_game_btn.clicked.connect(self.on_new_game_button_click)
        main_layout.addWidget(self.new_game_btn)

        self.continue_btn = QPushButton("Continue", self)
        self.continue_btn.clicked.connect(self.on_continue_button_click)
        main_layout.addWidget(self.continue_btn)

        self.settings_btn = QPushButton("Settings", self)
        self.settings_btn.clicked.connect(self.on_settings_button_click)
        main_layout.addWidget(self.settings_btn)

        self.leaderboard_btn = QPushButton("Leaderboard", self)
        self.leaderboard_btn.setObjectName("leaderBtn")
        self.leaderboard_btn.clicked.connect(self.on_leaderboard_button_click)
        main_layout.addWidget(self.leaderboard_btn)

        # add quit button
        self.quit_btn = QPushButton("Quit Game", self)
        self.quit_btn.setObjectName("quitBtn")
        self.quit_btn.clicked.connect(self.controller.quit_game)
        main_layout.addWidget(self.quit_btn)

        # spacer to push the buttons towards the top + centering them
        spacer_bottom = QSpacerItem(20, 140, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        self.setLayout(main_layout)

    # update welcome message with player name
    def update_player_info(self, player_name):
        self.label.setText(f"Hi, {player_name}!")

    # start a new game
    def on_new_game_button_click(self):
        self.controller.show_game_screen()

    # continue the current game
    def on_continue_button_click(self):
        self.controller.window.setCurrentWidget(self.controller.game_screen)

    # go to settings screen
    def on_settings_button_click(self):
        self.controller.show_settings()

    # show leaderboard
    def on_leaderboard_button_click(self):
        self.controller.show_leaderboard()

    # ask to switch players
    def on_username_label_click(self, event):
        parent_widget = self.window().window()
        msg = QMessageBox(parent_widget)
        msg.setWindowTitle("Switch Player")
        msg.setText("Do you really want to switch players?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        msg.setStyleSheet("""
            QLabel {
                font-size: 18pt;
            }
            QPushButton {
                min-width: 200px;
                min-height: 60px;
                font-size: 20pt;
            }
        """)

        # position the message box
        main_geometry = parent_widget.geometry()
        msg.move(
            main_geometry.x() + 380,
            main_geometry.y() + 400
        )

        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            self.controller.show_login_screen()