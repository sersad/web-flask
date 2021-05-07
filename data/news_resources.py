from flask import jsonify
from flask_restful import reqparse, abort,  Resource

from . import db_session
from .news import News

parser = reqparse.RequestParser()
parser.add_argument('id', required=False, type=int)
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('category_id', required=True, type=int)


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        db_sess = db_session.create_session()
        news = db_sess.query(News).get(news_id)
        return jsonify(
            {'news': news.to_dict(rules=('-user',
                                         '-comments',
                                         '-category',
                                         ))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        db_sess = db_session.create_session()
        news = db_sess.query(News).get(news_id)
        db_sess.delete(news)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        news = db_sess.query(News).all()
        return jsonify({'news': [item.to_dict(
            rules=('-user',
                   '-comments',
                   '-category',
                   )) for item in news]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            category_id=args['category_id'],
            is_published=args['is_published'],
            )
        if args['id'] and not db_sess.query(News).get(args['id']):
            news.id = args['id']

        db_sess.add(news)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")

