from app.extensions import db
from app.models.base import BaseModel

class Player(BaseModel):
    __tablename__ = "players"

    name = db.Column(
        db.String(100),
        nullable=False,
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False,
    )

    matches = db.relationship("Match", back_populates="player")
    team = db.relationship("Team", back_populates="players")
    goals = db.relationship("Goal", back_populates="player")