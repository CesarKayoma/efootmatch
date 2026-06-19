from app.extensions import db
from app.models.base import BaseModel

class Goal(BaseModel):
    __tablename__ = "goals"

    own_goal = db.Column(
        db.Boolean,
        default=False
    )

    scorer_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=False
    )

    assister_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id")
    )

    match_id = db.Column(
        db.Integer,
        db.ForeignKey("matches.id"),
        nullable=False
    )

    player = db.relationship("Player", back_populates="goals")