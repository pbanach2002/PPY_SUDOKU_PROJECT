from logic.sudoku_generator import generate_puzzle
import tkinter as tk
from tkinter import messagebox
from functools import partial
from db.database import SessionLocal
from models.game_result import GameResult

class GameWindow(tk.Frame):
    def __init__(self, root, controller, difficulty="medium"):
        super().__init__(root)
        self.root = root
        self.controller = controller
        self.user = controller.current_user
        self.difficulty = difficulty

        self.pack(padx=20, pady=20)
        tk.Label(self, text=f"Witaj, {self.user.username}!", font=("Arial", 16)).pack(pady=10)

        self.board_frame = tk.Frame(self)
        self.board_frame.pack()

        self.entries = []
        self.entry_vars = []
        self.evaluated_cells = set()
        self.error_cells = set()
        self.score = 0
        self.timer_seconds = 0
        self.handling_input = False

        num_visible = {"easy": 50, "medium": 40, "hard": 30}.get(self.difficulty, 40)
        self.puzzle, self.solution = generate_puzzle(num_visible=num_visible)

        self.score_label = tk.Label(self, text="Punkty: 0", font=("Arial", 12))
        self.score_label.pack()

        self.timer_label = tk.Label(self, text="Czas: 00:00", font=("Arial", 12))
        self.timer_label.pack()

        self.create_board()
        self.fill_board()

        self.back_button = tk.Button(self, text="Wyloguj", command=self.logout)
        self.back_button.pack(pady=10)

        self.scoreboard_button = tk.Button(self, text="Wyniki", command=self.controller.show_scoreboard)
        self.scoreboard_button.pack(pady=5)

        self.update_timer()

    def create_board(self):
        def validate_input(new_value):
            if new_value == "":
                return True
            return new_value.isdigit() and 1 <= int(new_value) <= 9 and len(new_value) == 1

        vcmd = (self.register(validate_input), "%P")

        for r in range(9):
            row_entries = []
            row_vars = []
            for c in range(9):
                var = tk.StringVar()

                entry = tk.Entry(
                    self.board_frame,
                    width=2,
                    font=("Arial", 18),
                    justify="center",
                    textvariable=var,
                    validate="key",
                    validatecommand=vcmd,
                    bg="#f4f4f4"
                )

                var.trace_add("write", partial(self.handle_input, var, r, c))

                entry.bind("<FocusIn>", lambda e: self.set_input_flag(True))
                entry.bind("<FocusOut>", lambda e: self.set_input_flag(False))

                entry.grid(row=r, column=c, padx=2, pady=2)
                if r % 3 == 0 and r != 0:
                    entry.grid_configure(pady=(6, 2))
                if c % 3 == 0 and c != 0:
                    entry.grid_configure(padx=(6, 2))

                row_entries.append(entry)
                row_vars.append(var)

            self.entries.append(row_entries)
            self.entry_vars.append(row_vars)

    def set_input_flag(self, state):
        self.handling_input = state

    def handle_input(self, var, row, col, *args):
        if not self.handling_input:
            return

        val = var.get()
        entry = self.entries[row][col]
        correct = self.solution[row][col]

        if val == "":
            entry.config(bg="#f4f4f4")
            return

        try:
            value = int(val)
        except ValueError:
            return

        if (row, col) in self.evaluated_cells:
            return

        if value == correct:
            if (row, col) in self.error_cells:
                entry.delete(0, tk.END)
                entry.insert(0, str(value))
                entry.config(
                    state="disabled",
                    disabledforeground="black",
                    disabledbackground="lightgreen"
                )
                self.error_cells.remove((row, col))
            else:
                self.score += 10
                entry.delete(0, tk.END)
                entry.insert(0, str(value))
                entry.config(
                    disabledbackground="lightgreen",
                    disabledforeground="black"
                )
                entry.config(state="disabled")
            self.evaluated_cells.add((row, col))
            self.score_label.config(text=f"Punkty: {self.score}")
        else:
            if (row, col) not in self.error_cells:
                self.score -= 10
                self.error_cells.add((row, col))
                self.score_label.config(text=f"Punkty: {self.score}")
            entry.config(bg="red")

    def fill_board(self):
        for r in range(9):
            for c in range(9):
                value = self.puzzle[r][c]
                entry = self.entries[r][c]
                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state="disabled", disabledforeground="black", bg="#d9d9d9")
                else:
                    entry.config(bg="#f4f4f4")

    def update_timer(self):
        mins = self.timer_seconds // 60
        secs = self.timer_seconds % 60
        self.timer_label.config(text=f"Czas: {mins:02d}:{secs:02d}")
        self.timer_seconds += 1
        self.after(1000, self.update_timer)

    def logout(self):
        with SessionLocal() as session:
            result = GameResult(
                player_id=self.user.id,
                score=self.score,
                duration_seconds=self.timer_seconds
            )
            session.add(result)
            session.commit()

        self.controller.current_user = None
        self.controller.show_login_screen()
