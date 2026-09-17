from sqlalchemy import case, func, or_, select

from app.extensions import db
from app.models import Goal, Match, Player, Team


class MatchValidationError(Exception):
    """Erro de validação de negócio ao criar/editar uma partida."""
    pass


def list_matches(page=1, per_page=10):
    pagination = db.paginate(
        select(Match).order_by(Match.created_at.desc(), Match.id.desc()),
        page=page,
        per_page=per_page,
        error_out=False,
    )

    for match in pagination.items:
        home_score = sum(
            1 for goal in match.match_goals
            if goal.team_id == match.home_team_id
        )

        away_score = sum(
            1 for goal in match.match_goals
            if goal.team_id == match.away_team_id
        )

        match.home_score = home_score
        match.away_score = away_score

    return pagination


def get_dashboard_stats():
    match_scores = (
        select(
            Match.id,
            Team.name.label("home_team_name"),
            func.sum(
                case((Goal.team_id == Match.home_team_id, 1), else_=0)
            ).label("home_score"),
            func.sum(
                case((Goal.team_id == Match.away_team_id, 1), else_=0)
            ).label("away_score"),
        )
        .join(Team, Team.id == Match.home_team_id)
        .outerjoin(Goal, Goal.match_id == Match.id)
        .group_by(Match.id, Team.name)
        .subquery()
    )

    cesar_score = case(
        (match_scores.c.home_team_name == "César", match_scores.c.home_score),
        else_=match_scores.c.away_score,
    )
    breno_score = case(
        (match_scores.c.home_team_name == "César", match_scores.c.away_score),
        else_=match_scores.c.home_score,
    )
    stats = db.session.execute(
        select(
            func.count(match_scores.c.id),
            func.coalesce(func.sum(case((cesar_score > breno_score, 1), else_=0)), 0),
            func.coalesce(func.sum(case((breno_score > cesar_score, 1), else_=0)), 0),
            func.coalesce(func.sum(case((cesar_score == breno_score, 1), else_=0)), 0),
            func.coalesce(func.sum(cesar_score), 0),
            func.coalesce(func.sum(breno_score), 0),
        )
    ).one()

    return {
        "total_matches": stats[0],
        "cesar_wins": stats[1],
        "breno_wins": stats[2],
        "cesar_goals": stats[4],
        "breno_goals": stats[5],
        "draws": stats[3],
    }


def get_leaderboard_stats(limit=10):
    """
    Calcula os rankings de jogadores pro dashboard:
    artilharia, assistências, MOTM e participações em gol (gols + assistências).

    Gol contra não conta na artilharia pessoal do jogador nem nas participações.
    """
    def ranking(query):
        return [
            {
                "player_name": player_name,
                "team_name": team_name,
                "value": value,
            }
            for player_name, team_name, value in db.session.execute(
                query.order_by(db.desc("value"), Player.id).limit(limit)
            )
        ]

    scorer_query = (
        select(
            Player.name,
            Team.name,
            func.count(Goal.id).label("value"),
        )
        .join(Goal, Goal.scorer_id == Player.id)
        .join(Team, Team.id == Player.team_id)
        .where(or_(Goal.own_goal.is_(False), Goal.own_goal.is_(None)))
        .group_by(Player.id, Player.name, Team.name)
    )
    assister_query = (
        select(
            Player.name,
            Team.name,
            func.count(Goal.id).label("value"),
        )
        .join(Goal, Goal.assister_id == Player.id)
        .join(Team, Team.id == Player.team_id)
        .group_by(Player.id, Player.name, Team.name)
    )
    motm_query = (
        select(
            Player.name,
            Team.name,
            func.count(Match.id).label("value"),
        )
        .join(Match, Match.man_of_the_match == Player.id)
        .join(Team, Team.id == Player.team_id)
        .group_by(Player.id, Player.name, Team.name)
    )
    participation_query = (
        select(
            Player.name,
            Team.name,
            func.count(Goal.id).label("value"),
        )
        .join(
            Goal,
            (Goal.scorer_id == Player.id)
            | (Goal.assister_id == Player.id),
        )
        .join(Team, Team.id == Player.team_id)
        .where(
            (Goal.assister_id == Player.id)
            | ((Goal.scorer_id == Player.id)
               & or_(Goal.own_goal.is_(False), Goal.own_goal.is_(None)))
        )
        .group_by(Player.id, Player.name, Team.name)
    )

    return {
        "top_scorers": ranking(scorer_query),
        "top_assisters": ranking(assister_query),
        "top_motm": ranking(motm_query),
        "top_participations": ranking(participation_query),
    }


