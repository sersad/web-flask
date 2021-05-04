import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Comments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    users_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    news_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("news.id"))

    content = sqlalchemy.Column(sqlalchemy.TEXT,
                                nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    users = orm.relation('Users',
                        back_populates='comments')
    news = orm.relation('News',
                        back_populates='comments')

    def __repr__(self):
        return f"***\n<class={__class__.__name__}>\n" \
               f"id={self.id}\tuser_id={self.user_id}\tnews_id={self.news_id}" \
               f"content={self.content}\tcreated_date={self.created_date}" \
               f"\n***"
