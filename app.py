# Lint as: python3
"""
APP for using the SQLite3 as database and save the users information into database.
"""
from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# This is basically removed the flask sqlalchemy track modification.
# As SQLALCHEMY also has a seperate track modicfication which keep
# the track of all the changes done in the object.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

# This is basically called first before any other call.
# Means after this call app.config will call
@app.before_first_request
def create_tables():
  db.create_all() # This will create all the models which are imported like Item.

jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
  db.init_app(app)
  app.run(port=5000, debug=True)
