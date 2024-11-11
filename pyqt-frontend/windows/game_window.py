import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from utils.api_call import api_request

class GameScreen(QWidget):
    def __init__(self, controller, rows=5, cols=6):
        super().__init__()
        self.controller = controller
        self.rows = rows
        self.cols = cols
        self.cell_size = 50  # Fixed cell size in pixels
        self.clicked_cells = []  # Track clicked cells

        grid_width = self.cols * self.cell_size
        grid_height = self.rows * self.cell_size
        self.setFixedSize(grid_width + 100, grid_height + 150)  # Extra space for centering and button

        self.setWindowTitle("Game Screen")

        self.top_layout = QHBoxLayout()
        # Main layout setup
        self.layout = QVBoxLayout()

        self.score_label = QLabel("Score: 0", self)
        self.moves_left_label = QLabel("Moves Left: 10", self)

        # Add labels to the top layout with space between them
        self.top_layout.addWidget(self.score_label)
        self.top_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Spacer for space between
        self.top_layout.addWidget(self.moves_left_label)
        
        self.layout.addLayout(self.top_layout)
        
        # Spacer at the top for vertical centering
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer_top)

        # Horizontal layout for centering the grid layout
        hbox_layout = QHBoxLayout()
        left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hbox_layout.addItem(left_spacer)
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        hbox_layout.addLayout(self.grid_layout)
        right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hbox_layout.addItem(right_spacer)

        self.layout.addLayout(hbox_layout)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer_bottom)

        # Back to main menu button
        self.back_button = QPushButton("Back to Main Menu", self)
        self.back_button.clicked.connect(self.on_back_button_click)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
        self.center()

        self.update_grid(self.rows, self.cols, self.generate_sample_items(self.rows, self.cols))

    def center(self):
        """Center the window on the screen."""
        screen_geometry = QDesktopWidget().availableGeometry()
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

    def update_grid(self, rows, cols, items):
        """Fill the grid with cells based on current state."""
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
        """Create a widget for each grid cell and handle cell clicks."""
        button = QPushButton(self)
        button.setFixedSize(self.cell_size, self.cell_size)
        button.setStyleSheet(f"background-color: {self.get_item_color(item_type)};")
        button.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))
        return button

    def get_item_color(self, item_type):
        """Map item type to color."""
        color_map = {
            0: 'purple',
            1: 'red',
            2: 'blue',
            3: 'green',
            4: 'yellow',
        }
        return color_map.get(item_type, 'gray')

    def generate_sample_items(self, rows, cols):
        """Generate sample grid data for testing without API."""
        import random
        types = [0, 1, 2, 3, 4]
        return [[random.choice(types) for _ in range(cols)] for _ in range(rows)]

    def cell_clicked(self, row, col):
        """Track cell clicks and send data to backend if two cells are selected."""
        self.clicked_cells.append({"x": col, "y": row})
        print(f"Cell clicked at row {row}, column {col}")

        if len(self.clicked_cells) == 2:
            # Prepare data for backend
            data = {"gems": self.clicked_cells}
            self.send_move_to_backend(data)
            self.clicked_cells = []  # Reset clicked cells for next move

    def send_move_to_backend(self, data):
        """Send selected cell coordinates to the backend and update the grid with the response."""
        response = api_request("/board/swap_gems_fullboard", params=data, method="POST")
        print(response)
        self.update_score_and_moves(response["current_score"], response["moves_left"])
        self.update_grid(len(response["board_status"]), len(response["board_status"][0]), response["board_status"])

    def on_back_button_click(self):
        """Return to main menu."""
        self.controller.show_main_menu()
    
    def update_score_and_moves(self, score, moves_left):
        """Update the score and moves left labels."""
        self.score_label.setText(f"Score: {score}")
        self.moves_left_label.setText(f"Moves Left: {moves_left}")
