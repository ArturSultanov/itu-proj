# ------------------------------------------------------------
# Author: Tatiana Fedorova (xfedor14)
# Subject: ITU
# Year: 2024
# ------------------------------------------------------------

from PyQt5.QtWidgets import QApplication, QStackedWidget, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QFontDatabase
from windows.login_window import LoginScreen
from windows.main_window import MainMenuScreen
from windows.game_window import GameScreen
from windows.settings_window import SettingsScreen
from windows.leaderboard_window import LeaderboardScreen
from windows.palette_window import PaletteScreen
from windows.difficulty_window import DifficultyScreen
from windows.change_window import ChangeScreen
from windows.pause_window import PauseScreen
from utils.api_call import api_request
import requests

class AppController:
    def __init__(self):
        self.app = QApplication([])
        # load custom font
        font_id = QFontDatabase.addApplicationFont("assets/PressStart2P.ttf")
        if font_id == -1:
            print("Error: font is not found")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # apply stylesheet
        with open("assets/styles.qss", "r") as style_file:
            self.original_qss = style_file.read()
        self.app.setStyleSheet(self.original_qss)
        self.current_theme = "normal"

        # setup stacked window
        self.window = QStackedWidget()
        
        # initialize all screens
        self.login_screen = LoginScreen(self)
        self.main_menu_screen = MainMenuScreen(self)
        self.game_screen = GameScreen(self)
        self.settings_screen = SettingsScreen(self)
        self.leaderboard_screen = LeaderboardScreen(self)
        self.palette_screen = PaletteScreen(self)
        self.difficulty_screen = DifficultyScreen(self)
        self.change_screen = ChangeScreen(self)

        # add screens to stacked widget
        self.window.addWidget(self.login_screen)
        self.window.addWidget(self.main_menu_screen)
        self.window.addWidget(self.game_screen)
        self.window.addWidget(self.settings_screen)
        self.window.addWidget(self.leaderboard_screen)
        self.window.addWidget(self.palette_screen)
        self.window.addWidget(self.difficulty_screen)
        self.window.addWidget(self.change_screen)
        
        self.window.setFixedSize(1280, 960)
        self.center_window()
    
    # set the global stylesheet
    def apply_global_style(self, qss_string: str):
        self.app.setStyleSheet(qss_string)

    # display login screen
    def show_login_screen(self):
        self.window.setCurrentWidget(self.login_screen)
    
    # center the window on the screen
    def center_window(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        screen_center = screen_geometry.center() 
        window_geometry = self.window.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.window.move(window_geometry.topLeft())

    # start the application with login screen
    def run(self):
        self.window.setCurrentWidget(self.login_screen)
        self.window.show()
        self.app.exec_()

    # handle user login
    def login(self, username):
        response = api_request("/login", {"login": username}, method="GET")
        return response

    # show the main menu screen
    def show_main_menu(self):
        player_name = api_request("/utils/current_player", method="GET")["login"]
        self.main_menu_screen.update_player_info(player_name)
        self.window.setCurrentWidget(self.main_menu_screen)
    
    # start a new game
    def show_game_screen(self):
        response = api_request("/menu/new_game")
        print(response["board_status"])
        self.game_screen.update_score_and_moves(response["current_score"], response["moves_left"])
        self.game_screen.update_grid(len(response["board_status"]), len(response["board_status"][0]), response["board_status"])
        self.window.setCurrentWidget(self.game_screen)
    
    # display settings screen
    def show_settings(self):
        self.window.setCurrentWidget(self.settings_screen)
    
    # show the leaderboard
    def show_leaderboard(self):
        api_request("/utils/sync", method="POST")
        self.leaderboard_screen.update_leaderboard()
        self.window.setCurrentWidget(self.leaderboard_screen)
    
    # display palette screen
    def show_palette(self):
        self.window.setCurrentWidget(self.palette_screen)

    # show difficulty selection
    def show_difficulty(self):
        self.window.setCurrentWidget(self.difficulty_screen)

    # display change name screen
    def show_change(self):
        self.window.setCurrentWidget(self.change_screen)

    # pause the game and show pause screen
    def show_pause(self, score, moves_left):
        self.pause_screen = PauseScreen(self, score, moves_left)
        index = self.window.indexOf(self.pause_screen)
        if index != -1:
            self.window.removeWidget(self.pause_screen)
        self.window.addWidget(self.pause_screen)
        self.window.setCurrentWidget(self.pause_screen)

    # fetch leaderboard data
    def get_leaderboard_data(self, limit=5):
        # print(api_request("/utils/sync", method="POST"))
        url = f"http://localhost:8000/menu/leaderboard?limit={limit}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() if not isinstance(response.json(), dict) else []
        return []

    # confirm and quit the game
    def quit_game(self):
        parent_widget = self.window.window()
        message_box = QMessageBox(parent_widget)
        message_box.setWindowTitle("Quit Game")
        message_box.setText("Are you sure you want to quit?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)

        # set font size
        font = message_box.font()
        font.setPointSize(18)
        message_box.setFont(font)
        
        # style the message box
        message_box.setStyleSheet("""
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
        message_box.move(
            main_geometry.x() + 200,
            main_geometry.y() + 400
        )
        
        reply = message_box.exec_()
        if reply == QMessageBox.Yes:
            self.app.quit()

if __name__ == "__main__":
    controller = AppController()
    controller.run()
