# blueprints.py
from flask_smorest import Api
from resources.users import blp as UsersBlueprint
from resources.contact import blp as ContactBlueprint
from resources.roles import blp as RolesBlueprint
from resources.auth import blp as AuthBlueprint

def register_blueprints(api):
    api.register_blueprint(UsersBlueprint, url_prefix='/api/users')
    api.register_blueprint(ContactBlueprint, url_prefix='/api/contact')
    api.register_blueprint(RolesBlueprint, url_prefix='/api/roles')
    api.register_blueprint(AuthBlueprint, url_prefix='/api/auth')
