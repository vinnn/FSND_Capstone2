#########################################################
# IMPORTS
#########################################################
import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json


#########################################################
# DATABASE CONFIGURATION
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
# database_name = "db_capstone2"
# IF LOCAL - path:
# database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
# IF DEPLOYMENT (TO HEROKU) - path:
# database_path = "postgres://dipxbxzeizwkwk:7c8373d60894aaaebb1e10380148f2b1dc1d2f9bafb3a62468b9effb1c7453e7@ec2-52-205-45-219.compute-1.amazonaws.com:5432/devh56majc5epu"
# database_path = "postgres://nfkphcncctfhsr:28a0b6b1e059768d27a4f75e8034b9d8dfa36395ca7011c1614f28503974b6ac@ec2-54-195-246-55.eu-west-1.compute.amazonaws.com:5432/d69ah6men0oka"


database_path = os.environ.get('DATABASE_URL')

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
# Association Table
#########################################################
movie_actors = db.Table(
    'movie_actors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
    )


#########################################################
# Actors
#########################################################
'''
Actor
an actor entity, extends the base SQLAlchemy Model
'''


class Actor(db.Model):
    __tablename__ = 'actors'  # table name to be plural, non-capitalized
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # String Name
    name = db.Column(db.String(80), unique=True, nullable=False)
    # String Age
    age = db.Column(db.Integer, unique=False, nullable=False)
    # String Gender
    gender = db.Column(db.String(80), unique=False, nullable=False)
    # Many-to-many relationship
    movie = db.relationship('Movie', secondary=movie_actors, backref=db.backref('actors', lazy=True))

    '''
    todictionary()
        dictionary representation of the model
    '''
    def todictionary(self):
        return {
            'id': self.id,
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
# method to give a readable string representation (for debugging and testing)
#########################################################
    def __repr__(self):
        return '<name %r>' % self.name


#########################################################
# Movies
#########################################################
'''
Movie
a movie entity, extends the base SQLAlchemy Model
'''


class Movie(db.Model):
    __tablename__ = 'movies'  # table name to be plural, non-capitalized
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # String Title
    title = db.Column(db.String(80), unique=True)
    # String Release_date
    release_date = db.Column(db.DateTime)
    # Many-to-many relationship
    actor = db.relationship('Actor', secondary=movie_actors, backref=db.backref('movies', lazy=True))

    '''
    todictionary()
        dictionary representation of the model
    '''
    def todictionary(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Jurassic Park'
            movie.update()
    '''
    def update(self):
        db.session.commit()

#########################################################
# method to give a readable string representation (for debugging and testing)
#########################################################
    def __repr__(self):
        return '<name %r>' % self.name
