from flask import Blueprint, render_template
from flask_login import login_required

from app.services.match_service import get_dashboard_stats, get_leaderboard_stats

bp = Blueprint("home", __name__)

@bp.route("/")
@login_required
def home():
    stats = get_dashboard_stats()
    leaderboard = get_leaderboard_stats(limit=5)
    return render_template("home/index.html", stats=stats, leaderboard=leaderboard)