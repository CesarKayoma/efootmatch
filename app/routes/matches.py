import json

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app.auth import admin_required
from app.forms.match import MatchForm
from app.services import match_service

bp = Blueprint("matches", __name__)


@bp.route("/")
@login_required
def home():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 50)
    page = max(page, 1)
    per_page = max(per_page, 1)
    matches = match_service.list_matches(page=page, per_page=per_page)
    return render_template("matches/index.html", matches=matches)


@bp.route("/new", methods=["GET", "POST"])
@admin_required
def new():
    form = MatchForm()
    context = match_service.get_form_context()

    if form.validate_on_submit():
        try:
            goals = json.loads(form.goals_json.data or "[]")

            match_service.create_match(
                motm_player_id=int(form.motm_player_id.data),
                goals=goals,
            )

            flash("Partida registrada com sucesso!", "success")
            return redirect(url_for("matches.home"))

        except match_service.MatchValidationError as error:
            flash(str(error), "error")

    return render_template(
        "matches/form.html",
        form=form,
        match=None,
        existing_goals=[],
        motm_player=None,
        **context,
    )


@bp.route("/<int:match_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(match_id):
    match = match_service.get_match_or_404(match_id)
    form = MatchForm()
    context = match_service.get_form_context()

    if form.validate_on_submit():
        try:
            goals = json.loads(form.goals_json.data or "[]")

            match_service.update_match(
                match_id=match.id,
                motm_player_id=int(form.motm_player_id.data),
                goals=goals,
            )

            flash("Partida atualizada com sucesso!", "success")
            return redirect(url_for("matches.home"))

        except match_service.MatchValidationError as error:
            flash(str(error), "error")

    if request.method == "GET":
        form.motm_player_id.data = str(match.man_of_the_match)

    existing_goals = [
        {
            "team_id": goal.team_id,
            "scorer_id": goal.scorer_id,
            "scorer_name": goal.scorer.name,
            "assister_id": goal.assister_id,
            "assister_name": goal.assister.name if goal.assister else None,
            "own_goal": goal.own_goal,
        }
        for goal in match.match_goals
    ]

    return render_template(
        "matches/form.html",
        form=form,
        match=match,
        existing_goals=existing_goals,
        motm_player=match.motm_player,
        **context,
    )


@bp.route("/<int:match_id>/delete", methods=["POST"])
@admin_required
def delete(match_id):
    match_service.delete_match(match_id)
    flash("Partida excluída.", "success")
    return redirect(url_for("matches.home"))