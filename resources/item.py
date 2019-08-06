from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every Item needs a store_id!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404

    def post(self, name):
        try:
            if ItemModel.find_by_name(name):
                return {'message': "An item with name '{}' already exists.".format(name)}, 409
            try:
                data = Item.parser.parse_args()
            except Exception as e:
                return {'message': 'invalid format', 'error': '{}'.format(e)}, 400
        except Exception as err:
            return {'message': 'Error occured while looking up item {}'.format(name), 'error': '{}'.format(err)}, 500
        item = ItemModel(name, data['price'], data['store_id'])
        item.save_to_db()
        return item.json(), 201

    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
