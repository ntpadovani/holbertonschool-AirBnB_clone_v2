#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime



Base = declarative_base() # Norman thingy


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True) # Norman thingy, represents a column containing a unique string (60 characters), can’t be null, primary key
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False) # Norman thingy, represents a column containing a datetime, can't be null, default value is the current datetime
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False) # Norman thingy, represents a column containing a datetime, can't be null, default value is the current datetime

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            for key, value in kwargs.items(): #Norman thingy, create instance attribute from this dictionary
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f") 
                    setattr(self, key, value) 
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self) #norman thingy
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        if ('_sa_instance_state' in dictionary):
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """ Deletes instance from storage """
        models.storage.delete(self) # Norman thingy, to delete the current instance from the storage