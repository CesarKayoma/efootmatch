from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Player, Team


class PlayerForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(max=100)])
    team_id = RadioField("Time", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Salvar")

    def __init__(self, *args, player=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._player = player

        teams = Team.query.order_by(Team.name).all()
        self.team_id.choices = [(team.id, team.name) for team in teams]

    def validate_name(self, field):
        if not field.data or not self.team_id.data:
            return

        query = Player.query.filter_by(name=field.data, team_id=self.team_id.data)

        if self._player:
            query = query.filter(Player.id != self._player.id)

        if query.first():
            raise ValidationError("Esse jogador já existe nesse time.")