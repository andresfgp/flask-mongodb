from flask_bcrypt import Bcrypt
from flask import jsonify, request, make_response
from bson import ObjectId
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, decode_token, get_jwt, jwt_required, create_refresh_token
from blacklist import token_blacklist

bcrypt = Bcrypt()

class User:
    def __init__(self, id, email, full_name="", role="user"):
        self.id = id
        self.email = email
        self.full_name = full_name
        self.role = role

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
        }

def configure_auth(app, users_collection):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_loader_callback(identity):
        user_data = users_collection.find_one({'_id': ObjectId(identity)})
        if user_data:
            user = User(
                id=str(user_data['_id']),
                email=user_data['email'],
                full_name=user_data.get('full_name', ''),
                role=user_data.get('role', 'user'),
            )
            return user.to_dict()

    @app.route('/login', methods=['POST'])
    def login():
        try:
            email = request.json.get('email')
            password = request.json.get('password')

            if not email or not password:
                return jsonify({'error': 'Email and password are required'}), 400

            user = users_collection.find_one({'email': email})
            if user and bcrypt.check_password_hash(user['password'], password):
                access_token = create_access_token(identity=str(user['_id']))
                refresh_token = create_refresh_token(identity=str(user['_id']))

                additional_data = {
                    'user_id': str(user['_id']),
                    'email': user['email'],
                    'full_name': user.get('full_name', ''),
                }
                return jsonify({'message': 'Login successful', 'data': additional_data, 'token': access_token, 'refresh_token': refresh_token}), 200

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

    @app.route('/refresh', methods=['POST'])
    def refresh():
        try:
            refresh_token = request.json.get('refresh_token')
            decoded_token = decode_token(refresh_token)
            new_token = create_access_token(identity=str(decoded_token['sub']["id"]))
            response = make_response(jsonify({'token': new_token }), 200)
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500