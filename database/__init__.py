from pymongo import MongoClient
from .db import Database
import app_config as config

database = Database(connectrion_string = config.CONST_MONGO_URL, database_name = config.CONST_DATABASE)
database.connect()

"""
Ce fichier initialise la connexion à MongoDB en utilisant la classe Database définie dans db.py.
Il utilise la chaîne de connexion et le nom de la base de données définis dans app_config.py.
"""