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

        title_label = tk.Label(left_frame, text="Enter your name", **self.button_label_options)
        title_label.grid(row=0, column=1, pady=(0, 40), sticky="w")

        self.entry_login = tk.Entry(left_frame, **self.button_label_options)
        self.entry_login.grid(row=1, column=1, sticky="w")
        self.entry_login.focus()

        entry_underline = tk.Label(left_frame, text="-----------", **self.button_label_options)
        entry_underline.grid(row=1, column=1, sticky="w", pady=(70,0))

        login_btn = tk.Button(left_frame, text="Confirm", command=self.login, **self.second_button_label_options)
        login_btn.grid(row=2, column=1, sticky="w", padx=40)

        right_frame = tk.Frame(main_frame, bg=self.background_color)
        right_frame.grid(row=0, column=1, sticky="w", pady=60)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        img_logo_label = tk.Label(right_frame, image=self.img_logo, bg=self.background_color)
        img_logo_label.grid(sticky="nsew")

        quit_btn = tk.Button(self.master, text="Quit Game", command=self.quit_confirmation, **self.button_label_options)
        quit_btn.place(relx=0.05, rely=0.95, anchor="sw")

        self.master.bind('<Return>', self.on_enter)

    # Handles login sending to the backend.
    def login(self):
        login_name = self.entry_login.get()
        if not login_name:
            self.show_error_message("Login name cannot be empty!")
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
            if "NewConnectionError" in str(e):
                self.show_error_message("Server Error!")
            else:
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

    # Shows error message.
    def show_error_message(self, message):
        error_label = tk.Label(self.master, text=message, font=("Press Start 2P", 14), fg="black", bg="white", \
                               highlightbackground="red", highlightthickness=3, padx=10, pady=10)
        error_label.place(relx=0.5, rely=0.9, anchor="center")
        self.master.after(3000, error_label.destroy)

    def run(self):
        self.create_widgets()
