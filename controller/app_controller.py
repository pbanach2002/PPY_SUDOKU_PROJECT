import tkinter as tk
from gui.login import LoginWindow

class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Multiplayer")
        self.current_frame = None
        self.current_user = None

        self.show_login_screen()  # ← wywołanie metody

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_login_screen(self):
        self.clear_frame()
        self.current_frame = LoginWindow(self.root, self)

    def show_game_screen(self):
        from gui.game import GameWindow
        self.clear_frame()
        self.current_frame = GameWindow(
            self.root,
            self,
            difficulty=self.difficulty if hasattr(self, "difficulty") else "medium"
        )

    def run(self):
        self.root.mainloop()

    def show_scoreboard(self):
        from gui.scoreboard import ScoreboardWindow
        self.clear_frame()
        self.current_frame = ScoreboardWindow(self.root, self)

    def show_settings_screen(self):
        from gui.settings import SettingsWindow
        self.clear_frame()
        self.current_frame = SettingsWindow(self.root, self)