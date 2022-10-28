import os
import json
from sqlalchemy import Column, Integer, String, create_engine, Date
from flask_sqlalchemy import SQLAlchemy



#DATABASE_PATH = os.environ['DATABASE_URL']
#DATABASE_PATH = 'postgresql://ulxxdhwkddjwqy:85e70942145391f2ffdb063db6bcc4e425659cdef7682654893e88d2a2c945c2@ec2-18-209-78-11.compute-1.amazonaws.com:5432/d3u8jvplibk40e'

DATABASE_PATH = os.getenv("DATABASE_URL")
if DATABASE_PATH.startswith("postgres://"):
    DATABASE_PATH = DATABASE_PATH.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


'''
setup_db(app) binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    app.context()


'''
Actors Table & Model
'''

#Renter
class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name' : self.name,
            'gender': self.gender,
            'age': self.age
            }


'''
Movies Table & Model
'''

#Rental
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title' : self.title,
            'release_date': self.release_date
            }