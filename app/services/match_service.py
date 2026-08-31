from app.extensions import db
from app.models import Match

def list_matches():
    query = Match.query.all()

    return query