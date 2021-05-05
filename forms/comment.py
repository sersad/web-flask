from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, length


class CommentForm(FlaskForm):
    content = TextAreaField("Комментарий", validators=[DataRequired(), length(max=500)])
    news_id = StringField("", validators=[DataRequired()])
    submit = SubmitField("Добавить")
