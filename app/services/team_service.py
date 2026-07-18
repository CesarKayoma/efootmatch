from app.extensions import db
from app.models import Team

def get_teams():
    return Team.query.all()

def get_team(team_id):
    return Team.query.get_or_404(team_id)