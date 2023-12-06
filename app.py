from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import os
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from resources.users import configure_users_routes
from resources.roles import configure_roles_routes
from resources.contact import configure_contact_routes
from resources.auth import configure_auth

app = Flask(__name__)
app.secret_key = "your_secret_key"
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://aussie-tea-user:aussie123@aussie-tea.xcz2kza.mongodb.net/form?retryWrites=true&w=majority"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MongoDB Collections
users_collection = mongo.db.users
roles_collection = mongo.db.roles
contact_collection = mongo.db.contact

configure_auth(app, users_collection)

# Configure routes
configure_users_routes(app, users_collection, bcrypt)
configure_roles_routes(app, roles_collection)
configure_contact_routes(app, contact_collection)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
