import tkinter as tk

class SettingsWindow(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.root = root
        self.controller = controller
        self.pack(padx=20, pady=20)

        tk.Label(self, text="Ustawienia gry", font=("Arial", 16)).pack(pady=10)

        # Liczba graczy
        tk.Label(self, text="Liczba graczy:").pack()
        self.player_count = tk.IntVar(value=1)
        player_menu = tk.OptionMenu(self, self.player_count, 1, 2, 3, 4)
        player_menu.pack(pady=5)

        # Poziom trudności
        tk.Label(self, text="Poziom trudności:").pack()
        self.difficulty = tk.StringVar(value="medium")
        diff_menu = tk.OptionMenu(self, self.difficulty, "easy", "medium", "hard")
        diff_menu.pack(pady=5)

        tk.Button(self, text="Rozpocznij grę", command=self.start_game).pack(pady=10)
        tk.Button(self, text="Wróć", command=self.controller.show_login_screen).pack()

    def start_game(self):
        self.controller.difficulty = self.difficulty.get()
        self.controller.player_count = self.player_count.get()
        self.controller.show_game_screen()
