#Author: Movsesian Lilit - xmovse00
import tkinter as tk
from tkinter import messagebox, PhotoImage
import requests
from .pause_page import PausePage

class GamePage:
    # Initializes the page.
    def __init__(self, master, game_data, player_data):
        self.master = master
        self.background_color = "#ffe500"
        self.game_data = game_data
        self.player_data = player_data
        self.selected_gems = []
        self.api_url = "http://localhost:8000"
        self.icons = [
            PhotoImage(file="assets/images/icon1.png").subsample(20, 20),
            PhotoImage(file="assets/images/icon2.png").subsample(20, 20),
            PhotoImage(file="assets/images/icon3.png").subsample(20, 20),
            PhotoImage(file="assets/images/icon4.png").subsample(20, 20),
            PhotoImage(file="assets/images/icon5.png").subsample(20, 20)
        ]
        self.img_score = PhotoImage(file="assets/images/score.png") 
        self.img_moves = PhotoImage(file="assets/images/moves.png") 
        self.img_pause = PhotoImage(file="assets/images/pause.png").subsample(6, 6)
        self.img_shuffle = PhotoImage(file="assets/images/shuffle.png")
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

        img_shuffle_btn = tk.Button(self.master, image=self.img_shuffle, command=self.shuffle, **self.button_label_options)
        img_shuffle_btn.place(relx=0.95, rely=0.95, anchor="se")

        self.board_frame = tk.Frame(main_frame, bg=self.background_color, relief="solid", bd=6)
        self.board_frame.grid()

        self.print_board()

        img_pause_btn = tk.Button(main_frame, image=self.img_pause, command=self.pause_pressed, **self.button_label_options)
        img_pause_btn.grid(pady=20)

        back_btn = tk.Button(self.master, text="Back", command=self.open_menu, **self.button_label_options)
        back_btn.place(relx=0.05, rely=0.95, anchor="sw")

    # Prints board and creates buttons of each icon.
    def print_board(self):
        for x in range(6):
            for y in range(6):
                value = self.game_data["board_status"][x][y]
                icon = self.icons[value]
                if value == 4:
                    button = tk.Button(self.board_frame, image=icon, bg=self.background_color, command=lambda x=x, y=y: self.click_gem(x, y), bd=0)
                else:
                    button = tk.Button(self.board_frame, image=icon, bg=self.background_color, command=lambda x=x, y=y: self.select_gem(x, y), bd=0)
                button.grid(row=x, column=y, padx=5, pady=5)

    # Selects gem, configures the button to the pressed design, adds the gem to the selected_gems list of 2.
    def select_gem(self, x, y):
        if len(self.selected_gems) < 2:
            button = self.board_frame.grid_slaves(row=x, column=y)[0]
            button.config(bg="white")
            self.selected_gems.append((x, y))
            
            if len(self.selected_gems) == 2:
                self.swap_gems()

    # Swaps the gems on the backend.
    def swap_gems(self):
        gem1, gem2 = self.selected_gems
        if abs(gem1[0] - gem2[0]) + abs(gem1[1] - gem2[1]) == 1:
            try:
                payload = {"gems": [{"x": gem1[1], "y": gem1[0]}, {"x": gem2[1], "y": gem2[0]}]}
                response = requests.post(f"{self.api_url}/board/swap_gems", json=payload)

                if response.status_code == 200:
                    self.update_game_data(response.json())
                elif response.status_code == 406:
                    pass
                else:
                    messagebox.showerror("Error", f"Response code: {response.status_code}")

            except requests.RequestException as e:
                messagebox.showerror("Request Error", f"An error occurred: {e}")

        # Configures the gems buttons.
        for gem in self.selected_gems:
            button = self.board_frame.grid_slaves(row=gem[0], column=gem[1])[0]
            button.config(bg=self.background_color)
        
        self.selected_gems.clear()


    # Clicks the heart gem on the backend, configures the button to the selected state and then to the unselected state.
    def click_gem(self, x, y):
        button = self.board_frame.grid_slaves(row=0, column=0)[0]
        button.config(bg="white")
        try:
            payload = {"x": y, "y": x}
            response = requests.post(f"{self.api_url}/board/click_gem", json=payload)
            
            if response.status_code == 200:
                new_data = response.json()
                self.update_game_data(new_data)
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")

        except requests.RequestException as e:
            messagebox.showerror("Request Error", f"An error occurred: {e}")

        # Configures the button.
        button.config(bg=self.background_color)

    # Updates the changed gems, left moves and current score.
    def update_game_data(self, new_data):
        updated_gems = new_data["updated_gems"]
    
        self.game_data["current_score"] = new_data["current_score"]
        self.game_data["moves_left"] = new_data["moves_left"]
        self.score_label.config(text=str(self.game_data["current_score"]))
        self.moves_label.config(text=str(self.game_data["moves_left"]))

        for gem in updated_gems:
            x, y, gem_type = gem["x"], gem["y"], gem["type"]
            self.game_data["board_status"][y][x] = gem_type
            if gem_type == 4:
                button = tk.Button(self.board_frame, image=self.icons[gem_type], bg=self.background_color,
                                command=lambda x=y, y=x: self.click_gem(x, y), bd=0)
            else:
                button = tk.Button(self.board_frame, image=self.icons[gem_type], bg=self.background_color,
                                command=lambda x=y, y=x: self.select_gem(x, y), bd=0)
            button.grid(row=y, column=x, padx=5, pady=5)

        if self.game_data["moves_left"] == 0:
            self.delete_current_game()
            self.game_over()

    # Creates the pause page.
    def pause_pressed(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        pause_page = PausePage(self.master, self.game_data, self.player_data)
        pause_page.run()

    # Draws a frame if 0 moves left with the open menu button.
    def game_over(self):
        rect_width = 700
        rect_height = 400
        rect_x0 = (self.master.winfo_width() - rect_width) // 2
        rect_y0 = (self.master.winfo_height() - rect_height) // 2

        overlay = tk.Frame(self.master, bg=self.background_color, relief="solid", bd=6)
        overlay.place(x=rect_x0, y=rect_y0, width=rect_width, height=rect_height)

        text_label = tk.Label(overlay,text="No moves left!", **self.button_label_options)
        text_label.pack(pady=60)

        back_button = tk.Button(overlay, text="Open Menu", command=self.open_menu, **self.second_button_label_options)
        back_button.pack(pady=40)

    # Handles the state when 0 moves left and deletes this game on the backend.
    def delete_current_game(self):
        try:
            response = requests.delete(f"{self.api_url}/menu/delete_game")
            response.raise_for_status()
            if response.status_code == 200:
                pass
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")
        except requests.RequestException as e:
            messagebox.showerror("Request Error", f"An error occurred: {e}")

    # Sends shuffle request to the backend.
    def shuffle(self):
        try:
            response = requests.get(f"{self.api_url}/board/shuffle")
            response.raise_for_status()

            if response.status_code == 200:
                self.game_data["board_status"] = response.json()["board_status"]
                self.print_board()
            else:
                messagebox.showerror("Error", f"Response code: {response.status_code}")

        except requests.RequestException as e:
            messagebox.showerror("Request Error", f"An error occurred: {e}")

    # Returns to the menu page.
    def open_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from .menu_page import MenuPage
        menu_page = MenuPage(self.master, self.player_data)
        menu_page.run()

    def run(self):
        self.create_widgets()
