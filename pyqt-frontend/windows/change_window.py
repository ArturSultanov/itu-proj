# ------------------------------------------------------------
# Author: Tatiana Fedorova (xfedor14)
# Subject: ITU
# Year: 2024
# ------------------------------------------------------------

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

class ChangeScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Change")
        
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()

        # set margins for left layout
        left_layout.setContentsMargins(0, 200, 0, 0)

        # add label for new name
        self.label = QLabel("Your new name")
        self.label.setStyleSheet("margin-left: 110px;")
        left_layout.addWidget(self.label)
        user_layout = QHBoxLayout()
        user_layout.setObjectName("userLayout")

        # add user icon
        self.icon = QSvgWidget("assets/icons/user_icon.svg")
        self.icon.setObjectName("userIcon")
        self.icon.setFixedSize(70, 80)
        user_layout.addWidget(self.icon)
        user_input = QVBoxLayout()
        self.username = QLineEdit(self)
        self.username.setObjectName("usernameInput")
        user_input.addWidget(self.username)

        # add underscore image
        self.userpic = QLabel(self)
        self.userpic.setPixmap(QPixmap("assets/icons/underscore.png"))
        self.userpic.setObjectName("underscoreIcon")
        self.userpic.setFixedHeight(10)
        user_input.addWidget(self.userpic)
        user_layout.addLayout(user_input)

        # set margins for user layout
        user_layout.setContentsMargins(110, 0, 0, 0)
        left_layout.addLayout(user_layout)

        # add confirm button
        self.login_btn = QPushButton("Confirm", self)
        self.login_btn.setObjectName("confirmBtn")
        self.login_btn.clicked.connect(self.on_login_button_click)
        left_layout.addWidget(self.login_btn)

        # add back button
        self.back_btn = QPushButton(self)
        self.quit_btn = QPushButton("Back", self)
        self.back_btn.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.back_btn.setText("Back")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setStyleSheet("margin-left: 70px;")
        self.back_btn.setIconSize(QSize(50, 50))
        self.back_btn.clicked.connect(self.on_back_button_click)
        self.back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        left_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft | Qt.AlignBottom)
        main_layout.addLayout(left_layout)

        # add right side image
        self.right_img = QLabel(self)
        self.right_img.setPixmap(QPixmap("assets/icons/screen_pic/change_pic.png")) 
        main_layout.addWidget(self.right_img, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.setLayout(main_layout)

    # handle confirm button click
    def on_login_button_click(self):
        username = self.username.text()
        response = self.controller.login(username)
        if response:
            self.controller.show_main_menu()
        else:
            self.label.setText("Login failed. Try again")
            
    # handle back button click
    def on_back_button_click(self):
        self.controller.show_main_menu()