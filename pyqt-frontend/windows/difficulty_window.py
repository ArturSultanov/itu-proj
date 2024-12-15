# ------------------------------------------------------------
# Author: Tatiana Fedorova (xfedor14)
# Subject: ITU
# Year: 2024
# ------------------------------------------------------------

import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from enum import Enum

class Difficulty(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"

class DifficultyScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Difficulty level")

        self.selected_icon = QIcon("assets/icons/right_icon.svg")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(80, 280, 0, 0)

        difficulty_layout = QVBoxLayout()

        # create easy button
        self.easy_button = QPushButton("Easy")
        self.easy_button.setIcon(self.selected_icon)
        self.easy_button.setIconSize(QSize(50, 50))
        self.easy_button.clicked.connect(lambda: self.set_difficulty(Difficulty.EASY))
        difficulty_layout.addWidget(self.easy_button, alignment=Qt.AlignLeft)

        # create normal button
        self.normal_button = QPushButton("Normal")
        self.normal_button.setIcon(self.selected_icon)
        self.normal_button.setIconSize(QSize(50, 50))
        self.normal_button.clicked.connect(lambda: self.set_difficulty(Difficulty.NORMAL))
        difficulty_layout.addWidget(self.normal_button, alignment=Qt.AlignLeft)

        # create hard button
        self.hard_button = QPushButton("Hard")
        self.hard_button.setIcon(self.selected_icon)
        self.hard_button.setIconSize(QSize(50, 50))
        self.hard_button.clicked.connect(lambda: self.set_difficulty(Difficulty.HARD))
        difficulty_layout.addWidget(self.hard_button, alignment=Qt.AlignLeft)

        main_layout.addLayout(difficulty_layout)

        # add right side image
        self.right_img = QLabel(self)
        self.right_img.setPixmap(QPixmap("assets/icons/screen_pic/difficulty_pic.png")) 
        self.right_img.setObjectName("difficultyPic")
        main_layout.addWidget(self.right_img, alignment=Qt.AlignRight)
        back_layout = QHBoxLayout()

        # create back button
        self.back_btn = QPushButton(self)
        self.back_btn.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.back_btn.setText("Back")
        self.back_btn.setStyleSheet("margin-bottom: 34px; ")
        self.back_btn.setIconSize(QSize(50, 50))
        self.back_btn.clicked.connect(self.on_back_button_click)
        self.back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)
        main_layout.addLayout(back_layout)
        self.setLayout(main_layout)


        # clear icons initially
        self.clear_all_icons()

    # go back to settings screen
    def on_back_button_click(self):
        self.controller.show_settings()

    # remove all icons from buttons
    def clear_all_icons(self):
        self.easy_button.setIcon(QIcon())
        self.normal_button.setIcon(QIcon())
        self.hard_button.setIcon(QIcon())

    # set the selected difficulty
    def set_difficulty(self, difficulty: Difficulty):
        set_diff_url = "http://localhost:8000/settings/set_difficulty"
        data = {"difficulty": difficulty.value}
        try:
            response = requests.patch(set_diff_url, json=data)
            if response.status_code == 200:
                print(response.json())

                # delete existing game
                delete_game_url = "http://localhost:8000/menu/delete_game"
                del_response = requests.delete(delete_game_url)
                if del_response.status_code == 200:
                    print(del_response.json())

                    # update icons to show selection
                    self.clear_all_icons()
                    if difficulty == Difficulty.EASY:
                        self.easy_button.setIcon(self.selected_icon)
                    elif difficulty == Difficulty.NORMAL:
                        self.normal_button.setIcon(self.selected_icon)
                    elif difficulty == Difficulty.HARD:
                        self.hard_button.setIcon(self.selected_icon)

                else:
                    print(f"Error deleting game: {del_response.status_code} - {del_response.text}")

            else:
                print(f"Error setting difficulty: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception occurred: {e}")
