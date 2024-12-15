from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

class PaletteScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Color Palette")

        self.selected_icon = QIcon("assets/icons/right_icon.svg")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(80, 280, 0, 0)

        difficulty_layout = QVBoxLayout()

        self.mono_btn = QPushButton("Monochromacy")
        self.mono_btn.setIconSize(QSize(50, 50))
        self.mono_btn.clicked.connect(lambda: self.set_palette("monochromacy"))
        difficulty_layout.addWidget(self.mono_btn, alignment=Qt.AlignLeft)

        self.normal_btn = QPushButton("Normal")
        self.normal_btn.setIconSize(QSize(50, 50))
        self.normal_btn.clicked.connect(lambda: self.set_palette("normal"))
        difficulty_layout.addWidget(self.normal_btn, alignment=Qt.AlignLeft)

        main_layout.addLayout(difficulty_layout)

        self.right_img = QLabel(self)
        self.right_img.setPixmap(QPixmap("assets/icons/screen_pic/palette_pic.png"))
        self.right_img.setObjectName("difficultyPic")
        main_layout.addWidget(self.right_img, alignment=Qt.AlignRight)

        back_layout = QHBoxLayout()
        self.back_btn = QPushButton(self)
        self.back_btn.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.back_btn.setText("Back")
        self.back_btn.setStyleSheet("margin-bottom: 34px;")
        self.back_btn.setIconSize(QSize(50, 50))
        self.back_btn.clicked.connect(self.on_back_button_click)
        self.back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)
        main_layout.addLayout(back_layout)

        self.setLayout(main_layout)

        self.clear_all_icons()

    def on_back_button_click(self):
        self.controller.show_settings()

    def clear_all_icons(self):
        self.mono_btn.setIcon(QIcon())
        self.normal_btn.setIcon(QIcon())

    def set_palette(self, palette_value: str):
        self.clear_all_icons()
        if palette_value == "monochromacy":
            monochrome_qss = self.controller.original_qss.replace("#FFE500", "#888888")
            self.controller.apply_global_style(monochrome_qss)
            self.controller.current_theme = "monochromacy"
            self.mono_btn.setIcon(self.selected_icon)

            self.controller.game_screen.update_grid(
                self.controller.game_screen.rows, 
                self.controller.game_screen.cols,
                self.controller.game_screen.generate_sample_items(
                    self.controller.game_screen.rows, 
                    self.controller.game_screen.cols
                )
            )

        elif palette_value == "normal":
            self.controller.apply_global_style(self.controller.original_qss)
            self.controller.current_theme = "normal"
            self.normal_btn.setIcon(self.selected_icon)

            self.controller.game_screen.update_grid(
                self.controller.game_screen.rows, 
                self.controller.game_screen.cols,
                self.controller.game_screen.generate_sample_items(
                    self.controller.game_screen.rows, 
                    self.controller.game_screen.cols
                )
            )

