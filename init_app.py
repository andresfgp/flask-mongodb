# init_app.py
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

jwt = JWTManager()
mongo = PyMongo()

def init_app(app):
    mongo.init_app(app)
    jwt.init_app(app)

def get_collection(collection_name):
    return mongo.db[collection_name]