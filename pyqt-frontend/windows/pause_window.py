from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon 

class PauseScreen(QWidget):
    def __init__(self, controller, score, moves_left):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Pause")

        self.main_layout = QHBoxLayout()
        self.layout = QVBoxLayout()

        score_layout = QVBoxLayout()
        score_top_layout = QHBoxLayout()
        self.main_layout.addSpacing(350)
        self.icon = QSvgWidget("assets/icons/coin_icon.svg", self)

        self.icon.setFixedSize(80, 70)
        score_top_layout.addWidget(self.icon, alignment=Qt.AlignVCenter )
        # Вместо "0" подставляем аргумент score
        self.score_text_label = QLabel(str(score), self)
        self.score_text_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        score_top_layout.addWidget(self.score_text_label)
        score_layout.addLayout(score_top_layout)

        self.underpic = QLabel(self)
        self.underpic.setPixmap(QPixmap("assets/icons/underscore_small_icon.png"))
        self.underpic.setAlignment(Qt.AlignHCenter | Qt.AlignRight)
        self.underpic.setContentsMargins(20, 0, 0, 0)
        score_layout.addWidget(self.underpic)
        score_layout.setContentsMargins(0, 20, 0, 0)
        self.main_layout.addLayout(score_layout)

        self.main_layout.addSpacing(150)

        energy_layout = QVBoxLayout()
        energy_top_layout = QHBoxLayout()
        self.energy_icon = QSvgWidget("assets/icons/energy_icon.svg", self)
        self.energy_icon.setFixedSize(40, 70)
        energy_top_layout.addWidget(self.energy_icon)
        # Вместо "0" подставляем аргумент moves_left
        self.energy_text_label = QLabel(str(moves_left), self)
        self.energy_text_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        energy_top_layout.addWidget(self.energy_text_label)
        energy_layout.addLayout(energy_top_layout)
        self.en_underpic = QLabel(self)
        self.en_underpic.setPixmap(QPixmap("assets/icons/underscore_small_icon.png"))
        self.en_underpic.setAlignment(Qt.AlignHCenter | Qt.AlignRight)
        energy_layout.addWidget(self.en_underpic)
        energy_layout.setContentsMargins(0, 20, 0, 0)
        self.main_layout.addLayout(energy_layout)

        self.main_layout.addWidget(self.score_text_label)
        self.main_layout.addWidget(self.energy_text_label)

        self.layout.addLayout(self.main_layout)

        img = QPixmap("assets/icons/pause_pic.png")
        scaled_img = img.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img = QLabel(self)
        self.img.setPixmap(scaled_img)
        self.img.setObjectName("pausePic")
        self.layout.addWidget(self.img, alignment=Qt.AlignHCenter)
        self.layout.addStretch()  # Остаток пространства снизу, приподнимает картинку

        play_layout = QHBoxLayout()
        self.play_btn = QPushButton(self)
        self.play_btn.setIcon(QIcon("assets/icons/play_icon.svg"))
        self.play_btn.setText("Play")
        self.play_btn.setObjectName("playBtn")
        self.play_btn.setIconSize(QSize(50, 50))
        self.play_btn.clicked.connect(self.on_play_button_click)
        self.play_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        play_layout.addWidget(self.play_btn, alignment=Qt.AlignHCenter)
        play_layout.setContentsMargins(0, 30, 0, 20)
        self.layout.addLayout(play_layout)

        back_layout = QHBoxLayout()
        self.back_btn = QPushButton(self)
        self.back_btn.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.back_btn.setText("Back")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setIconSize(QSize(50, 50))
        self.back_btn.clicked.connect(self.on_back_button_click)
        
        self.back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        back_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)
        self.layout.addLayout(back_layout)

        self.setLayout(self.layout)

    def on_play_button_click(self):
        self.controller.window.setCurrentWidget(self.controller.game_screen)

    def on_back_button_click(self):
        self.controller.show_main_menu()
