#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os
from models.engine.db_storage import DBStorage # Import DBStorage class in this file
from models.engine.file_storage import FileStorage # Import FileStorage class in this file

if os.getenv('HBNB_TYPE_STORAGE') == "db":
    storage = DBStorage() # Create an instance of DBStorage and store it in the variable storage (the line storage.reload() should be executed after this instantiation)
    storage.reload()

else:
    storage = FileStorage() # Create an instance of FileStorage and store it in the variable storage (the line storage.reload() should be executed after this instantiation)
    storage.reload()