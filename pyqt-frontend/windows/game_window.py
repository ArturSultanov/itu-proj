import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QPixmap, QIcon 
from utils.api_call import api_request

class GameScreen(QWidget):
    def __init__(self, controller, rows=5, cols=6):
        super().__init__()
        self.controller = controller

        self.rows = rows
        self.cols = cols
        self.cell_size = 100
        self.clicked_cells = []

        self.setWindowTitle("Game Screen")

        self.main_layout = QHBoxLayout()
        self.layout = QVBoxLayout()

        self.score_label = QLabel("Score: 0", self)
        self.moves_left_label = QLabel("Moves Left: 10", self)

        spacer = QSpacerItem(0, 150, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.main_layout.addItem(spacer)

        self.main_layout.addWidget(self.score_label, alignment=Qt.AlignHCenter)
        self.main_layout.addWidget(self.moves_left_label, alignment=Qt.AlignHCenter)
        self.layout.addLayout(self.main_layout)

        space_layout = QHBoxLayout()
        left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        space_layout.addItem(left_spacer)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        space_layout.addLayout(self.grid_layout)

        right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        space_layout.addItem(right_spacer)
        self.layout.addLayout(space_layout)

        # spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.layout.addItem(spacer_bottom)

        self.back_button = QPushButton("Back to Main Menu", self)
        self.back_button.clicked.connect(self.on_back_button_click)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
        self.update_grid(self.rows, self.cols, self.generate_sample_items(self.rows, self.cols))


    def update_grid(self, rows, cols, items):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for row in range(rows):
            for col in range(cols):
                item_type = items[row][col] if row < len(items) and col < len(items[row]) else 0
                grid_item = self.create_item_widget(item_type, row, col)
                self.grid_layout.addWidget(grid_item, row, col)

    def create_item_widget(self, item_type, row, col):
        button = QPushButton(self)
        button.setFixedSize(100, 100)  # Устанавливаем фиксированный размер кнопки
        icon = self.get_item_icon(item_type)
        button.setIcon(icon)
        button.setIconSize(button.size())  # Иконка занимает весь размер кнопки
        button.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))
        return button



    def get_item_icon(self, item_type):
        icon_map = {
            # 0: 'assets/icons/chicken_icon.png',
            0: 'assets/icons/lemon_icon.svg',
            # 1: 'assets/icons/chili_icon.png',
            1: 'assets/icons/donut_icon.png',
            2: 'assets/icons/cherry_icon.svg',
            # 4: 'assets/icons/rice_icon.png',
            4: 'assets/icons/star_icon.png',
            # 3: 'assets/icons/avo_icon.png',
            # 3: 'assets/icons/banana_icon.svg',
            3: 'assets/icons/beer_icon.png',
        }
        return QIcon(icon_map.get(item_type, 'assets/icons/banana.svg'))


    def generate_sample_items(self, rows, cols):
        import random
        types = [0, 1, 2, 3, 4]
        return [[random.choice(types) for _ in range(cols)] for _ in range(rows)]

    def cell_clicked(self, row, col):
        self.clicked_cells.append({"x": col, "y": row})
        print(f"Cell clicked at row {row}, column {col}")

        if len(self.clicked_cells) == 2:
            # Prepare data for backend
            data = {"gems": self.clicked_cells}
            self.send_move_to_backend(data)
            self.clicked_cells = []

    def send_move_to_backend(self, data):
        response = api_request("/board/swap_gems_fullboard", params=data, method="POST")
        print(response)
        self.update_score_and_moves(response["current_score"], response["moves_left"])
        self.update_grid(len(response["board_status"]), len(response["board_status"][0]), response["board_status"])

    def on_back_button_click(self):
        self.controller.show_main_menu()
    
    def update_score_and_moves(self, score, moves_left):
        self.score_label.setText(f"Score: {score}")
        self.moves_left_label.setText(f"Moves Left: {moves_left}")
    

