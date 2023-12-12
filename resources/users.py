from flask import jsonify, request
from flask_jwt_extended import jwt_required
from crud_operations import create_document, read_all_documents, read_one_document, update_document, partial_update_document, delete_document

def configure_users_routes(app, users_collection, bcrypt):
    @app.route('/users', methods=['POST'])
    @jwt_required()
    def create_user():
        try:
            data = request.get_json()
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
    def update_user(id):
        try:
            data = request.get_json()
            result, error = update_document(users_collection, id, data)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<id>', methods=['PATCH'])
    @jwt_required()
    def partial_update_user(id):
        try:
            data = request.get_json()
            result, error = partial_update_document(users_collection, id, data)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<id>', methods=['DELETE'])
    @jwt_required()
    def delete_user(id):
        try:
            result, error = delete_document(users_collection, id)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
