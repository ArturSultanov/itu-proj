import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget
from windows.login_window import LoginWindow
from windows.main_window import MainWindow
from windows.game_window import GameWindow1

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow(self)
        self.login_window = None
        self.game_window = GameWindow1(self)

    def show_login(self):
        self.login_window = LoginWindow(self)
        # Create a stacked widget to manage layouts
        self.stacked_widget = QStackedWidget()
        
        # Add layouts to stacked widget
        self.stacked_widget.addWidget(self.login_window.init_ui())
        self.stacked_widget.addWidget(self.main_window.init_ui())
        self.stacked_widget.addWidget(self.game_window.init_ui())


        # Show login layout first
        self.stacked_widget.setCurrentIndex(0)
        
        self.stacked_widget.show()

    def show_main(self):
        # Switch to the main window layout
        self.stacked_widget.setCurrentIndex(1)

    def show_game(self):
        # Switch to the game window layout
        self.stacked_widget.setCurrentIndex(2)

    def run(self):
        self.show_login()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = AppController()
    controller.run()
