# init_app.py
from flask_pymongo import PyMongo, GridFS
from flask_jwt_extended import JWTManager

jwt = JWTManager()
mongo = PyMongo()

def init_app(app):
    mongo.init_app(app)
    jwt.init_app(app)

def get_collection(collection_name):
    return mongo.db[collection_name]

def get_gridfs():
    def gridfs_factory():
        return GridFS(mongo.db)
    return gridfs_factory