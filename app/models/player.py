from app.extensions import db
from app.models.base import BaseModel

class Player(BaseModel):
    __tablename__ = "players"

    name = db.Column(
        db.String(100),
        nullable=False,
    )