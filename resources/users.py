# resources/users.py
from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask_bcrypt import Bcrypt
from crud_operations import create_document, read_all_documents, read_one_document, update_document, partial_update_document, delete_document, delete_documents
from decorator.roles_required import roles_required
from schemas.users import UserSchema, UserUpdateSchema, UserPatchSchema
from init_app import get_collection

user_schema = UserSchema()
user_update_schema = UserUpdateSchema()
user_patch_schema = UserPatchSchema()

blp = Blueprint("Users", "users", description="Operations on users")
bcrypt = Bcrypt()

def get_users_collection():
     return get_collection('users')
    
@blp.route('/',strict_slashes=False, methods=['POST'])
@jwt_required()
# @roles_required(required_roles=['admin']) 
def create_user():
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

        # Create full_name by combining first_name and last_name
        data['fullName'] = f"{data.get('firstName', '')} {data.get('lastName', '')}"

        # Encrypt the password before saving to the database
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        result, error = create_document(get_users_collection(), data)
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'id': result}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/', strict_slashes=False, methods=['GET'])
@jwt_required()
@roles_required(required_roles=['admin'])
def read_users():
    try:
        data, error = read_all_documents(get_users_collection())
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/<id>', strict_slashes=False, methods=['GET'])
@jwt_required()
@roles_required(required_roles=['admin'])
def read_one_user(id):
    try:
        data, error = read_one_document(get_users_collection(), id)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/<id>', strict_slashes=False, methods=['PUT'])
@jwt_required()
@roles_required(required_roles=['admin'])
def update_user(id):
    try:
        data = request.get_json()

        # Validate user data for update
        errors = user_update_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400

        # Check if email already exists
        existing_user = get_users_collection().find_one({'email': data['email'], '_id': {'$ne': id}})
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400

        # Update fullName by combining firstName and lastName
        data['fullName'] = f"{data.get('firstName', '')} {data.get('lastName', '')}"

        # Default role as public
        data['role'] = data.get('role', 'public')

        # Encrypt the password before saving to the database
        if 'password' in data:
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        result, error = update_document(get_users_collection(), id, data)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/<id>', strict_slashes=False, methods=['PATCH'])
@jwt_required()
@roles_required(required_roles=['admin'])
def partial_update_user(id):
    try:
        data = request.get_json()

        # Validate user data for patch
        errors = user_patch_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400
        
        object_id = ObjectId(id)
        existing_user = get_users_collection().find_one({'_id': object_id})
        if not existing_user:
            return jsonify({'error': 'User not found'}), 404

        # Check if email already exists
        if 'email' in data:
            existing_user_with_email = get_users_collection().find_one({'email': data['email'], '_id': {'$ne': id}})
            if existing_user_with_email:
                return jsonify({'error': 'Email already exists'}), 400

        # Update full_name by combining first_name and last_name
        if 'firstName' in data or 'lastName' in data:
            firstName = data.get('first_name', existing_user.get('firstName', ''))
            lastName = data.get('lastName', existing_user.get('lastName', ''))
            data['fullName'] = f"{firstName} {lastName}"

        # Encrypt the password before saving to the database
        if 'password' in data:
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        result, error = partial_update_document(get_users_collection(), id, data)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@blp.route('/', strict_slashes=False, methods=['DELETE'])
@jwt_required()
@roles_required(required_roles=['admin'])
def bulk_delete_users():
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({'error': 'Invalid or no JSON data provided'}), 400

        document_ids = request_data.get('ids')
        if not document_ids:
            return jsonify({'error': 'No document IDs provided'}), 400

        hard_delete = request_data.get('hardDelete', False)
        results, error = delete_documents(get_users_collection(), document_ids, hard_delete)
        if error:
            return jsonify({'error': error}), 404
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500