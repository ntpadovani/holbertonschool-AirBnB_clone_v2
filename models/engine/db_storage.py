#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm.exc import NoResultFound
import os


class DBStorage:
    """This class manages storage of hbnb models in JSON format"""
    __engine = None 
    __session = None

    __classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                }

    def __init__(self):
        """ Initializes the database """
        user = os.getenv('HBNB_MYSQL_USER') # Norman thingy, this is self explainatory 
        password = os.getenv('HBNB_MYSQL_PWD') # Norman thingy, this is self explainatory
        host = os.getenv('HBNB_MYSQL_HOST') # Norman thingy, this is self explainatory
        database = os.getenv('HBNB_MYSQL_DB') # Norman thingy, this is self explainatory

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'. #Norman thingy, create the engine, the engine must be linked to the MySQL database
                                      format(user, password, host, database),
                                      pool_pre_ping=True) #Norman thingy, feature that tests connections for liveness upon each checkout.
        if (os.getenv('HBNB_ENV') == 'test'): # drop all tables if the environment variable HBNB_ENV is equal to test
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None): #Norman thingy
        """Returns all objects based on class provided"""
        obj_dict = {}
        if cls is None:
            for key, value in self.__classes.items():
                try:
                    result = self.__session.query(value).all() # if cls=None, query all types of objects
                except:
                    pass
                for obj in result:
                    new_key = key + "." + obj.id
                    obj_dict[new_key] = obj
        else:
            result = self.__session.query(self.__classes[cls]).all() # query on the current database session (self.__session) all objects depending of the class name (argument cls)
            for obj in result: #  method must return a dictionary
                new_key = str(cls) + "." + obj.id
                obj_dict[new_key] = obj

        return obj_dict

    def new(self, obj):
        self.__session.add(obj) # add the object to the current database session (self.__session)
        pass

    def save(self):
        """commits the changes to the database"""
        self.__session.commit() # commit all changes of the current database session (self.__session)

    def reload(self):
        ''' Creates all the tables in the current Database '''
        Base.metadata.create_all(self.__engine) # self explainatory

        # Creates session factory - creates session object with given rules
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False) # using a sessionmaker - the option expire_on_commit must be set to False
        # Session will call upon the same registry of sessions created
        # This allows us to get back the same session everytime
        Session = scoped_session(session_factory) # and scoped_session - to make sure your Session is thread-safe

        # Now we have a "global" session that our app can use collectively
        self.__session = Session()

    def delete(self, obj=None):
        if obj is not None: #  delete from the current database session obj if not None
            self.__session.delete(obj)
        pass