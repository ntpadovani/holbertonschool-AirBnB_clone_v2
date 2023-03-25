#!/usr/bin/python3
""" State Module for HBNB project """
from os import environ
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='states',
                              cascade='all, delete')
    else:
        @property
        def cities(self):
            """ getter method for reviews when place_id == Place.id"""
            from models import storage
            cities_list = []

            for city in storage.all(City):
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
