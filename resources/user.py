import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "User with the username " + data['username'] + " already exists!"}, 409
        try:
            user = UserModel(**data)
            user.save_to_db()
        except Exception as e:
            return {"message": "{}".format(e)}, 500
        return {"message": "User created successfully"}, 201
