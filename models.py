import os
import json
from sqlalchemy import Column, Integer, String, create_engine, Date
from flask_sqlalchemy import SQLAlchemy



#DATABASE_PATH = os.environ['DATABASE_URL']
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
    app.app_context()
    #db.create_all()
    


'''
Renters Table & Model
'''
class Renters(db.Model):
    __tablename__ = 'Renters'

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
Rentals Table & Model
'''
class Rentals(db.Model):
    __tablename__ = 'Rentals'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, address, rent):
        self.title = address
        self.release_date = rent

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
            'address' : self.address,
            'rent': self.rent
            }