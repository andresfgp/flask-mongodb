from flask_bcrypt import Bcrypt
from flask import jsonify, request
from bson import ObjectId
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from blacklist import token_blacklist

bcrypt = Bcrypt()

class User:
    def __init__(self, id, email, full_name=""):
        self.id = id
        self.email = email
        self.full_name = full_name

def configure_auth(app, users_collection):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_loader_callback(identity):
        user_data = users_collection.find_one({'_id': ObjectId(identity)})
        if user_data:
            return User(id=str(user_data['_id']), email=user_data['email'], full_name=user_data.get('full_name', ''))

    @app.route('/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return jsonify({'error': 'Email and password are required'}), 400

            user = users_collection.find_one({'email': email})
            if user and bcrypt.check_password_hash(user['password'], password):
                token = create_access_token(identity=str(user['_id']))
                additional_data = {
                    'user_id': str(user['_id']),
                    'email': user['email'],
                    'full_name': user.get('full_name', ''),
                }
                return jsonify({'message': 'Login successful', 'data': additional_data, 'token': token}), 200

            return jsonify({'error': 'Invalid email or password'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        try:
            jti = get_jwt()['jti']
            app.config['JWT_BLACKLIST_ENABLED'] = True
            app.config['JWT_BLACKLIST_TOKEN_CHECK'] = 'refresh'
            token_blacklist.add(jti)
            return jsonify({'message': 'Logout successful'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
