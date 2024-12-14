#Author: Movsesian Lilit - xmovse00
import tkinter as tk
from tkinter import messagebox, PhotoImage
import requests
from .game_page import GamePage
from .leader_page import LeaderPage
from .settings_page import SettingsPage

class MenuPage:
    # Initializes the page.
    def __init__(self, master, player_data):
        self.master = master
        self.background_color = "#ffe500"
        self.player_data = player_data
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.img_welcome = PhotoImage(file="assets/images/welcome.png")
        self.api_url = "http://localhost:8000"
        self.button_label_options = {
            "font": ("Press Start 2P", 24),
            "bg": self.background_color,
            "fg": "black",
            "bd": 0,
        }
        self.second_button_label_options = {
            "font": ("Press Start 2P", 24),
            "fg": "white",
            "bg": "black",
            "bd": 0,
        }
        
    # Creates widgets.
    def create_widgets(self):
        img_welcome_label = tk.Label(self.master, image=self.img_welcome, bg=self.background_color)
        img_welcome_label.pack(pady=0)

        welcome_btn = tk.Button(self.master, text=f"Hi, {self.player_data['login']}!", command=self.switch_user,\
                                 font=("Press Start 2P", 24), bg=self.background_color, fg="black")
        welcome_btn.pack(pady=0)

        button_frame = tk.Frame(self.master, bg=self.background_color)
        button_frame.pack(pady=20)
        button_frame.columnconfigure(0, weight=1)
        for i in range(4):
            button_frame.rowconfigure(i, weight=1)

        play_btn = tk.Button(button_frame, text="New Game", command=self.start_new_game, **self.button_label_options)
        play_btn.grid(row=0, column=0)

        self.continue_btn = tk.Button(button_frame, text="Continue", command=self.continue_game, **self.button_label_options)
        self.continue_btn.grid(row=1, column=0)

        # Checks if there is an existing game and configures the button.
        try:
            response = requests.get(f"{self.api_url}/menu/continue")
            if response.status_code == 200:
                self.continue_btn.config(state="normal")
                self.delete_btn = tk.Button(button_frame, text="Delete",command=self.delete_confirmation, \
                                       font=("Press Start 2P", 14), bg="red", fg="white", bd=0)
                self.delete_btn.grid(row=1, column=0, padx=(460,0), pady=(0,10))
            if response.status_code == 404:
                self.continue_btn.config(state="disabled")
        except requests.RequestException as e:
            if "NewConnectionError" in str(e):
                self.show_error_message("Server Error!")
            else:
                if "NewConnectionError" in str(e):
                    self.show_error_message("Server Error!")
                else:
                    messagebox.showerror("Request Error", f"An error occurred: {e}")

        settings_btn = tk.Button(button_frame, text="Settings", command=self.open_settings, **self.button_label_options)
        settings_btn.grid(row=2, column=0)

        leaderboard_btn = tk.Button(button_frame, text="Leaderboard", command=self.get_leaderboard, **self.button_label_options)
        leaderboard_btn.grid(row=3, column=0)

        quit_btn = tk.Button(self.master, text="Quit Game", command=self.quit_confirmation, **self.button_label_options)
        quit_btn.place(relx=0.05, rely=0.95, anchor="sw")

    # Requests the backend for the new game.
    def start_new_game(self):
        try:
            response = requests.get(f"{self.api_url}/menu/new_game")
            response.raise_for_status()

            if response.status_code == 200:
                game_data = response.json()
                self.open_new_game(game_data)
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")

        except requests.RequestException as e:
            if "NewConnectionError" in str(e):
                self.show_error_message("Server Error!")
            else:
                messagebox.showerror("Request Error", f"An error occurred: {e}")

    # Creates the game page.
    def open_new_game(self, game_data):
        for widget in self.master.winfo_children():
            widget.destroy()
        game_page = GamePage(self.master, game_data, self.player_data)
        game_page.run()

    # Requests the backend for an existing game.
    def continue_game(self):
        try:
            response = requests.get(f"{self.api_url}/menu/continue")
            response.raise_for_status()
            if response.status_code == 200:
                game_data = response.json()
                self.open_new_game(game_data)
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")

        except requests.RequestException as e:
            if "NewConnectionError" in str(e):
                self.show_error_message("Server Error!")
            else:
                messagebox.showerror("Request Error", f"An error occurred: {e}")

    # Created settings page.
    def open_settings(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        settings_page = SettingsPage(self.master, self.player_data)
        settings_page.run()

    # Requests the backend for the leaders.
    def get_leaderboard(self):
        try:
            response = requests.get(f"{self.api_url}/menu/leaderboard", params={"limit": 20})
            response.raise_for_status()

            if response.status_code == 200:
                leader_data = response.json()
                self.open_leaderboard(leader_data)
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")

        except requests.RequestException as e:
            if "NewConnectionError" in str(e):
                self.show_error_message("Server Error!")
            else:
                messagebox.showerror("Request Error", f"An error occurred: {e}")

    # Creates the leaderboard page.
    def open_leaderboard(self, leader_data):
        for widget in self.master.winfo_children():
            widget.destroy()
        leader_page = LeaderPage(self.master, leader_data, self.player_data)
        leader_page.run()

    # Deletes an existing game on the backend and configures the buttons.
    def delete_current_game(self, overlay):
        overlay.destroy()
        try:
            response = requests.delete(f"{self.api_url}/menu/delete_game")
            response.raise_for_status()
            if response.status_code == 200:
                self.continue_btn.config(state="disabled")
                if self.delete_btn:
                    self.delete_btn.destroy()
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")
        except requests.RequestException as e:
            if "NewConnectionError" in str(e):
                self.show_error_message("Server Error!")
            else:
                messagebox.showerror("Request Error", f"An error occurred: {e}")

    def quit_confirmation(self):
        rect_width = 700
        rect_height = 400
        rect_x0 = (self.master.winfo_width() - rect_width) // 2
        rect_y0 = (self.master.winfo_height() - rect_height) // 2

        overlay = tk.Frame(self.master, bg=self.background_color, relief="solid", bd=6)
        overlay.place(x=rect_x0, y=rect_y0, width=rect_width, height=rect_height)

        text_label = tk.Label(overlay,text="""Are you sure you
want to quit 
the game?""", **self.button_label_options)
        text_label.pack(pady=60)

        button_frame = tk.Frame(overlay, bg=self.background_color)
        button_frame.pack(pady=10)

        yes_button = tk.Button(button_frame, text="Yes", command=self.quit_game, **self.second_button_label_options)
        yes_button.grid(row=0, column=0, padx=60)

        no_button = tk.Button(button_frame, text="No", command=overlay.destroy, **self.second_button_label_options)
        no_button.grid(row=0, column=1, padx=260)

    def quit_game(self):
        self.master.destroy()

    # A frame for the user switching window.
    def switch_user(self):
        rect_width = 700
        rect_height = 400
        rect_x0 = (self.master.winfo_width() - rect_width) // 2
        rect_y0 = (self.master.winfo_height() - rect_height) // 2

        overlay = tk.Frame(self.master, bg=self.background_color, relief="solid", bd=6)
        overlay.place(x=rect_x0, y=rect_y0, width=rect_width, height=rect_height)

        text_label = tk.Label(overlay,text="""Are you sure you
want to change 
player?""", **self.button_label_options)
        text_label.pack(pady=60)

        button_frame = tk.Frame(overlay, bg=self.background_color)
        button_frame.pack(pady=10)

        yes_button = tk.Button(button_frame, text="Yes", command=self.open_login, **self.second_button_label_options)
        yes_button.grid(row=0, column=0, padx=60)

        no_button = tk.Button(button_frame, text="No", command=overlay.destroy, **self.second_button_label_options)
        no_button.grid(row=0, column=1, padx=260)
    
    def delete_confirmation(self):
        rect_width = 700
        rect_height = 400
        rect_x0 = (self.master.winfo_width() - rect_width) // 2
        rect_y0 = (self.master.winfo_height() - rect_height) // 2

        overlay = tk.Frame(self.master, bg=self.background_color, relief="solid", bd=6)
        overlay.place(x=rect_x0, y=rect_y0, width=rect_width, height=rect_height)

        text_label = tk.Label(overlay,text="""Are you sure you
want to delete 
current game?""", **self.button_label_options)
        text_label.pack(pady=60)

        button_frame = tk.Frame(overlay, bg=self.background_color)
        button_frame.pack(pady=10)

        yes_button = tk.Button(button_frame, text="Yes", command=lambda: self.delete_current_game(overlay), **self.second_button_label_options)
        yes_button.grid(row=0, column=0, padx=60)

        no_button = tk.Button(button_frame, text="No", command=overlay.destroy, **self.second_button_label_options)
        no_button.grid(row=0, column=1, padx=260)

    # Creates the login page in case of the user switch.
    def open_login(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from .login_page import LoginPage
        login_page = LoginPage(self.master)
        login_page.run()

    # Shows error message.
    def show_error_message(self, message):
        error_label = tk.Label(self.master, text=message, font=("Press Start 2P", 14), fg="black", bg="white", \
                               highlightbackground="red", highlightthickness=3, padx=10, pady=10)
        error_label.place(relx=0.5, rely=0.9, anchor="center")
        self.master.after(3000, error_label.destroy)
        
    def run(self):
        self.create_widgets()
