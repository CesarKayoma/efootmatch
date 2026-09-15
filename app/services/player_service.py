from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Player, Team


class PlayerValidationError(Exception):
    """Erro de validação de negócio ao criar/editar/excluir um jogador."""
    pass


def list_players_by_team():
    """Retorna (time_cesar, time_breno) já com o relacionamento .players carregado."""
    cesar = Team.query.filter_by(name="César").first()
    breno = Team.query.filter_by(name="Breno").first()

    if not cesar or not breno:
        raise PlayerValidationError(
            "Times 'César' e 'Breno' precisam existir cadastrados no banco."
        )

    return cesar, breno


def get_player_or_404(player_id):
    return Player.query.get_or_404(player_id)


def create_player(name, team_id):
    player = Player(name=name, team_id=team_id)
    db.session.add(player)
    db.session.commit()
    return player


def update_player(player_id, name, team_id):
    player = get_player_or_404(player_id)
    player.name = name
    player.team_id = team_id
    db.session.commit()
    return player


def delete_player(player_id):
    player = get_player_or_404(player_id)

    try:
        db.session.delete(player)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise PlayerValidationError(
            f"Não é possível excluir {player.name}: ele já tem gols, "
            "assistências ou MOTM registrados em alguma partida."
        )