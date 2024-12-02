#Author: Movsesian Lilit - xmovse00
import tkinter as tk
from tkinter import messagebox, PhotoImage
import requests

class DifficultyPage:
    # Initializes the page.
    def __init__(self, master, player_data):
        self.master = master
        self.background_color = "#ffe500"
        self.player_data = player_data
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.api_url = "http://localhost:8000"
        self.img_girl = PhotoImage(file="assets/images/girl.png")

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
        for i in range(3):
            left_frame.rowconfigure(i, weight=1)

        self.easy_btn = tk.Button(left_frame, text="Easy", command=lambda: self.set_difficulty(1), **button_label_options)
        self.easy_btn.grid(row=0, column=0, sticky="w")

        self.normal_btn = tk.Button(left_frame, text="Normal", command=lambda: self.set_difficulty(2), **button_label_options)
        self.normal_btn.grid(row=1, column=0, sticky="w")

        self.hard_btn = tk.Button(left_frame, text="Hard", command=lambda: self.set_difficulty(3), **button_label_options)
        self.hard_btn.grid(row=2, column=0, sticky="w")

        right_frame = tk.Frame(main_frame, bg=self.background_color)
        right_frame.grid(row=0, column=1, sticky="se", pady=20)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        img_girl_label = tk.Label(right_frame, image=self.img_girl, bg=self.background_color)
        img_girl_label.grid(sticky="se")

        back_btn = tk.Button(self.master, text="Back", command=self.open_settings, **button_label_options)
        back_btn.place(relx=0.05, rely=0.95, anchor="sw")

        self.get_current_difficulty()

    # Created the settings page.
    def open_settings(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from .settings_page import SettingsPage
        settings_page = SettingsPage(self.master, self.player_data)
        settings_page.run()

    # Sends get request to the backend to determine which difficulty level is currently selected and configure the buttons.
    def get_current_difficulty(self):
        try:
            response = requests.get(f"{self.api_url}/settings/get_difficulty")
            response.raise_for_status()
            if response.status_code == 200:
                self.current_difficulty = response.json().get("difficulty", 1)
                self.update_button_states()
            else:
                messagebox.showerror("Error", f"Failed to fetch difficulty: {response.status_code}")
        except requests.RequestException as e:
            messagebox.showerror("Request Error", f"An error occurred: {e}")

    # Configures the buttons based on the current level.
    def update_button_states(self):
        if self.current_difficulty == 1:
            self.easy_btn.config(state="disabled")
            self.normal_btn.config(state="normal")
            self.hard_btn.config(state="normal")
        elif self.current_difficulty == 2:
            self.easy_btn.config(state="normal")
            self.normal_btn.config(state="disabled")
            self.hard_btn.config(state="normal")
        elif self.current_difficulty == 3:
            self.easy_btn.config(state="normal")
            self.normal_btn.config(state="normal")
            self.hard_btn.config(state="disabled")

    # Sends request to the backend to change the difficulty.
    def set_difficulty(self, diff):
        try:
            response = requests.patch(f"{self.api_url}/settings/set_difficulty", json={"difficulty": diff})
            response.raise_for_status()
            if response.status_code == 200:
                self.current_difficulty = diff
                self.update_button_states()
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")
        except requests.RequestException as e:
            messagebox.showerror("Request Error", f"An error occurred: {e}")

    def run(self):
        self.create_widgets()
