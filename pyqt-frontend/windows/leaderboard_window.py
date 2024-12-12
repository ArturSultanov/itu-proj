from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtSvg import QSvgWidget

class LeaderboardScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Leaderboard")

        main_layout = QVBoxLayout()




        back_layout = QHBoxLayout()
        self.back_btn = QPushButton(self)
        self.back_btn.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.back_btn.setText("Back")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setIconSize(QSize(50, 50))
        self.back_btn.clicked.connect(self.on_back_button_click)
        self.back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        back_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)
        main_layout.addLayout(back_layout)

        self.setLayout(main_layout)

    def on_back_button_click(self):
        self.controller.show_main_menu()
