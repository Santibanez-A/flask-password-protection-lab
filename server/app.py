#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema



#login session capture passing resource
class Login(Resource):

    def post(self):
        data = request.get_json()

        user = User.query.filter_by(
            username=data.get('username')
        ).first()

        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id

            user_json = UserSchema().dump(user)

            return user_json, 200

        return {}, 401

#sign up session passing resource
class Signup(Resource):

    def post(self):
        data = request.get_json()

        user = User(
            username=data.get('username')
        )

        user.password_hash = data.get('password')

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        user_json = UserSchema().dump(user)

        return user_json, 201
#authenticates session
class CheckSession(Resource):

    def get(self):
        user_id = session.get('user_id')

        if user_id:
            user = User.query.filter_by(id=user_id).first()

            user_json = UserSchema().dump(user)

            return user_json, 200

        return {}, 204
#logout from session
class Logout(Resource):

    def delete(self):
        session.pop('user_id', None)

        return {}, 204

#clear the info once gone
class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204


#linking all together
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(ClearSession, '/clear', endpoint='clear')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
