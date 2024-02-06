# app.py
from flask import Flask
import os
from flask_cors import CORS
from datetime import timedelta
from flask_smorest import Api
from init_app import init_app
from blueprints import register_blueprints
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config["MONGO_URI"] = "mongodb+srv://aussie-tea-user:GNoKDXUv3swk4ydK@aussie-tea.xcz2kza.mongodb.net/form?retryWrites=true&w=majority"
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECK'] = 'refresh'

    JWTManager(app)  # Initialize JWTManager and associate it with the app

    init_app(app)  # Initialize the mongo object with the app

    api = Api(app)
    register_blueprints(api)

    return app

if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
