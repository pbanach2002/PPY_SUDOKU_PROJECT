from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base  # używamy wspólnej bazy definicji

# Tworzenie silnika bazy danych
engine = create_engine('sqlite:///PPY_SUDOKU.db', echo=True)

# Sesja do komunikacji z bazą
SessionLocal = sessionmaker(bind=engine)

# Funkcja do inicjalizacji tabel – wywołasz ją w main.py
def init_db():
    from models import player, game_result  # <- dopiero tutaj import modeli
    Base.metadata.create_all(bind=engine)
