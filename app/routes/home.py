import re
from datetime import date

from flask import Blueprint, abort, render_template, request
from flask_login import login_required

from app.services.match_service import (
    get_dashboard_stats,
    get_leaderboard_stats,
    get_recent_matches,
)
from app.time_utils import utc_month_bounds

bp = Blueprint("home", __name__)


def _parse_month(value):
    if not value:
        return None
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", value):
        abort(400, description="O mês deve estar no formato AAAA-MM.")

    try:
        month = date.fromisoformat(value + "-01")
    except ValueError:
        abort(400, description="O mês informado é inválido.")

    if month.year == date.max.year and month.month == 12:
        abort(400, description="O mês informado está fora do intervalo permitido.")
    return month


@bp.route("/")
@login_required
def home():
    selected_month = request.args.get("month", "")
    month = _parse_month(selected_month)
    start_at, end_at = utc_month_bounds(month) if month else (None, None)

    stats = get_dashboard_stats(start_at=start_at, end_at=end_at)
    leaderboard = get_leaderboard_stats(
        limit=5,
        start_at=start_at,
        end_at=end_at,
    )
    recent_matches = get_recent_matches(
        limit=5,
        start_at=start_at,
        end_at=end_at,
    )
    return render_template(
        "home/index.html",
        stats=stats,
        leaderboard=leaderboard,
        recent_matches=recent_matches,
        selected_month=selected_month,
    )