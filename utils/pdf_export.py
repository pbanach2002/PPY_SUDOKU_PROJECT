from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from db.database import SessionLocal
from models.game_result import GameResult
from models.player import Player

def export_results_to_pdf(filename="wyniki.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Wyniki Graczy Sudoku")

    c.setFont("Helvetica", 12)
    y = height - 100

    headers = ["Gracz", "Punkty", "Czas (s)", "Data"]
    for i, header in enumerate(headers):
        c.drawString(50 + i * 120, y, header)
    y -= 20

    with SessionLocal() as session:
        results = (
            session.query(GameResult)
            .join(Player)
            .order_by(GameResult.score.desc())
            .all()
        )

        for result in results:
            row = [
                result.player.username,
                str(result.score),
                str(result.duration_seconds),
                result.played_at.strftime("%Y-%m-%d %H:%M")
            ]
            for i, value in enumerate(row):
                c.drawString(50 + i * 120, y, value)
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50

    c.save()
