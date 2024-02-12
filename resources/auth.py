# resources/auth.py
from flask_bcrypt import Bcrypt
from flask import jsonify, request, make_response, current_app
from bson import ObjectId
from flask_jwt_extended import jwt_required, create_access_token, decode_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity
from blacklist import token_blacklist
from flask_smorest import Blueprint
from init_app import get_collection, jwt
from schemas.users import UserSchema
from crud_operations import create_document

user_schema = UserSchema()
bcrypt = Bcrypt()
blp = Blueprint("Auth", "auth", description="Operations on auth")

def get_users_collection():
     return get_collection('users')
class User:
    def __init__(self, id, email, fullName="", role="user"):
        self.id = id
        self.email = email
        self.fullName = fullName
        self.role = role

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'fullName': self.fullName,
            'role': self.role,
        }
    
@jwt.user_identity_loader
def user_loader_callback(identity):
    user_data = get_users_collection().find_one({'_id': ObjectId(identity)})
    if user_data:
        user = User(
            id=str(user_data['_id']),
            email=user_data['email'],
            fullName=user_data.get('fullName', ''),
            role=user_data.get('role', 'user'),
        )
        return user.to_dict()

@blp.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = get_users_collection().find_one({'email': email, 'metadata.isDeleted': False})
        if user and bcrypt.check_password_hash(user['password'], password):
            accessToken = create_access_token(identity=str(user['_id']))
            refreshToken = create_refresh_token(identity=str(user['_id']))

            # Construct the response user object
            userData = {
                "id": str(user['_id']),
                "displayName": user.get('fullName'),
                "email": user['email'],
                "photoURL": user.get('photoURL'),
                "phoneNumber": user.get('phoneNumber'),
                "country": user.get('country'),
                "address": user.get('address'),
                "state": user.get('state'),
                "city": user.get('city'),
                "zipCode": user.get('zipCode'),
                "about": user.get('about'),
                "role": user.get('role', 'user'),
                "isPublic": user.get('isPublic', True),
            }
            # Construct the response
            return jsonify({
                "accessToken": accessToken,
                "refreshToken": refreshToken,
                "user": userData
            }), 200
        return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Validate user data
        errors = user_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400

        # Check if email already exists
        existing_user = get_users_collection().find_one({'email': data['email']})
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400

        # Create fullName by combining firstName and lastName
        data['fullName'] = f"{data.get('firstName', '')} {data.get('lastName', '')}"
        
        # Default role as public
        data['role'] = data.get('role', 'admin')
        data['status'] = data.get('status', 'active')

        # Encrypt the password before saving to the database
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        result, error = create_document(get_users_collection(), data)
        if error:
            return jsonify({'error': error}), 500

        # Create access and refresh tokens for the new user
        accessToken = create_access_token(identity=str(result))
        refreshToken = create_refresh_token(identity=str(result))

        # Construct the response user object
        userData = {
            "id": result,
            "displayName": data.get('fullName'),
            "email": data['email'],
            "photoURL": data.get('photoURL', ''),
            "phoneNumber": data.get('phoneNumber', ''),
            "country": data.get('country', ''),
            "address": data.get('address', ''),
            "state": data.get('state', ''),
            "city": data.get('city', ''),
            "zipCode": data.get('zipCode', ''),
            "about": data.get('about'),
            "role": data.get('role', 'admin'), # Updated to reflect default admin role
            "isPublic": data.get('isPublic', True),
        }

        # Construct the response
        return jsonify({
            "accessToken": accessToken,
            "refreshToken": refreshToken,
            "user": userData
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_identity = get_jwt_identity()
        
        # Extract the user ID from the identity dictionary
        user_id = user_identity['id']

        # Find the user in the database
        user = get_users_collection().find_one({'_id': ObjectId(user_id), 'metadata.isDeleted': False})

        if user:
            # Construct the response user object
            userData = {
                "id": str(user['_id']),
                "displayName": user.get('fullName'),
                "email": user['email'],
                "photoURL": user.get('photoURL'),
                "phoneNumber": user.get('phoneNumber'),
                "country": user.get('country'),
                "address": user.get('address'),
                "state": user.get('state'),
                "city": user.get('city'),
                "zipCode": user.get('zipCode'),
                "about": user.get('about'),
                "role": user.get('role', 'user'),
                "isPublic": user.get('isPublic', True),
            }
            return jsonify({'user': userData}), 200

        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()['jti']
        token_blacklist.add(jti)
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/refresh', methods=['POST'])
def refresh():
    try:
        refreshToken = request.json.get('refreshToken')
        decodedToken = decode_token(refreshToken)
        newToken = create_access_token(identity=str(decodedToken['sub']["id"]))
        response = make_response(jsonify({'token': newToken }), 200)
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

