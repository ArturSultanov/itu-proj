#Author: Movsesian Lilit - xmovse00
import tkinter as tk
from tkinter import PhotoImage

class PausePage:
    # Initializes the page.
    def __init__(self, master, game_data, player_data):
        self.master = master
        self.background_color = "#ffe500"
        self.game_data = game_data
        self.player_data = player_data
        self.selected_gems = []
        self.api_url = "http://localhost:8000"
        self.img_score = PhotoImage(file="assets/images/score.png") 
        self.img_moves = PhotoImage(file="assets/images/moves.png") 
        self.img_play = PhotoImage(file="assets/images/play.png")
        self.img_pause_girl = PhotoImage(file="assets/images/pause_girl.png")
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
        main_frame.pack(pady=20)
        main_frame.columnconfigure(0, weight=1)
        for i in range(3):
            main_frame.rowconfigure(i, weight=1)

        top_frame = tk.Frame(main_frame, bg=self.background_color)
        top_frame.grid()
        for i in range(5):
            top_frame.columnconfigure(i, weight=1)
        for i in range(2):
            top_frame.rowconfigure(i, weight=1)

        img_score_label = tk.Label(top_frame, image=self.img_score, bg=self.background_color)
        img_score_label.grid(row=0, column=0, rowspan=2)

        self.score_label = tk.Label(top_frame, text=f"{self.game_data['current_score']}", **self.button_label_options)
        self.score_label.grid(row=0, column=1)

        score_underline = tk.Label(top_frame, text="------", **self.button_label_options)
        score_underline.grid(row=1, column=1)
        
        spacer = tk.Label(top_frame, width=60, bg=self.background_color)
        spacer.grid(row=0, column=2, rowspan=2)
        
        img_moves_label = tk.Label(top_frame, image=self.img_moves, bg=self.background_color)
        img_moves_label.grid(row=0, column=3, rowspan=2)

        self.moves_label = tk.Label(top_frame, text=f"{self.game_data['moves_left']}", **self.button_label_options)
        self.moves_label.grid(row=0, column=4)

        moves_underline = tk.Label(top_frame, text="------", **self.button_label_options)
        moves_underline.grid(row=1, column=4)

        img_pause_girl_label = tk.Label(main_frame, image=self.img_pause_girl, **self.button_label_options)
        img_pause_girl_label .grid()

        img_play_btn = tk.Button(main_frame, image=self.img_play, command=self.play_pressed, **self.button_label_options)
        img_play_btn.grid()

        quit_btn = tk.Button(self.master, text="Quit Game", command=self.quit_confirmation, **self.button_label_options)
        quit_btn.place(relx=0.05, rely=0.95, anchor="sw")

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

    # Creates the game page with the same game data.
    def play_pressed(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from .game_page import GamePage
        game_page = GamePage(self.master, self.game_data, self.player_data)
        game_page.run()

    def run(self):
        self.create_widgets()
