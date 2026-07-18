from app.extensions import db
from app.models.base import BaseModel

class Match(BaseModel):
    __tablename__ = "matches"

    man_of_the_match = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=False
    )

    home_team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    away_team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    motm_player = db.relationship("Player", back_populates="motm_matches")

    match_goals = db.relationship("Goal", back_populates="match")

    home_team = db.relationship(
        "Team", foreign_keys=[home_team_id], back_populates="matches_home"
    )
    
    away_team = db.relationship(
        "Team", foreign_keys=[away_team_id], back_populates="matches_away"
    )