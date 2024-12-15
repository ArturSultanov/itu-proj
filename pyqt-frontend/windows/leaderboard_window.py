import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtSvg import QSvgWidget

class LeaderboardScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Leaderboard")

        self.main_layout = QHBoxLayout()

        self.tmp_layout = QVBoxLayout()
        self.leader_layout = QVBoxLayout()
        self.leader_layout.setContentsMargins(100, 200, 0, 0)
        
        self.update_leaderboard()
        self.tmp_layout.addLayout(self.leader_layout)
        
        back_layout = QHBoxLayout()
        self.back_btn = QPushButton(self)
        self.back_btn.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.back_btn.setText("Back")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setStyleSheet("margin-left: 70px;")
        self.back_btn.setIconSize(QSize(50, 50))
        self.back_btn.clicked.connect(self.on_back_button_click)
        self.back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.tmp_layout.addLayout(back_layout)
        self.main_layout.addLayout(self.tmp_layout)
        self.right_img = QLabel(self)
        self.right_img.setPixmap(QPixmap("assets/icons/screen_pic/leaderboard_pic.png"))
        self.right_img.setObjectName("difficultyPic")
        self.main_layout.addWidget(self.right_img, alignment=Qt.AlignRight | Qt.AlignBottom)
        self.setLayout(self.main_layout)

    def on_back_button_click(self):
        self.controller.show_main_menu()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                nested_layout = item.layout()
                if nested_layout is not None:
                    self.clear_layout(nested_layout)

    def update_leaderboard(self):
        players = self.controller.get_leaderboard_data(limit=5)
        self.clear_layout(self.leader_layout)
        
        for player in players:
            user_layout = QHBoxLayout()
            user_layout.setAlignment(Qt.AlignLeft)

            icon = QSvgWidget("assets/icons/user_icon.svg")
            icon.setObjectName("userIcon")
            icon.setFixedSize(70, 80)
            user_layout.addWidget(icon, alignment=Qt.AlignLeft)

            user_input_layout = QVBoxLayout()
            user_input_layout.setContentsMargins(40,0,0,0)

            name_score_layout = QHBoxLayout()
            name_label = QLabel(player['login'])
            name_label.setFixedHeight(50)
            name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            score_label = QLabel(str(player['highest_score']))
            score_label.setFixedHeight(50)
            score_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            name_score_layout.addWidget(name_label)
            name_score_layout.addWidget(score_label)
            user_input_layout.addLayout(name_score_layout)

            userpic = QLabel()
            userpic.setPixmap(QPixmap("assets/icons/underscore.png"))
            userpic.setFixedHeight(10)
            user_input_layout.addWidget(userpic)
            user_layout.addLayout(user_input_layout)
            self.leader_layout.addLayout(user_layout)