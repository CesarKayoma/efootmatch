from app.extensions import db
from app.models.base import BaseModel

class User(BaseModel):
    _tablename_ = "users"

    email = db.Column(
        db.String(255),
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="viewer"
    )