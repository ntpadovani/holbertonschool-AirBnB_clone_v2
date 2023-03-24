#!/usr/bin/python3
""" State Module for HBNB project """
from os import environ
from models.base_model import BaseModel, Base #Norman thingy, State inherits from BaseModel and Base
from models.city import City 
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.engine.file_storage import FileStorage

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states' # Norman thingy, represents the table name, states
    name = Column(String(128), nullable=False) # Norman thingy, represents a column containing a string (128 characters), can't be null

    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='states', #Norman thingy, must represent a relationship with the class City
                              cascade='all, delete') # Norman thingy, If the State object is deleted, all linked City objects must be automatically deleted
    else:
        @property #Norman thingy, comments would be too long so will not go into details but here is the getter method
        def cities(self):
            """ getter method for reviews when place_id == Place.id"""
            from models import storage
            cities_list = []
            
            for city in storage.all(City):
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list