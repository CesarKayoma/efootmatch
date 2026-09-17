from urllib.parse import urljoin, urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

from app.models import User

bp = Blueprint("auth", __name__)


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


def _is_safe_redirect_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash("E-mail ou senha inválidos.", "error")
            return render_template("auth/login.html", form=form), 401

        login_user(user)
        next_url = request.args.get("next")
        if next_url and _is_safe_redirect_url(next_url):
            return redirect(next_url)
        return redirect(url_for("home.home"))

    return render_template("auth/login.html", form=form)


@bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
