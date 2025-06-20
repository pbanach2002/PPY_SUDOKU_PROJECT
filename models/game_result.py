from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class GameResult(Base):
    __tablename__ = "game_results"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    score = Column(Integer, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    played_at = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="results")
