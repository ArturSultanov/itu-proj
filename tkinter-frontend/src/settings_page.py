#Author: Movsesian Lilit - xmovse00
import tkinter as tk
from tkinter import PhotoImage
from .difficulty_page import DifficultyPage
from .change_login_page import ChangeLoginPage

class SettingsPage:
    # Initializes the page.
    def __init__(self, master, player_data):
        self.master = master
        self.background_color = "#ffe500"
        self.player_data = player_data
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.img_bot = PhotoImage(file="assets/images/bot.png")
        
    # Creates widgets.
    def create_widgets(self):
        button_label_options = {
            "font": ("Press Start 2P", 24),
            "bg": self.background_color,
            "fg": "black",
            "bd": 0,
        }

        main_frame = tk.Frame(self.master, bg=self.background_color)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        for i in range(2):
            main_frame.rowconfigure(i, weight=1)

        left_frame = tk.Frame(main_frame, bg=self.background_color)
        left_frame.grid(row=0, column=0, sticky="w", pady=260, padx=140)
        left_frame.columnconfigure(0, weight=1)
        for i in range(2):
            left_frame.rowconfigure(i, weight=1)

        difficulty_btn = tk.Button(left_frame, text="Difficulty Level", command=self.change_difficulty, **button_label_options)
        difficulty_btn.grid(row=0, column=0, sticky="w")

        change_name_btn = tk.Button(left_frame, text="Change Name", command=self.change_login, **button_label_options)
        change_name_btn.grid(row=1, column=0, sticky="w")

        right_frame = tk.Frame(main_frame, bg=self.background_color)
        right_frame.grid(row=0, column=1, sticky="se", pady=20)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        img_bot_label = tk.Label(right_frame, image=self.img_bot, bg=self.background_color)
        img_bot_label.grid(sticky="se")

        back_btn = tk.Button(self.master, text="Back", command=self.open_menu, **button_label_options)
        back_btn.place(relx=0.05, rely=0.95, anchor="sw")

    # Returns to the menu.
    def open_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from .menu_page import MenuPage
        menu_page = MenuPage(self.master, self.player_data)
        menu_page.run()

    # Creates the difficulty change page.
    def change_difficulty(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        difficulty_page = DifficultyPage(self.master, self.player_data)
        difficulty_page.run()

    # Creates the login change page.
    def change_login(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        change_login_page = ChangeLoginPage(self.master, self.player_data)
        change_login_page.run()

    def run(self):
        self.create_widgets()