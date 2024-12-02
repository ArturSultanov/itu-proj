#Author: Movsesian Lilit - xmovse00
import tkinter as tk
from tkinter import messagebox, PhotoImage
import requests
from .menu_page import MenuPage

class LoginPage:
    # Initializes the page.
    def __init__(self, master):
        self.master = master
        self.background_color = "#ffe500"
        self.master.configure(bg=self.background_color)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.api_url = "http://localhost:8000"
        self.img_person = PhotoImage(file="assets/images/user.png")
        self.img_logo = PhotoImage(file="assets/images/logo.png")

    # Creates widgets.
    def create_widgets(self):
        button_label_options = {
            "font": ("Press Start 2P", 24),
            "bg": self.background_color,
            "fg": "black",
            "bd": 0,
        }
        second_button_label_options = {
            "font": ("Press Start 2P", 24),
            "fg": "white",
            "bg": "black",
            "bd": 0,
        }
                
        main_frame = tk.Frame(self.master, bg=self.background_color)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        left_frame = tk.Frame(main_frame, bg=self.background_color)
        left_frame.grid(row=0, column=0, sticky="w", padx=100, pady=200)
        for i in range(2):
            left_frame.columnconfigure(i, weight=1)
        for i in range(3):
            left_frame.rowconfigure(i, weight=1)

        img_person_label = tk.Label(left_frame, image=self.img_person, bg=self.background_color)
        img_person_label.grid(row=1, column=0, padx=(0, 40), sticky="w")

        title_label = tk.Label(left_frame, text="Enter your name", **button_label_options)
        title_label.grid(row=0, column=1, pady=(0, 40), sticky="w")

        self.entry_login = tk.Entry(left_frame, **button_label_options)
        self.entry_login.grid(row=1, column=1, sticky="w")
        self.entry_login.focus()

        entry_underline = tk.Label(left_frame, text="-----------", **button_label_options)
        entry_underline.grid(row=1, column=1, sticky="w", pady=(70,0))

        login_btn = tk.Button(left_frame, text="Confirm", command=self.login, **second_button_label_options)
        login_btn.grid(row=2, column=1, sticky="w", padx=40)

        right_frame = tk.Frame(main_frame, bg=self.background_color)
        right_frame.grid(row=0, column=1, sticky="w", pady=60)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        img_logo_label = tk.Label(right_frame, image=self.img_logo, bg=self.background_color)
        img_logo_label.grid(sticky="nsew")

        quit_btn = tk.Button(self.master, text="Quit Game", command=self.quit_game, **button_label_options)
        quit_btn.place(relx=0.05, rely=0.95, anchor="sw")

        self.master.bind('<Return>', self.on_enter)

    # Handles login sending to the backend.
    def login(self):
        login_name = self.entry_login.get()
        if not login_name:
            messagebox.showerror("Error", "Login name cannot be empty!")
            return
        
        try:
            response = requests.get(f"{self.api_url}/login", params={"login": login_name})
            response.raise_for_status()

            if response.status_code == 200:
                self.player_data = response.json()
                self.open_menu()
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")

        except requests.RequestException as e:
            messagebox.showerror("Request Error", f"An error occurred: {e}")

    # Returns to the menu.
    def open_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        menu_page = MenuPage(self.master, self.player_data)
        menu_page.run()

    # Triggered when Enter key is pressed to call the login function.
    def on_enter(self, event):
        self.login()

    def quit_game(self):
        self.master.destroy()

    def run(self):
        self.create_widgets()
