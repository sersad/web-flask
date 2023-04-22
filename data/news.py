import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    news = orm.relationship("News", cascade="all, delete")


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    category_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("category.id"))
    title = sqlalchemy.Column(sqlalchemy.String,
                              nullable=True)
    content = sqlalchemy.Column(sqlalchemy.TEXT,
                                nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_published = sqlalchemy.Column(sqlalchemy.Boolean,
                                     default=True)

    user = orm.relationship('Users', back_populates='news')
    # если новость удалили то и каскадом комментарии
    comments = orm.relationship('Comments', cascade="all, delete")
    category = orm.relationship("Category", back_populates='news')

    def __repr__(self):
        return f"***\n<class={__class__.__name__}>\n" \
               f"id={self.id}\ttitle={self.title}\tcontent={self.content}\tuser_id={self.user_id} " \
               f"created_date={self.created_date}\tis_published={self.is_published} " \
               f"user={self.user}\tcomments={self.comments}\tcategories={self.category} " \
               f"\n***"


