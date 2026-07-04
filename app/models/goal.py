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

    __table_args__ = (
        db.CheckConstraint(
            "assister_id IS NULL OR scorer_id != assister_id",
            name="check_scorer_is_not_assister"
        ),
    )

    scorer = db.relationship(
        "Player", foreign_keys=[scorer_id], back_populates="scored_goals"
    )
    assister = db.relationship(
        "Player", foreign_keys=[assister_id], back_populates="assisted_goals"
    )