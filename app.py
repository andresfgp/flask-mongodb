from flask import Flask
from flask_pymongo import PyMongo
import os
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from resources.users import configure_users_routes
from resources.roles import configure_roles_routes
from resources.contact import configure_contact_routes
from resources.auth import configure_auth
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) 
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://aussie-tea-user:GNoKDXUv3swk4ydK@aussie-tea.xcz2kza.mongodb.net/form?retryWrites=true&w=majority"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

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
