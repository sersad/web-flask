from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    is_published = BooleanField("Опубликовать?")
    category = SelectField("Категория новости", coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить')
