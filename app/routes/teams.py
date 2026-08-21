from flask import Blueprint, render_template

bp = Blueprint("teams", __name__)

@bp.route("/")
def home():
    return render_template("teams/index.html")