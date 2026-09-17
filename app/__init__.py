from flask import Flask
from app.models import Goal, Match, Player, Team, User
from app.extensions import csrf, db, login_manager, migrate
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.json.ensure_ascii = False

    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY must be configured.")
    app.config["SECRET_KEY"] = secret_key

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URL must be configured.")
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.home import bp as home_bp
    from app.routes.matches import bp as matches_bp
    from app.routes.teams import bp as teams_bp
    from app.routes.players import bp as players_bp
    from app.routes.auth import bp as auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(matches_bp, url_prefix="/matches")
    app.register_blueprint(teams_bp, url_prefix="/teams")
    app.register_blueprint(players_bp, url_prefix="/players")

    @app.cli.command("seed-users")
    def seed_users():
        """Create or update the admin and viewer users from environment variables."""
        users = (
            ("ADMIN_EMAIL", "ADMIN_PASSWORD", "admin"),
            ("VIEWER_EMAIL", "VIEWER_PASSWORD", "viewer"),
        )
        for email_key, password_key, role in users:
            email = os.environ.get(email_key)
            password = os.environ.get(password_key)
            if not email or not password:
                raise RuntimeError(
                    f"{email_key} and {password_key} must be configured."
                )

            email = email.strip().lower()
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User(email=email)
                db.session.add(user)
            user.role = role
            user.set_password(password)

        db.session.commit()
        print("Admin and viewer users are ready.")

    return app