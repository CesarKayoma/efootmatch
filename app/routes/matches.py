from flask import Blueprint, render_template, request

from app.services import match_service

bp = Blueprint("matches", __name__)

@bp.route("/")
def home():
    matches = match_service.list_matches()
    return {
        "matches": [
            {
                "id": match.id,
                "motm": match.man_of_the_match,
                "match_date": match.created_at,
            }
            for match in matches
        ]
    }