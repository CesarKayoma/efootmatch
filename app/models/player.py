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

    __table_args__ = (
        db.UniqueConstraint("name", "team_id", name="unique_player_name_team"),
    )

    motm_matches = db.relationship("Match", back_populates="motm_player")
    team = db.relationship("Team", back_populates="players")

    scored_goals = db.relationship("Goal", foreign_keys="[Goal.scorer_id]", back_populates="scorer")
    assisted_goals = db.relationship("Goal", foreign_keys="[Goal.assister_id]", back_populates="assister")