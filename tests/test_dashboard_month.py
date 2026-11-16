import os
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from app import create_app
from app.extensions import db
from app.models import Goal, Match, Player, Team, User
from app.services.match_service import get_dashboard_stats, get_leaderboard_stats
from app.time_utils import format_local_date, utc_month_bounds


class DashboardMonthTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(
            os.environ,
            {"SECRET_KEY": "test-secret", "DATABASE_URL": "sqlite://"},
        )
        self.environment.start()
        self.app = create_app()
        self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.cesar = Team(name="César")
        self.breno = Team(name="Breno")
        db.session.add_all([self.cesar, self.breno])
        db.session.flush()
        self.cesar_player = Player(name="Jogador César", team_id=self.cesar.id)
        self.breno_player = Player(name="Jogador Breno", team_id=self.breno.id)
        self.user = User(
            email="test@example.com",
            password_hash="unused",
            role="admin",
        )
        db.session.add_all([self.cesar_player, self.breno_player, self.user])
        db.session.commit()

        self.client = self.app.test_client()
        with self.client.session_transaction() as session:
            session["_user_id"] = str(self.user.id)
            session["_fresh"] = True

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.environment.stop()

    def add_match(self, created_at, home_goals, away_goals):
        match = Match(
            created_at=created_at,
            man_of_the_match=self.cesar_player.id,
            home_team_id=self.cesar.id,
            away_team_id=self.breno.id,
        )
        db.session.add(match)
        db.session.flush()
        db.session.add_all(
            [
                Goal(
                    match_id=match.id,
                    scorer_id=self.cesar_player.id,
                    team_id=self.cesar.id,
                )
                for _ in range(home_goals)
            ]
            + [
                Goal(
                    match_id=match.id,
                    scorer_id=self.breno_player.id,
                    team_id=self.breno.id,
                )
                for _ in range(away_goals)
            ]
        )
        db.session.commit()

    def test_utc_timestamp_is_shown_as_local_game_date(self):
        utc_timestamp = datetime(2026, 11, 14, 1, 0, tzinfo=timezone.utc)
        naive_utc_timestamp = datetime(2026, 11, 14, 1, 0)

        self.assertEqual(format_local_date(utc_timestamp), "13/11/2026")
        self.assertEqual(format_local_date(naive_utc_timestamp), "13/11/2026")

    def test_month_filter_uses_local_calendar_boundaries(self):
        self.add_match(datetime(2026, 11, 1, 2, 59), 0, 1)
        self.add_match(datetime(2026, 11, 1, 3, 0), 1, 0)
        self.add_match(datetime(2026, 11, 14, 1, 0), 2, 1)

        start_at, end_at = utc_month_bounds(datetime(2026, 11, 1).date())
        stats = get_dashboard_stats(start_at=start_at, end_at=end_at)
        leaderboard = get_leaderboard_stats(
            start_at=start_at,
            end_at=end_at,
        )

        self.assertEqual(start_at, datetime(2026, 11, 1, 3, 0))
        self.assertEqual(end_at, datetime(2026, 12, 1, 3, 0))
        self.assertEqual(stats["total_matches"], 2)
        self.assertEqual(stats["cesar_wins"], 2)
        self.assertEqual(stats["breno_wins"], 0)
        self.assertEqual(stats["cesar_goals"], 3)
        self.assertEqual(stats["breno_goals"], 1)
        self.assertEqual(leaderboard["top_scorers"][0]["value"], 3)

        response = self.client.get("/?month=2026-11")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Dados de 11/2026.", response.text)
        self.assertIn("13/11/2026", response.text)
        self.assertNotIn("31/10/2026", response.text)
        self.assertNotIn("0 : 1", response.text)

        match_list = self.client.get("/matches/")
        self.assertIn("13/11/2026", match_list.text)
        self.assertNotIn("14/11/2026", match_list.text)

    def test_invalid_month_returns_bad_request(self):
        response = self.client.get("/?month=2026-13")
        self.assertEqual(response.status_code, 400)

    def test_match_form_focus_order_stays_keyboard_friendly(self):
        response = self.client.get("/matches/new")
        self.assertEqual(response.status_code, 200)

        control_ids = [
            "team-cesar",
            "scorer-input",
            "own-goal-checkbox",
            "add-goal-btn",
            "assist-input",
            "motm-input",
            "submit",
        ]
        positions = [response.text.index(f'id="{control_id}"') for control_id in control_ids]
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
