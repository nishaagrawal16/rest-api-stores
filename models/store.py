from db import db

class StoreModel(db.Model):
  __tablename__ = 'stores'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))

  # One to Many relationship means one store can many items
  items = db.relationship('ItemModel', lazy='dynamic')
  # When we create the StoreModel, we are going to create an object for each
  # item in the database that matches that store id. If we have few items then
  # it's ok. But if we have many items then it is very expensive operation.
  # for not creating the item obejct we use the lazy dynamic. So whenever we
  # use the json method we will get the error. So we need to use the .all()
  # because self.items no longer is a list of items. Now it is a query builder
  # that has the ability to look into the database but it is slower because
  # whenever we need to call the json() method, we need to look into the
  # database table.
  
  def __init__(self, name):
    self.name = name

  def json(self):
    return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

  @classmethod
  def find_by_name(cls, name):
    # It is equvalent to: SELECT * FROM items where name=name LIMIT 1
    return cls.query.filter_by(name=name).first() 

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()