from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
  # This is only for parse the request payload from the frontend
  # and skip other not useful data.
  parser = reqparse.RequestParser()
  parser.add_argument('price',
    type=float,
    required=True,
    help="This filed can not be left blank!"      
  )
  parser.add_argument('store_id',
    type=int,
    required=True,
    help="Every Item needs a Store Id."      
  )
  @jwt_required()
  def get(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      return item.json()
    return {'message': 'Item not found'}, 404

  def post(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      return {'message': "An item with name '{}' is already exists.".format(name)}, 400
    data = Item.parser.parse_args()
    # data['price'], data['store_id']
    item = ItemModel(name, **data)
    try:
      item.save_to_db()
    except:
      return {'message': 'An error occured inserting the item'}, 500 # Internal server error
    return item.json(), 201

  def put(self, name):
    data = Item.parser.parse_args()

    item = ItemModel.find_by_name(name)
    if item:
      item.price = data['price']
    else:
      item = ItemModel(name, **data)
    item.save_to_db()

    return item.json()

  def delete(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      item.delete_from_db()
      return {'message': 'Item deleted'}
    return {'message': 'Item not found'}

class ItemList(Resource):
  def get(self):
    return {'items': [item.json() for item in ItemModel.query.all()]}