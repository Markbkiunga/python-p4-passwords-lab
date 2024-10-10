#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User


class ClearSession(Resource):

    def delete(self):

        session["page_views"] = None
        session["user_id"] = None

        return {}, 204


class Signup(Resource):

    def post(self):
        json = request.get_json()
        user = User(username=json["username"])
        user.password_hash = json["password"]
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


class CheckSession(Resource):
    pass

    def get(self):
        if session["user_id"] and session["username"]:
            user_id = session["user_id"]
            user = User.query.filter_by(id=user_id).first()
            print(user)
            return make_response(user.to_dict(), 200)
        else:
            return make_response({}, 204)


class Login(Resource):
    pass

    def post(self):
        json = request.get_json()
        user = User.query.filter_by(username=json["username"]).first()
        if user and user.password_hash == json["password"]:
            session["user_id"] = user.id
            session["username"] = user.username
            response = user.to_dict()
            return make_response(response, 200)
        else:
            response = {"message": "Invalid username or password"}
            return make_response(response, 404)


class Logout(Resource):
    pass

    def delete(self):
        if session["user_id"] and session["username"]:
            session.clear()
            return make_response({}, 204)
        else:
            return make_response({}, 204)


api.add_resource(ClearSession, "/clear", endpoint="clear")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
