#Author: Movsesian Lilit - xmovse00
import tkinter as tk
from tkinter import PhotoImage

class LeaderPage:
    # Initializes the page.
    def __init__(self, master, leader_data, player_data):
        self.master = master
        self.background_color = "#ffe500"
        self.leader_data = leader_data
        self.player_data = player_data
        self.current_page = 0
        self.items_per_page = 5
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.img_lab = PhotoImage(file="assets/images/lab.png")
        self.img_person = PhotoImage(file="assets/images/user.png").subsample(2, 2)
        self.img_left_arrow = PhotoImage(file="assets/images/larr.png")
        self.img_right_arrow = PhotoImage(file="assets/images/rarr.png")
        self.button_label_options = {
            "font": ("Press Start 2P", 24),
            "bg": self.background_color,
            "fg": "black",
            "bd": 0,
        }
        
    # Creates widgets.
    def create_widgets(self):
        main_frame = tk.Frame(self.master, bg=self.background_color)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        for i in range(2):
            main_frame.rowconfigure(i, weight=1)

        self.left_frame = tk.Frame(main_frame, bg=self.background_color)
        self.left_frame.grid(row=0, column=0, sticky="w", pady=100, padx=280)

        for i in range(3):
            self.left_frame.columnconfigure(i, weight=1)
        for i in range(5):
            self.left_frame.rowconfigure(i, weight=1)

        right_frame = tk.Frame(main_frame, bg=self.background_color)
        right_frame.grid(row=0, column=1, sticky="nse")
        
        right_frame.config(width=400, height=500)
        right_frame.grid_propagate(False)

        img_lab_label = tk.Label(right_frame, image=self.img_lab, bg=self.background_color)
        img_lab_label.place(x=210, y=400, anchor="center")

        nav_frame = tk.Frame(self.master, bg=self.background_color)
        nav_frame.place(relx=0.35, rely=0.9, anchor="center")
        
        nav_frame.columnconfigure(0, weight=1)
        for i in range(3):
            nav_frame.rowconfigure(i, weight=1)
        
        self.left_button = tk.Button(nav_frame, image=self.img_left_arrow, command=self.previous_page, **self.button_label_options)
        self.left_button.grid(row=0, column=0, padx=20)
        
        self.page_label = tk.Label(nav_frame, text="", **self.button_label_options)
        self.page_label.grid(row=0, column=1, padx=20)
        
        self.right_button = tk.Button(nav_frame, image=self.img_right_arrow, command=self.next_page, **self.button_label_options)
        self.right_button.grid(row=0, column=2, padx=20)

        back_btn = tk.Button(self.master, text="Back", command=self.open_menu, **self.button_label_options)
        back_btn.place(relx=0.05, rely=0.95, anchor="sw")
        
        self.update_display()


     # Updates the leaderboard display based on the current page.
    def update_display(self):
        # Clear the previous leaderboard.
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Determine the range of leaders to display based on the current page.
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page
        leaders_to_display = self.leader_data[start_index:end_index]

        # Add leader information to the left frame.
        for i, leader in enumerate(leaders_to_display):
            img_label = tk.Label(self.left_frame, image=self.img_person, bg=self.background_color)
            img_label.grid(row=i, column=0, sticky="w", padx=0)

            leader_label = tk.Label(self.left_frame, text=f" {leader['login']}", **self.button_label_options)
            leader_label.grid(row=i, column=1, sticky="w")
            score_label = tk.Label(self.left_frame, text=f"{leader['highest_score']}", **self.button_label_options)
            score_label.grid(row=i, column=2, sticky="e")

            entry_underline = tk.Label(self.left_frame, text=" ------------- ", **self.button_label_options)
            entry_underline.grid(row=i, column=1, columnspan=2, sticky="w", pady=(70,0))

        # Calculate and display the total number of pages.
        total_pages = (len(self.leader_data) - 1) // self.items_per_page + 1
        self.page_label.config(text=f"{self.current_page + 1} / {total_pages}")

        # Disable the left arrow button if on the first page and the right arrow button if on the last page.
        self.left_button.config(state="normal" if self.current_page > 0 else "disabled")
        self.right_button.config(state="normal" if self.current_page < total_pages - 1 else "disabled")

    # Go to the previous page in the leaderboard.
    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    # Go to the next page in the leaderboard.
    def next_page(self):
        total_pages = (len(self.leader_data) - 1) // self.items_per_page + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_display()

    # Returns to the menu page.
    def open_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from .menu_page import MenuPage
        menu_page = MenuPage(self.master, self.player_data)
        menu_page.run()

    def run(self):
        self.create_widgets()