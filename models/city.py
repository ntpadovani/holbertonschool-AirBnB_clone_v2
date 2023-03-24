#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base #Norman thingys, City inherits from BaseModel 
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities' # Norman thingys, Add or replace in the class City
    name = Column(String(128), nullable=False) # Norman thingys, represents a column containing a string (128 characters), can’t be null
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False) # Norman thingys, represents a column containing a string (60 characters), can't be null, is a foreign key 

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        places = relationship('Place', backref='cities', cascade='delete')
