from data import db_session
from data.news import News, Category
from data.users import Users, UsersTypes


def add_users_types(db_sess):
    """
    Создаем типы пользователей
    :param db_sess:
    :return:
    """
    types1 = UsersTypes(id=1,
                        users_type="Администраторы")
    types2 = UsersTypes(id=2,
                        users_type="Обычные пользователи")
    types3 = UsersTypes(id=3,
                        users_type="Пользователи только для чтения")
    db_sess.add(types1)
    db_sess.add(types2)
    db_sess.add(types3)
    db_sess.commit()


def add_user(db_sess):
    """
    для теста создаем юзеров
    :param db_sess:
    :return:
    """
    user1 = Users(name="Администратор",
                  login="admin",
                  email="email@email.ru",
                  user_type_id=1,
                  hashed_password='12345'
                  )
    user2 = Users(name="Пользователь",
                  login="user",
                  email="email1@email.ru",
                  user_type_id=2,
                  hashed_password='123'
                  )
    user1.set_password(user1.hashed_password)
    user2.set_password(user2.hashed_password)
    db_sess.add(user1)
    db_sess.add(user2)
    db_sess.commit()


def add_category(db_sess):
    """
    для теста создаем юзеров
    :param db_sess:
    :return:
    """
    category1 = Category(id=1,
                         name="Regular")
    category2 = Category(id=2,
                         name="Sport")
    category3 = Category(id=3,
                         name="IT")
    db_sess.add(category1)
    db_sess.add(category2)
    db_sess.add(category3)
    db_sess.commit()


def add_news(db_sess):
    """
    для теста создаем юзеров
    :param db_sess:
    :return:
    """
    news1 = News(title="Первая новость",
                 content="Текст первой новости",
                 user_id=1,
                 )
    news2 = News(title="Вторая новость",
                 content="Текст второй новости",
                 user_id=1,
                 )
    news3 = News(title="Третья новость",
                 content="Текст 3 новости",
                 user_id=1,
                 )

    db_sess.add(news1)
    db_sess.add(news2)
    db_sess.add(news3)
    db_sess.commit()


def main():
    db_session.global_init("db/base.db")
    db_sess = db_session.create_session()
    add_users_types(db_sess)
    add_user(db_sess)
    add_category(db_sess)
    add_news(db_sess)


if __name__ == '__main__':
    main()
