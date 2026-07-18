from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Team

class TeamForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Save")

    def __init__(self, *args, team=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._team = team
    
    def validate_name(self, field):
        if not field.data:
            return
        query = Team.query.filter_by(name=field.data)
        if self._team:
            query = query.filter(Team.id != self._team.id)

        team = query.first()

        if team:
            raise ValidationError("Team already exists.")