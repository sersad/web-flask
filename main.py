import logging
import os
from datetime import datetime

from flask import Flask, render_template, redirect, make_response, request, session, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFError, CSRFProtect

from data import db_session
from data.comments import Comments
from data.news import News, Category
from data.users import Users
from forms.comment import CommentForm
from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm

from flask_restful import reqparse, abort, Api, Resource

from waitress import serve

app = Flask(__name__)
csrf = CSRFProtect(app)
api = Api(app)

SECRET_KEY = os.urandom(32)

app.config.update(
    SECRET_KEY=SECRET_KEY,
    DEBUG=True,
    WTF_CSRF_ENABLED=True)



# Затем сразу после создания приложения flask инициализируем LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Чтобы продлить жизнь сессии
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

logging.basicConfig(level=logging.WARNING)

@login_manager.user_loader
def load_user(user_id):
    """
    функция для получения пользователя, украшенная декоратором login_manager.user_loader
    """
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = CommentForm()
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    if form.validate_on_submit():
        comment = Comments(content=form.content.data,
                           users_id=current_user.id,
                           news_id=int(form.news_id.data))
        logging.warning(f"{current_user.id}")
        db_sess.add(comment)
        db_sess.commit()
        return redirect('/')
    return render_template("index.html", news=news, form=form)



@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с такой почтой уже есть")

        if db_sess.query(Users).filter(Users.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким логином уже есть")
        user = Users(
            name=form.name.data,
            login=form.login.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Если форма логина прошла валидацию, мы находим пользователя,
    проверяем, введен ли для него правильный пароль, если да,
    вызываем функцию login_user модуля flask-login и передаем туда объект
    нашего пользователя, а также значение галочки «Запомнить меня».
    После чего перенаправляем пользователя на главную страницу нашего приложения."""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    db_sess = db_session.create_session()
    category = db_sess.query(Category).all()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        news.is_published = form.is_published.data
        print(form.category.data)
        news.category_id = form.category.data
        current_user.news.append(news)
        # мы изменили текущего пользователя с помощью метода merge
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html',
                           title='Добавление новости',
                           form=form,
                           category=category)


@app.route('/news/<id_>', methods=['GET', 'POST'])
@login_required
def edit_news(id_):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id_,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id_,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return render_template('error.html', reason=reason)


def main():
    db_session.global_init("db/base.db")
    db_sess = db_session.create_session()

    # # user = db_sess.query(Users).first()
    # # print(user.news)
    # news = db_sess.query(News).all()
    # for item in news:
    #     print(item.user)

    # db_sess = db_session.create_session()
    # category = [(i.id, i.name) for i in db_sess.query(Category).all()]
    # print(category)

    port = int(os.environ.get('PORT', 5000))
    # с дефаултными значениями будет не более 4 потоков
    app.run()
    # serve(app, port=port, host="0.0.0.0")


if __name__ == '__main__':
    main()