# =========================
# CRUD de partidas
# =========================

def get_cesar_breno_teams():
    """Retorna (time_cesar, time_breno). A liga é fixa entre esses dois times."""
    cesar = Team.query.filter_by(name="César").first()
    breno = Team.query.filter_by(name="Breno").first()

    if not cesar or not breno:
        raise MatchValidationError(
            "Times 'César' e 'Breno' precisam existir cadastrados no banco."
        )

    return cesar, breno


def get_match_or_404(match_id):
    return Match.query.get_or_404(match_id)


def get_form_context():
    """
    Monta os dados que o template do formulário precisa:
    times fixos, jogadores por time e lista completa de jogadores (pro MOTM).
    """
    cesar, breno = get_cesar_breno_teams()

    players_by_team = {
        cesar.id: [{"id": p.id, "name": p.name} for p in cesar.players],
        breno.id: [{"id": p.id, "name": p.name} for p in breno.players],
    }

    all_players = players_by_team[cesar.id] + players_by_team[breno.id]

    return {
        "cesar_team": cesar,
        "breno_team": breno,
        "players_by_team": players_by_team,
        "all_players": all_players,
    }


def _validate_goals(goals, cesar_id, breno_id):
    if not isinstance(goals, list):
        raise MatchValidationError("Formato de gols inválido.")

    valid_team_ids = (cesar_id, breno_id)

    for goal in goals:
        team_id = goal.get("team_id")
        scorer_id = goal.get("scorer_id")
        assister_id = goal.get("assister_id")

        if team_id not in valid_team_ids:
            raise MatchValidationError("Um dos gols tem um time inválido.")

        if not scorer_id:
            raise MatchValidationError("Todo gol precisa de um autor.")

        if assister_id and assister_id == scorer_id:
            raise MatchValidationError(
                "O autor do gol não pode ser também o assistente."
            )


def _replace_goals(match, goals):
    Goal.query.filter_by(match_id=match.id).delete()

    for goal in goals:
        own_goal = bool(goal.get("own_goal", False))

        db.session.add(Goal(
            match_id=match.id,
            team_id=goal["team_id"],
            scorer_id=goal["scorer_id"],
            # Gol contra não carrega assistência
            assister_id=None if own_goal else goal.get("assister_id"),
            own_goal=own_goal,
        ))


def create_match(motm_player_id, goals):
    cesar, breno = get_cesar_breno_teams()
    _validate_goals(goals, cesar.id, breno.id)

    match = Match(
        man_of_the_match=motm_player_id,
        home_team_id=cesar.id,
        away_team_id=breno.id,
    )

    db.session.add(match)
    db.session.flush()  # garante match.id antes de criar os gols

    _replace_goals(match, goals)

    db.session.commit()
    return match


def update_match(match_id, motm_player_id, goals):
    cesar, breno = get_cesar_breno_teams()
    _validate_goals(goals, cesar.id, breno.id)

    match = get_match_or_404(match_id)
    match.man_of_the_match = motm_player_id

    _replace_goals(match, goals)

    db.session.commit()
    return match


def delete_match(match_id):
    match = get_match_or_404(match_id)

    Goal.query.filter_by(match_id=match.id).delete()
    db.session.delete(match)
    db.session.commit()