from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.news import Category


class NewsForm(FlaskForm):
    db_session.global_init("db/base.db")
    db_sess = db_session.create_session()
    category = [(i.id, i.name) for i in db_sess.query(Category).all()]

    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    is_published = BooleanField("Опубликованное")
    # category = SelectField("Категория", choices=category, validators=[DataRequired()])
    category = SelectField("Категория", coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить')
