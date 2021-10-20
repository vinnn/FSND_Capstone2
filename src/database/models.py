#########################################################
#I# IMPORTS 
#########################################################
import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json


#########################################################
#I# DATABASE CONFIGURATION
#########################################################
'''
use db = SQLAlchemy() + db.init_app(app), instead of db = SQLAlchemy(app)
https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/factories-extensions
'''

#  SQLITE SETUP  ###################################
# database_filename = "database11.db"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
#
# db = SQLAlchemy()        
# '''
# setup_db(app)
#     binds a flask application and a SQLAlchemy service
# '''
# def setup_db(app):
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)


#  POSTGRES SETUP  ###################################
database_name = "db_capstone2"
# IF LOCAL - path:
database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
# IF DEPLOYMENT (TO HEROKU) - path:
# database_path = "postgres://nfkphcncctfhsr:28a0b6b1e059768d27a4f75e8034b9d8dfa36395ca7011c1614f28503974b6ac@ec2-54-195-246-55.eu-west-1.compute.amazonaws.com:5432/d69ah6men0oka"

db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


#########################################################

#########################################################
'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


#########################################################

#########################################################
'''
Actor
an actor entity, extends the base SQLAlchemy Model
'''
class Actor(db.Model):
    __tablename__ = 'actors'  # table name to be plural, non-capitalized
    # Autoincrementing, unique primary key
############################################################
############################################################  TO RECTIFY
############################################################
############################################################
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
############################################################
############################################################
############################################################
############################################################   
    # String Name
    name = Column(String(80), unique=True, nullable=False)
    # String Age
    age = Column(Integer, unique=False, nullable=False)
    # String Gender
    gender = Column(String(80), unique=False, nullable=False)

    '''
    todictionary()
        dictionary representation of the model
    '''    
    def todictionary(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            actor = Actor(name=req_name, age=req_age, gender=req_gender)
            actor.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor(name=req_name, age=req_age)
            actor.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'James'
            actor.update()
    '''
    def update(self):
        db.session.commit()


#########################################################
#I# method to give a readable string representation (for debugging and testing)
#########################################################
    def __repr__(self):
        return '<name %r>' % self.name


