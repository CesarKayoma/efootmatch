from flask import Blueprint, render_template

from app.services.match_service import get_dashboard_stats, get_leaderboard_stats

bp = Blueprint("home", __name__)

@bp.route("/")
def home():
    stats = get_dashboard_stats()
    leaderboard = get_leaderboard_stats()
    return render_template("home/index.html", stats=stats, leaderboard=leaderboard)