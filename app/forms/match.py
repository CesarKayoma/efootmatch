from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired


class MatchForm(FlaskForm):
    # Preenchido via JS pelo combobox de busca de MOTM
    motm_player_id = HiddenField(
        "MOTM",
        validators=[DataRequired(message="Selecione o MOTM da partida.")]
    )

    # Preenchido via JS com um JSON.stringify() da lista de gols
    # montada em memória no navegador (ex: '[{"team_id": 1, "scorer_id": 4, ...}]')
    goals_json = HiddenField("Goals", default="[]")

    submit = SubmitField("Save Match!")