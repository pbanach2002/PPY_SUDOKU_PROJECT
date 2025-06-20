import tkinter as tk
from tkinter import messagebox
from db.database import SessionLocal
from db.encryption import hash_password, verify_password
from models.player import Player

class LoginWindow(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.root = root
        self.pack(padx=10, pady=10)

        tk.Label(self, text="Login").grid(row=0, column=0, sticky="e")
        tk.Label(self, text="Hasło").grid(row=1, column=0, sticky="e")

        self.username_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self, text="Zaloguj", command=self.login)
        self.register_button = tk.Button(self, text="Zarejestruj", command=self.register)

        self.login_button.grid(row=2, column=0, pady=5)
        self.register_button.grid(row=2, column=1, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with SessionLocal() as session:
            user = session.query(Player).filter_by(username=username).first()
            if user and verify_password(password, user.password_hash.encode()):
                messagebox.showinfo("Sukces!", f"Zalogowano jako {username}")
                self.controller.current_user = user
                self.controller.show_game_screen()
                self.controller.show_settings_screen()
            else:
                messagebox.showerror("Błąd!", "Nieprawidłowy login lub hasło.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if len(password) < 6:
            messagebox.showerror("Błąd!", "Hasło musi zawierać co najmniej 6 znaków.")
            return

        with SessionLocal() as session:
            if session.query(Player).filter_by(username=username).first():
                messagebox.showerror("Błąd!", "Użytkownik już istnieje.")
                return

            hashed = hash_password(password).decode()
            user = Player(username=username, password_hash=hashed)
            session.add(user)
            session.commit()
            messagebox.showinfo("Sukces!", "Rejestracja zakończona.")
