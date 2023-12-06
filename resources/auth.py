from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import jsonify, request, flash
from bson import ObjectId
import jwt
from datetime import datetime, timedelta

from crud_operations import document_exists

bcrypt = Bcrypt()

class User(UserMixin):
    pass

def configure_auth(app, users_collection):
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            user = User()
            user.id = str(user_data['_id'])
            return user
        return None

    def generate_jwt_token(user):
        expiration_time = datetime.utcnow() + timedelta(days=1)
        token_payload = {
            'user_id': str(user['_id']),
            'exp': expiration_time,
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
        return token

    @app.route('/login', methods=['POST'])
    def login():
        if request.method == 'POST':
            email = request.get_json()['email']
            password = request.get_json()['password']
            user = users_collection.find_one({'email': email})
            if user and bcrypt.check_password_hash(user['password'], password):
                user_obj = User()
                user_obj.id = str(user['_id'])
                login_user(user_obj)
                flash('Login successful', 'success')

                # Additional data to include in the response
                additional_data = {
                    'user_id': str(user['_id']),
                    'email': user['email'],
                    'full_name': user.get('full_name', ''),
                    # Assuming full_name is a field in your user document
                    # Add any other relevant user data here
                }

                # Generate JWT token
                token = generate_jwt_token(user)

                return jsonify({'message': 'Login successful', 'data': additional_data, 'token': token}), 200
            else:
                return jsonify({'error': 'Invalid email or password'}), 401

        return jsonify({'error': 'Method not allowed'}), 405

    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out', 'success')
        return jsonify({'message': 'Logout successful'}), 200
