from collections import Counter

from sqlalchemy import select

from app.extensions import db
from app.models import Match, Goal, Team


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
    matches = Match.query.all()

    total_matches = len(matches)

    cesar_wins = 0
    breno_wins = 0
    draws = 0

    cesar_goals = 0
    breno_goals = 0

    for match in matches:
        home_score = sum(
            1 for goal in match.match_goals
            if goal.team_id == match.home_team_id
        )

        away_score = sum(
            1 for goal in match.match_goals
            if goal.team_id == match.away_team_id
        )

        if match.home_team.name == "César":
            cesar_score, breno_score = home_score, away_score
        else:
            cesar_score, breno_score = away_score, home_score

        cesar_goals += cesar_score
        breno_goals += breno_score

        if cesar_score > breno_score:
            cesar_wins += 1
        elif breno_score > cesar_score:
            breno_wins += 1
        else:
            draws += 1

    return {
        "total_matches": total_matches,
        "cesar_wins": cesar_wins,
        "breno_wins": breno_wins,
        "cesar_goals": cesar_goals,
        "breno_goals": breno_goals,
        "draws": draws,
    }


def get_leaderboard_stats(limit=10):
    """
    Calcula os rankings de jogadores pro dashboard:
    artilharia, assistências, MOTM e participações em gol (gols + assistências).

    Gol contra não conta na artilharia pessoal do jogador nem nas participações.
    """
    goals = Goal.query.all()
    matches = Match.query.all()

    scorer_counts = Counter()
    assister_counts = Counter()
    participation_counts = Counter()
    motm_counts = Counter()

    player_info = {}  # player_id -> (name, team_name)

    for goal in goals:
        if not goal.own_goal:
            scorer_counts[goal.scorer_id] += 1
            participation_counts[goal.scorer_id] += 1
            player_info[goal.scorer_id] = (goal.scorer.name, goal.scorer.team.name)

        if goal.assister_id:
            assister_counts[goal.assister_id] += 1
            participation_counts[goal.assister_id] += 1
            player_info[goal.assister_id] = (goal.assister.name, goal.assister.team.name)

    for match in matches:
        motm_id = match.man_of_the_match
        motm_counts[motm_id] += 1
        player_info.setdefault(
            motm_id, (match.motm_player.name, match.motm_player.team.name)
        )

    def build_ranking(counter):
        return [
            {
                "player_name": player_info[player_id][0],
                "team_name": player_info[player_id][1],
                "value": value,
            }
            for player_id, value in counter.most_common(limit)
        ]

    return {
        "top_scorers": build_ranking(scorer_counts),
        "top_assisters": build_ranking(assister_counts),
        "top_motm": build_ranking(motm_counts),
        "top_participations": build_ranking(participation_counts),
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