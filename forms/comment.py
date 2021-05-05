from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, length


class CommentForm(FlaskForm):
    content = TextAreaField("Комментарий", validators=[DataRequired(), length(max=500)])
    submit = SubmitField("Добавить")
