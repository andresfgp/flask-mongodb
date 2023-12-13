from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from crud_operations import create_document, read_all_documents, read_one_document, update_document, partial_update_document, delete_document
from decorator.roles_required import roles_required
from schemas import UserSchema, UserUpdateSchema, UserPatchSchema

user_schema = UserSchema()
user_update_schema = UserUpdateSchema()
user_patch_schema = UserPatchSchema()

def configure_users_routes(app, users_collection, bcrypt):
    @app.route('/users', methods=['POST'])
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
            existing_user = users_collection.find_one({'email': data['email']})
            if existing_user:
                return jsonify({'error': 'Email already exists'}), 400

            # Create full_name by combining first_name and last_name
            data['full_name'] = f"{data.get('first_name', '')} {data.get('last_name', '')}"

            # Encrypt the password before saving to the database
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            result, error = create_document(users_collection, data)
            if error:
                return jsonify({'error': error}), 500
            return jsonify({'id': result}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/users', methods=['GET'])
    @jwt_required()
    @roles_required(required_roles=['admin'])
    def read_users():
        try:
            data, error = read_all_documents(users_collection)
            if error:
                return jsonify({'error': error}), 500
            return jsonify({'result': data}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<id>', methods=['GET'])
    @jwt_required()
    @roles_required(required_roles=['admin'])
    def read_one_user(id):
        try:
            data, error = read_one_document(users_collection, id)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'result': data}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<id>', methods=['PUT'])
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
            existing_user = users_collection.find_one({'email': data['email'], '_id': {'$ne': id}})
            if existing_user:
                return jsonify({'error': 'Email already exists'}), 400

            # Update full_name by combining first_name and last_name
            data['full_name'] = f"{data.get('first_name', '')} {data.get('last_name', '')}"

            # Encrypt the password before saving to the database
            if 'password' in data:
                data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            result, error = update_document(users_collection, id, data)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<id>', methods=['PATCH'])
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
            existing_user = users_collection.find_one({'_id': object_id})
            if not existing_user:
                return jsonify({'error': 'User not found'}), 404

            # Check if email already exists
            if 'email' in data:
                existing_user_with_email = users_collection.find_one({'email': data['email'], '_id': {'$ne': id}})
                if existing_user_with_email:
                    return jsonify({'error': 'Email already exists'}), 400

            # Update full_name by combining first_name and last_name
            if 'first_name' in data or 'last_name' in data:
                first_name = data.get('first_name', existing_user.get('first_name', ''))
                last_name = data.get('last_name', existing_user.get('last_name', ''))
                data['full_name'] = f"{first_name} {last_name}"

            # Encrypt the password before saving to the database
            if 'password' in data:
                data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            result, error = partial_update_document(users_collection, id, data)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<id>', methods=['DELETE'])
    @jwt_required()
    @roles_required(required_roles=['admin'])
    def hard_delete_user(id):
        try:
            result, error = delete_document(users_collection, id, True)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<id>/soft-delete', methods=['DELETE'])
    @jwt_required()
    @roles_required(required_roles=['admin'])
    def soft_delete_user(id):
        try:
            result, error = delete_document(users_collection, id, False)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500