from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QPixmap

class LoginScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Login")

        self.layout = QVBoxLayout()

        # Основной горизонтальный макет
        main_layout = QHBoxLayout()

        # Левый блок с полем ввода и подчеркиванием
        left_layout = QVBoxLayout()

        # Текстовая метка "Enter your name"
        self.label = QLabel("Enter your name")
        self.label.setObjectName("nameTextLabel")
        left_layout.addWidget(self.label)

        # Иконка пользователя
        self.icon = QSvgWidget("assets/icons/user_icon.svg")
        self.icon.setObjectName("userIcon")
        self.icon.setFixedSize(90, 100)
        left_layout.addWidget(self.icon)

        # Поле ввода
        self.username_input = QLineEdit(self)
        self.username_input.setObjectName("usernameInput")
        left_layout.addWidget(self.username_input)

        # Картинка под полем ввода
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("assets/icons/underscore.png"))
        self.image_label.setObjectName("underscoreIcon")
        self.image_label.setFixedHeight(10)
        left_layout.addWidget(self.image_label)

        # Добавляем левый блок в основной горизонтальный макет
        main_layout.addLayout(left_layout)

        # Добавляем Spacer между блоками
        spacer = QSpacerItem(50, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        main_layout.addItem(spacer)

        # Картинка в правой части экрана
        self.right_image = QLabel(self)
        self.right_image.setPixmap(QPixmap("assets/icons/login_pic.png")) 
        self.right_image.setObjectName("loginPic")
        main_layout.addWidget(self.right_image)

        # Добавляем основной горизонтальный макет в основной вертикальный
        self.layout.addLayout(main_layout)

        # Кнопка подтверждения
        self.login_button = QPushButton("Confirm", self)
        self.login_button.setObjectName("confirmBtn")
        self.login_button.clicked.connect(self.on_login_button_click)
        self.layout.addWidget(self.login_button)

        # Кнопка выхода
        self.quit_button = QPushButton("Quit Game", self)
        self.quit_button.setObjectName("quitBtn")
        self.quit_button.clicked.connect(self.controller.quit_game)
        self.layout.addWidget(self.quit_button)

        # Устанавливаем основной макет
        self.setLayout(self.layout)

    def on_login_button_click(self):
        username = self.username_input.text()
        
        # Запрос к серверу
        response = self.controller.login(username)
        if response:
            self.controller.show_main_menu()
        else:
            self.label.setText("Login failed. Try again")
