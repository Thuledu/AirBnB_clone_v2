#!/usr/bin/python3
"""This module defines a class to manage the database storage for the hbnb clone"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place, place_amenity
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db), pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        session = self.__session()
        objects = {}
        if cls:
            query_result = session.query(cls).all()
            for obj in query_result:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for model in [State, City, Place, User, Amenity, Review]:
                query_result = session.query(model).all()
                for obj in query_result:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        session.close()
        return objects

    def new(self, obj):
        session = self.__session()
        session.add(obj)
        session.commit()
        session.close()

    def save(self):
        session = self.__session()
        session.commit()
        session.close()

    def delete(self, obj=None):
        if obj:
            session = self.__session()
            session.delete(obj)
            session.commit()
            session.close()

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        self.__session.remove()
