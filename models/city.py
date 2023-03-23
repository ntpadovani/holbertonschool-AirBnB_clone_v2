#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel #Norman thingys, City inherits from BaseModel 
from models.base_model import Base # Norman thingys, and Base (respect the order)
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities' # Norman thingys, Add or replace in the class City
    name = Column(String(128), nullable=False) # Norman thingys, represents a column containing a string (128 characters), can’t be null
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False) # Norman thingys, represents a column containing a string (60 characters), can't be null, is a foreign key 
    #places = relationship("Place", backref='cities',
    #                     cascade="all, delete, delete-orphan")