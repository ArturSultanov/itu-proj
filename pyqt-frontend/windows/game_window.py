import requests
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon 
from utils.api_call import api_request
from PyQt5.QtSvg import QSvgWidget

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

        score_layout = QVBoxLayout()
        score_top_layout = QHBoxLayout()
        self.main_layout.addSpacing(350)
        self.icon = QSvgWidget("assets/icons/coin_icon.svg", self)

        self.icon.setFixedSize(80, 70)
        score_top_layout.addWidget(self.icon, alignment=Qt.AlignVCenter )
        self.score_text_label = QLabel("0", self)
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
        self.energy_text_label = QLabel("0", self)
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

        space_layout = QHBoxLayout()
        left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        space_layout.addItem(left_spacer)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        space_layout.addLayout(self.grid_layout)

        right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        space_layout.addItem(right_spacer)
        self.layout.addLayout(space_layout)

        pause_layout = QHBoxLayout()
        self.pause_btn = QPushButton(self)
        self.pause_btn.setIcon(QIcon("assets/icons/pause_icon.svg"))
        self.pause_btn.setText("Pause")
        self.pause_btn.setObjectName("pauseBtn")
        self.pause_btn.setIconSize(QSize(50, 50))
        self.pause_btn.clicked.connect(self.on_pause_button_click)
        self.pause_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        pause_layout.addWidget(self.pause_btn, alignment=Qt.AlignHCenter)
        pause_layout.setContentsMargins(0, 30, 0, 20)
        self.layout.addLayout(pause_layout)

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
        button.setFixedSize(100, 100)
        button.setProperty('item_type', item_type)
        icon = self.get_item_icon(item_type)
        button.setIcon(icon)
        button.setIconSize(QSize(90, 90))  # Размер иконки меньше кнопки
        button.setStyleSheet("border: none;")
        button.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))
        return button

    def get_item_icon(self, item_type):
        normal_icon_map = {
            # 0: 'assets/icons/normal/chicken_icon.png',
            0: 'assets/icons/normal/lemon_icon.svg',
            # 1: 'assets/icons/normal/chili_icon.png',
            1: 'assets/icons/normal/donut_icon.png',
            2: 'assets/icons/normal/cherry_icon.svg',
            # 4: 'assets/icons/normal/rice_icon.png',
            # 4: 'assets/icons/normal/star_icon.png',
            4: 'assets/icons/normal/heart_icon.png',
            # 3: 'assets/icons/normal/avo_icon.png',
            # 3: 'assets/icons/normal/banana_icon.svg',
            3: 'assets/icons/normal/beer_icon.png',
        }
        mono_icon_map = {
            0: 'assets/icons/mono/bomb_icon.png',
            1: 'assets/icons/mono/what_icon.png',
            2: 'assets/icons/mono/pill_icon.png',
            3: 'assets/icons/mono/diamond_icon.png',
            # 3: 'assets/icons/mono/poison_icon.png',
            # 3: 'assets/icons/mono/what_icon.png',
            4: 'assets/icons/mono/health_icon.png',
        }

        if self.controller.current_theme == "monochromacy":
            icon_path = mono_icon_map.get(item_type, 'assets/icons/banana.svg')
        else:
            icon_path = normal_icon_map.get(item_type, 'assets/icons/banana.svg')

        return QIcon(icon_path)


    def generate_sample_items(self, rows, cols):
        import random
        types = [0, 1, 2, 3, 4]
        return [[random.choice(types) for _ in range(cols)] for _ in range(rows)]

    def cell_clicked(self, row, col):
        button = self.grid_layout.itemAtPosition(row, col).widget()

        if not button:
            return
        print(f"Clicked cells: {self.clicked_cells}")


        if len(self.clicked_cells) == 0:
            self.clear_item_selection()
            button.setStyleSheet("border: 5px solid black;")
            self.clicked_cells.append({"x": col, "y": row})
            return

        if len(self.clicked_cells) == 1:
            button.setStyleSheet("border: 5px solid black;")
            self.clicked_cells.append({"x": col, "y": row})
            data = {"gems": self.clicked_cells}
            self.send_move_to_backend(data)

    def clear_item_selection(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = self.grid_layout.itemAtPosition(row, col).widget()
                if button:
                    button.setStyleSheet("")

    def send_move_to_backend(self, data):
        response = api_request("/board/swap_gems_fullboard", params=data, method="POST")
        print(response)

        self.clear_item_selection()

        if "current_score" not in response or "moves_left" not in response:
            self.show_end_game_dialog()
            return

        if "board_status" in response:
            self.update_grid(len(response["board_status"]), len(response["board_status"][0]), response["board_status"])
            self.update_score_and_moves(response["current_score"], response["moves_left"])

        self.clicked_cells = []

    def on_pause_button_click(self):
        score = self.score_text_label.text()
        moves_left = self.energy_text_label.text()
        self.controller.show_pause(score, moves_left)
    
    def update_score_and_moves(self, score, moves_left):
        self.score_text_label.setText(f"{score}")
        self.energy_text_label.setText(f"{moves_left}")

        if moves_left == 0:
            self.show_end_game_dialog()

    def show_end_game_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Game Over")

        vbox = QVBoxLayout(dialog)
        label = QLabel("No moves left. Game Over!", dialog)
        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        new_game_btn = QPushButton("New Game", dialog)
        leaderboard_btn = QPushButton("Leaderboard", dialog)

        new_game_btn.clicked.connect(lambda: self.start_new_game(dialog))
        leaderboard_btn.clicked.connect(lambda: self.open_leaderboard(dialog))

        hbox.addWidget(new_game_btn)
        hbox.addWidget(leaderboard_btn)
        vbox.addLayout(hbox)

        dialog.setLayout(vbox)
        dialog.exec_()

    def sync_player_state(self):

        url = "http://localhost:8000/utils/sync"
        headers = {"accept": "application/json"}
        
        try:
            requests.post(url, headers=headers)
        
        except requests.RequestException as e:
            print(f"Sync error {e}")

    def start_new_game(self, dialog):
        dialog.close()
        self.controller.show_game_screen()

    def open_leaderboard(self, dialog):
        dialog.close()
        self.controller.show_leaderboard()