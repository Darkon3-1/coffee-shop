import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    print('adding drinks')
    add_records()

'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''
class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    recipe =  Column(String(180), nullable=False)

    '''
    short()
        short form representation of the Drink model
    '''
    def short(self):
        print('getting stuff')
        print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    '''
    long()
        long form representation of the Drink model
    '''
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())

def add_records():
    print('creating some yummy drinks')
    vanilla_latte_recipe = [
                { "name":"Milk","color":"blue","parts":2 },
                { "name":"Vanilla","color":"green","parts":0.5 },
                { "name":"Coffee","color":"brown","parts":3 } ]

    iced_lemonade_recipe = [ { "name":"Lemon juice","color":"yellow", "parts":0.5 },
            { "name":"water","color":"pink", "parts":5 },
            { "name":"Sugar","color":"red", "parts":1 },
            { "name":"Ice","color":"black", "parts":2 } ]

    hot_chocolate_recipe = [ { "name":"Milk","color":"pink", "parts":3 },
                { "name":"Chocolate powder","color":"brown", "parts":1.5 },
                { "name":"Cream","color":"purple", "parts":1 } ]

    coffee_recipe = [ { "name":"Coffee","color":"brown", "parts":3 },
                { "name":"Milk","color":"blue", "parts":1.5 },
                { "name":"Cream","color":"yellow", "parts":1 } ]
    matcha_shake_recipe = [{"name": "milk","color": "grey","parts": 1},
                {"name": "matcha","color": "green","parts": 3}]


    vanilla_latte = (Drink(
            id = 1,
            title = 'Vanilla Latte',
            recipe = json.dumps(vanilla_latte_recipe)
            ))

    iced_lemonade = (Drink(
            id = 2,
            title = 'Iced Lemonade',
            recipe = json.dumps(iced_lemonade_recipe)
            ))

    hot_chocolate = (Drink(
            id = 3,
            title = 'Hot Chocolate',
            recipe = json.dumps(hot_chocolate_recipe)
            ))

    coffee = (Drink(
            id = 4,
            title = 'coffee',
            recipe = json.dumps(coffee_recipe)
            ))
    macha_shake = (Drink(
            id = 5,
            title = 'matcha shake',
            recipe = json.dumps(matcha_shake_recipe)
            ))

    vanilla_latte.insert()
    iced_lemonade.insert()
    hot_chocolate.insert()
    coffee.insert()
    macha_shake.insert()