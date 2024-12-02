#Author: Movsesian Lilit - xmovse00
import tkinter as tk
from src.login_page import LoginPage

def main():
    # Create the root window for the application.
    root = tk.Tk()
    root.title("Tile Match")
    # Maximize the window.
    root.state("zoomed")
    login_page = LoginPage(root)
    login_page.run()
     # Start the main event loop. 
    root.mainloop()

if __name__ == "__main__":
    main()