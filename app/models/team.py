from app.extensions import db
from app.models.base import BaseModel

class Team(BaseModel):
    __tablename__ = "teams"

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )