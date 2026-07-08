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

    return app