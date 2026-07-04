from app.extensions import db
from app.models.base import BaseModel

class Match(BaseModel):
    __tablename__ = "matches"

    man_of_the_match = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=False
    )

    motm_player = db.relationship("Player", back_populates="motm_matches")