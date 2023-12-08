from flask import jsonify, request
from flask_login import login_required, current_user
from crud_operations import create_document, read_all_documents, read_one_document, update_document, partial_update_document, delete_document

def configure_contact_routes(app, contact_collection):
    @app.route('/contact', methods=['POST'])
    def create_contact():
        try:
            data = request.get_json()
            data['user_id'] = current_user.id  # Add the current user's ID to the contact
            result, error = create_document(contact_collection, data)
            if error:
                return jsonify({'error': error}), 500
            return jsonify({'id': result}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/contact', methods=['GET'])
    def read_contacts():
        try:
            data, error = read_all_documents(contact_collection)
            if error:
                return jsonify({'error': error}), 500
            return jsonify({'result': data}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/contact/<id>', methods=['GET'])
    def read_one_contact(id):
        try:
            data, error = read_one_document(contact_collection, id)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'result': data}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/contact/<id>', methods=['PUT'])
    def update_contact(id):
        try:
            data = request.get_json()
            result, error = update_document(contact_collection, id, data)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/contact/<id>', methods=['PATCH'])
    def partial_update_contact(id):
        try:
            data = request.get_json()
            result, error = partial_update_document(contact_collection, id, data)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/contact/<id>', methods=['DELETE'])
    def delete_contact(id):
        try:
            result, error = delete_document(contact_collection, id)
            if error:
                return jsonify({'error': error}), 404
            return jsonify({'message': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
