#Author: Movsesian Lilit - xmovse00
import tkinter as tk
from tkinter import messagebox, PhotoImage
import requests

class ChangeLoginPage:
    # Initializes the page.
    def __init__(self, master, player_data):
        self.master = master
        self.player_data = player_data
        self.background_color = "#ffe500"
        self.master.configure(bg=self.background_color)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.api_url = "http://localhost:8000"
        self.img_person = PhotoImage(file="assets/images/user.png")
        self.img_logo = PhotoImage(file="assets/images/change.png")

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

        title_label = tk.Label(left_frame, text="Enter your new name", **button_label_options)
        title_label.grid(row=0, column=1, pady=(0, 40), sticky="w")

        self.entry_login = tk.Entry(left_frame, **button_label_options)
        self.entry_login.grid(row=1, column=1, sticky="w")
        self.entry_login.focus()

        entry_underline = tk.Label(left_frame, text="-----------", **button_label_options)
        entry_underline.grid(row=1, column=1, sticky="w", pady=(70,0))

        login_btn = tk.Button(left_frame, text="Confirm", command=self.change_login, **second_button_label_options)
        login_btn.grid(row=2, column=1, sticky="w", padx=40)

        right_frame = tk.Frame(main_frame, bg=self.background_color)
        right_frame.grid(row=0, column=1, sticky="w", pady=60)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        img_logo_label = tk.Label(right_frame, image=self.img_logo, bg=self.background_color)
        img_logo_label.grid(sticky="nsew")

        back_btn = tk.Button(self.master, text="Back", command=self.open_menu, **button_label_options)
        back_btn.place(relx=0.05, rely=0.95, anchor="sw")

        self.master.bind('<Return>', self.on_enter)

    # Handles changing the login and sending it to the backend.
    def change_login(self):
        new_login = self.entry_login.get()
        if not new_login:
            messagebox.showerror("Error", "Login name cannot be empty!")
            return
        try:
            response = requests.patch(f"{self.api_url}/settings/update_login", json={"login": new_login})
            response.raise_for_status()
            if response.status_code == 200:
                self.get_current_player()
                self.open_menu()
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")
        except requests.RequestException as e:
            if "500" in str(e):
                self.show_error_message("This login name already exists!")
            else:
                messagebox.showerror("Request Error", f"An error occurred: {e}")

    # Fetches the current player's data from the backend.
    def get_current_player(self):
        try:
            response = requests.get(f"{self.api_url}/utils/current_player")
            response.raise_for_status()
            if response.status_code == 200:
                self.player_data = response.json()
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")
        except requests.RequestException as e:
            messagebox.showerror("Request Error", f"An error occurred: {e}")

    # Returns to the menu
    def open_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from .menu_page import MenuPage
        menu_page = MenuPage(self.master, self.player_data)
        menu_page.run()

    # Shows error message, is used in case of existing login in the database.
    def show_error_message(self, message):
        error_label = tk.Label(self.master, text=message, font=("Press Start 2P", 14), fg="black", bg="white", \
                               highlightbackground="red", highlightthickness=3, padx=10, pady=10)
        error_label.place(relx=0.5, rely=0.9, anchor="center")
        self.master.after(3000, error_label.destroy)


    def on_enter(self, event):
        self.change_login()

    def run(self):
        self.create_widgets()
