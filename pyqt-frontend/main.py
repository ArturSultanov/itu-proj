from PyQt5.QtWidgets import QApplication, QStackedWidget, QDesktopWidget
from PyQt5.QtGui import QFontDatabase
from windows.login_window import LoginScreen
from windows.main_window import MainMenuScreen
from windows.game_window import GameScreen
from utils.api_call import api_request

class AppController:
    def __init__(self):
        self.app = QApplication([])
        font_id = QFontDatabase.addApplicationFont("assets/PressStart2P.ttf")
        if font_id == -1:
            print("Error: font is not found")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        with open("assets/styles.qss", "r") as style_file:
            self.app.setStyleSheet(style_file.read())

        self.window = QStackedWidget()

        self.login_screen = LoginScreen(self)
        self.main_menu_screen = MainMenuScreen(self)
        self.game_screen = GameScreen(self)

        self.window.addWidget(self.login_screen)
        self.window.addWidget(self.main_menu_screen)
        self.window.addWidget(self.game_screen)
        
        # window
        self.window.resize(1280, 960)
        self.center_window()
        
    def center_window(self):
        # window centering
        screen_geometry = QDesktopWidget().availableGeometry()
        screen_center = screen_geometry.center() 
        window_geometry = self.window.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.window.move(window_geometry.topLeft())

    def run(self):
        # login screen
        self.window.setCurrentWidget(self.login_screen)
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
    def quit_game(self):
        response = api_request("/utils/exit", method="POST")
        if response and isinstance(response, dict) and "detail" in response:
            print(response["detail"])
        else:
            print("No 'detail' key in the response or the response is invalid:", response)
        self.app.quit()

if __name__ == "__main__":
    controller = AppController()
    controller.run()
