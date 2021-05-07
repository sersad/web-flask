from flask import jsonify
from flask_restful import reqparse, abort,  Resource

from . import db_session
from .users import Users

parser = reqparse.RequestParser()
parser.add_argument('id', required=False, type=int)
parser.add_argument('name', required=True)
parser.add_argument('login', required=True)
parser.add_argument('email', required=True)
parser.add_argument('user_type_id', required=True, type=int)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(Users).get(user_id)
        return jsonify(
            {'users': users.to_dict(rules=('-news',
                                         '-users_type',
                                         '-comments',
                                         ))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(Users).get(user_id)
        db_sess.delete(users)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(Users).all()
        return jsonify({'users': [item.to_dict(
            rules=('-news',
                   '-users_type',
                   '-comments',
                   )) for item in users]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = Users(
            name=args['name'],
            login=args['login'],
            email=args['email'],
            user_type_id=args['user_type_id'],
            )
        if args['id'] and not db_sess.query(Users).get(args['id']):
            user.id = args['id']

        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def abort_if_users_not_found(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Users).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")

