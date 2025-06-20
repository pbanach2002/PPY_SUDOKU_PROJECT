import tkinter as tk
from tkinter import ttk
from db.database import SessionLocal
from models.game_result import GameResult
from models.player import Player
from datetime import datetime
from utils.pdf_export import export_results_to_pdf

class ScoreboardWindow(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.root = root
        self.controller = controller
        self.pack(padx=20, pady=20)

        tk.Label(self, text="Wyniki graczy", font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("gracz", "punkty", "czas", "data"), show="headings")
        self.tree.heading("gracz", text="Gracz")
        self.tree.heading("punkty", text="Punkty")
        self.tree.heading("czas", text="Czas (s)")
        self.tree.heading("data", text="Data")

        self.tree.pack()

        self.load_results()

        tk.Button(self, text="Powrót", command=self.controller.show_game_screen).pack(pady=10)
        tk.Button(self, text="Eksportuj do PDF", command=self.export_pdf).pack(pady=5)

    def export_pdf(self):
        export_results_to_pdf()
        from tkinter import messagebox
        messagebox.showinfo("Eksport zakończony", "Plik PDF został zapisany jako 'wyniki.pdf'")

    def load_results(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        with SessionLocal() as session:
            results = (
                session.query(GameResult)
                .join(Player)
                .order_by(GameResult.score.desc())
                .all()
            )
            for result in results:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        result.player.username,
                        result.score,
                        result.duration_seconds,
                        result.played_at.strftime("%Y-%m-%d %H:%M")
                    )
                )
