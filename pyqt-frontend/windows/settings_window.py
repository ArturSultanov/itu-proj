# ------------------------------------------------------------
# Author: Tatiana Fedorova (xfedor14)
# Subject: ITU
# Year: 2024
# ------------------------------------------------------------

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtSvg import QSvgWidget

class SettingsScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Settings")

        main_layout = QVBoxLayout()

        # add setting buttons
        self.palette_btn = QPushButton("Color palette", self)
        self.palette_btn.setObjectName("paletteBtn")
        self.palette_btn.clicked.connect(self.on_palette_button_click)
        main_layout.addWidget(self.palette_btn, alignment=Qt.AlignLeft)

        self.difficulty_btn = QPushButton("Difficulty level", self)
        self.difficulty_btn.setObjectName("leftBtn")
        self.difficulty_btn.clicked.connect(self.on_difficulty_button_click)
        main_layout.addWidget(self.difficulty_btn, alignment=Qt.AlignLeft)

        self.change_btn = QPushButton("Change name", self)
        self.change_btn.setObjectName("leftBtn")
        self.change_btn.clicked.connect(self.on_change_button_click)
        main_layout.addWidget(self.change_btn, alignment=Qt.AlignLeft)
        
        # add settings image
        image_layout = QVBoxLayout()
        self.right_img = QLabel(self)
        self.right_img.setPixmap(QPixmap("assets/icons/screen_pic/settings_pic.png")) 
        self.right_img.setObjectName("settingPic")
        image_layout.addWidget(self.right_img, alignment=Qt.AlignRight)
        main_layout.addLayout(image_layout)

        # add back button
        back_layout = QHBoxLayout()
        self.back_btn = QPushButton(self)
        self.back_btn.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.back_btn.setText("Back")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setStyleSheet("margin-left: 70px;")
        self.back_btn.setIconSize(QSize(50, 50))
        self.back_btn.clicked.connect(self.on_back_button_click)
        self.back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)

        main_layout.addLayout(back_layout)
        self.setLayout(main_layout)

    # go to color palette screen
    def on_palette_button_click(self):
        self.controller.show_palette()

    # go to difficulty level screen
    def on_difficulty_button_click(self):
        self.controller.show_difficulty()

    # go to change name screen
    def on_change_button_click(self):
        self.controller.show_change()

    # go back to main menu
    def on_back_button_click(self):
        self.controller.show_main_menu()
