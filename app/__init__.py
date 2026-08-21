from flask import Flask
from app.models import Goal, Match, Player, Team
from app.extensions import db, migrate
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.home import bp as home_bp
    from app.routes.matches import bp as matches_bp
    from app.routes.teams import bp as teams_bp
    from app.routes.players import bp as players_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(matches_bp, url_prefix="/matches")
    app.register_blueprint(teams_bp, url_prefix="/teams")
    app.register_blueprint(players_bp, url_prefix="/players")

    return app