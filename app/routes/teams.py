from flask import Blueprint, render_template
from flask_login import login_required

from app.services import team_service

bp = Blueprint("teams", __name__)

@bp.route("/")
@login_required
def home():
    teams = team_service.get_teams()
    return render_template("teams/index.html", teams=teams)