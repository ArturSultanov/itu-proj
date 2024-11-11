# frontend/main.py
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDesktopWidget
from windows.login_window import LoginScreen
from windows.main_window import MainMenuScreen
from windows.game_window import GameScreen
from utils.api_call import api_request

class AppController:
    def __init__(self):
        self.app = QApplication([])

        self.window = QStackedWidget()

        self.login_screen = LoginScreen(self)
        self.main_menu_screen = MainMenuScreen(self)
        self.game_screen = GameScreen(self)

        self.window.addWidget(self.login_screen)
        self.window.addWidget(self.main_menu_screen)
        self.window.addWidget(self.game_screen)
        
        # Set the default window size
        self.window.resize(1000, 1000)  # Default size of the window

        # Center the window
        self.center_window()
        
    def center_window(self):
        """Centers the window on the screen."""
        screen_geometry = QDesktopWidget().availableGeometry()  # Get screen geometry
        screen_center = screen_geometry.center()  # Get the center of the screen
        window_geometry = self.window.frameGeometry()  # Get the geometry of the window
        window_geometry.moveCenter(screen_center)  # Move window to the center
        self.window.move(window_geometry.topLeft())  # Move the window to the top-left corner of the geometry

    def run(self):
        self.window.setCurrentWidget(self.login_screen)  # Start with login screen
        self.window.show()
        self.app.exec_()

    def login(self, username):
        response = api_request("/login", {"login": username}, method="GET")
        return response

    def show_main_menu(self):
        player_name = api_request("/utils/current_player", method="GET")["login"]
        self.main_menu_screen.update_player_info(player_name)
        self.window.setCurrentWidget(self.main_menu_screen)
    
    def show_game_screen(self):
        response = api_request("/menu/new_game")
        print(response["board_status"])
        self.game_screen.update_score_and_moves(response["current_score"], response["moves_left"])
        self.game_screen.update_grid(len(response["board_status"]), len(response["board_status"][0]), response["board_status"])
        self.window.setCurrentWidget(self.game_screen)


if __name__ == "__main__":
    controller = AppController()
    controller.run()
