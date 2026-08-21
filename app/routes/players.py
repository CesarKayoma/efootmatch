from flask import Blueprint, render_template

bp = Blueprint("players", __name__)

@bp.route("/")
def home():
    return render_template("players/index.html")