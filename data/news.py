import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.SMALLINT,
                           primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)

    news = orm.relation("News", back_populates='category')


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    category_id = sqlalchemy.Column(sqlalchemy.SMALLINT,
                                     sqlalchemy.ForeignKey("category.id"))
    title = sqlalchemy.Column(sqlalchemy.String,
                              nullable=True)
    content = sqlalchemy.Column(sqlalchemy.TEXT,
                                nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean,
                                   default=False)
    is_published = sqlalchemy.Column(sqlalchemy.Boolean,
                                     default=True)

    user = orm.relation('Users', back_populates='news')
    comments = orm.relation('Comments', back_populates='news')
    category = orm.relation("Category", back_populates='news')

    def __repr__(self):
        return f"***\n<class={__class__.__name__}>\n" \
               f"id={self.id}\ttitle={self.title}\tcontent={self.content}\tuser_id={self.user_id} " \
               f"created_date={self.created_date}\tis_private={self.is_private}\tis_published={self.is_published} " \
               f"user={self.user}\tcomments={self.comments}\tcategories={self.categories} " \
               f"\n***"
