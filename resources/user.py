import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('username',
    type=str,
    required=True,
    help="This filed can not be blank!"
  )
  parser.add_argument('password',
    type=str,
    required=True,
    help="This filed can not be blank!"
  )

  def post(self):
    data = UserRegister.parser.parse_args()
    if UserModel.find_by_username(data['username']):
      return {"message": "A user with that name already exists"}, 400
    # data['username'], data['password'] => **data (unpack)
    user = UserModel(**data)
    user.save_to_db()

    return {"message": "User registered Successfully"}, 201
