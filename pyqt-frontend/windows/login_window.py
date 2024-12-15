# ------------------------------------------------------------
# Author: Tatiana Fedorova (xfedor14)
# Subject: ITU
# Year: 2024
# ------------------------------------------------------------

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QPixmap

class LoginScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Login")
        
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 200, 0, 0)

        # add label for name input
        self.label = QLabel("Enter your name")
        self.label.setObjectName("nameTextLabel")
        left_layout.addWidget(self.label)

         # add user icon
        user_layout = QHBoxLayout()
        user_layout.setObjectName("userLayout")
        self.icon = QSvgWidget("assets/icons/user_icon.svg")
        self.icon.setObjectName("userIcon")
        self.icon.setFixedSize(70, 80)
        user_layout.addWidget(self.icon)
        user_input = QVBoxLayout()
        self.username = QLineEdit(self)
        self.username.setObjectName("usernameInput")
        self.username.textChanged.connect(self.check_username_length)
        user_input.addWidget(self.username)

        # add underscore image
        self.userpic = QLabel(self)
        self.userpic.setPixmap(QPixmap("assets/icons/underscore.png"))
        self.userpic.setObjectName("underscoreIcon")
        self.userpic.setFixedHeight(10)
        user_input.addWidget(self.userpic)
        user_layout.addLayout(user_input)

        # set margins for user input layout
        user_layout.setContentsMargins(110, 0, 0, 0)
        left_layout.addLayout(user_layout)

        # add confirm button
        self.login_btn = QPushButton("Confirm", self)
        self.login_btn.setObjectName("confirmBtn")
        self.login_btn.clicked.connect(self.on_login_button_click)
        left_layout.addWidget(self.login_btn)

        # add quit button
        self.quit_btn = QPushButton("Quit Game", self)
        self.quit_btn.setObjectName("quitBtn")
        self.quit_btn.clicked.connect(self.controller.quit_game)
        left_layout.addWidget(self.quit_btn)

        main_layout.addLayout(left_layout)

        # add right side image
        self.right_img = QLabel(self)
        self.right_img.setPixmap(QPixmap("assets/icons/screen_pic/login_pic.png")) 
        self.right_img.setObjectName("loginPic")
        main_layout.addWidget(self.right_img)

        self.setLayout(main_layout)

    # limit username to 10 characters
    def check_username_length(self):
        if len(self.username.text()) > 10:
            self.username.setText(self.username.text()[:10])
            self.show_warning("The login must contain 10 or fewer characters")

    # show a warning message box
    def show_warning(self, message):
        parent_widget = self.window().window()
        msg = QMessageBox(parent_widget)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
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
            main_geometry.x() + 200,
            main_geometry.y() + 400
        )
        msg.exec_()

    # handle login button click
    def on_login_button_click(self):
        username = self.username.text()
        if not username.strip():
            self.show_warning("Username cannot be empty.")
            return
        
        response = self.controller.login(username)
        if response:
            self.controller.show_main_menu()
        else:
            self.label.setText("Login failed. Try again")
