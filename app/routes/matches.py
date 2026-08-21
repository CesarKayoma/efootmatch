from flask import Blueprint, render_template

bp = Blueprint("matches", __name__)

@bp.route("/")
def home():
    return render_template("matches/index.html")