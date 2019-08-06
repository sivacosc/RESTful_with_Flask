from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores


def create_app(name):
    named_app = Flask(name)
    from db import db
    db.init_app(named_app)
    named_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    named_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    named_app.secret_key = 'siva'
    with named_app.app_context():
        db.create_all()
    api = Api(named_app)

    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(Items, '/items')
    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(Stores, '/stores')
    api.add_resource(UserRegister, '/register')
    return named_app
# @app.before_first_request
# def create_tables():
#     db.create_all()


if __name__ == "__main__":
    app = create_app(__name__)
    jwt = JWT(app, authenticate, identity)
    app.run(port=5000, debug=True)
