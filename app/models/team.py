from app.extensions import db
from app.models.base import BaseModel

class Team(BaseModel):
    __tablename__ = "teams"

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    players = db.relationship("Player", back_populates="team")

    matches_home = db.relationship("Match", foreign_keys="[Match.home_team_id]", back_populates="home_team")
    matches_away = db.relationship("Match", foreign_keys="[Match.away_team_id]", back_populates="away_team")