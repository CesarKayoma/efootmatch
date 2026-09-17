from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app.auth import admin_required
from app.forms.player import PlayerForm
from app.services import player_service

bp = Blueprint("players", __name__)


@bp.route("/")
@login_required
def home():
    cesar_team, breno_team = player_service.list_players_by_team()
    return render_template(
        "players/index.html",
        cesar_team=cesar_team,
        breno_team=breno_team,
    )


@bp.route("/new", methods=["GET", "POST"])
@admin_required
def new():
    form = PlayerForm()

    if form.validate_on_submit():
        player_service.create_player(
            name=form.name.data,
            team_id=form.team_id.data,
        )
        flash("Jogador cadastrado com sucesso!", "success")
        return redirect(url_for("players.home"))

    return render_template("players/form.html", form=form, player=None)


@bp.route("/<int:player_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(player_id):
    player = player_service.get_player_or_404(player_id)
    form = PlayerForm(player=player)

    if form.validate_on_submit():
        player_service.update_player(
            player_id=player.id,
            name=form.name.data,
            team_id=form.team_id.data,
        )
        flash("Jogador atualizado com sucesso!", "success")
        return redirect(url_for("players.home"))

    if request.method == "GET":
        form.name.data = player.name
        form.team_id.data = player.team_id

    return render_template("players/form.html", form=form, player=player)


@bp.route("/<int:player_id>/delete", methods=["POST"])
@admin_required
def delete(player_id):
    try:
        player_service.delete_player(player_id)
        flash("Jogador excluído.", "success")
    except player_service.PlayerValidationError as error:
        flash(str(error), "error")

    return redirect(url_for("players.home"))