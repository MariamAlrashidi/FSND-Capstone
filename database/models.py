import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import datetime
import json


database_filename = os.environ.get("DATABASE", "database.db")
project_dir = os.path.dirname(os.path.abspath(__file__))


#database_path = os.environ['DATABASE_URL']

database_name = "casting_agency"
database_path = "postgres://postgres:1234567890@{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
  #  db.drop_all()
    db.create_all()

#Table Show
class Show(db.Model):
    __tablename__ = 'show'
    actor_id = db.Column(db.Integer(), db.ForeignKey(
        'actor.id'), primary_key=True, nullable=True)
    movie_id = db.Column(db.Integer(), db.ForeignKey(
        'movie.id'), primary_key=True, nullable=True)

    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def format(self):
        return {"actor_id": self.actor_id, "movie_id": self.movie_id}

    def get_show(self):
        return {
            "actor_id": self.actor_id,
            "movie_id": self.movie_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())

#Table Actor

class Actor(db.Model):
    __tablename__ = "actor"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String(80), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {"id": self.id, "name": self.name, "age": self.age}

    def get_actor(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


#Table Mivie
class Movie(db.Model):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)

    def __init__(self, title, release_date=None):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }

    def get_movie(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


