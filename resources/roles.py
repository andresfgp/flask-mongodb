from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from crud_operations import create_document, read_all_documents, read_one_document, update_document, partial_update_document, delete_document
from decorator.roles_required import roles_required
from init_app import get_collection

blp = Blueprint("Roles", "roles", description="Operations on roles")

def get_roles_collection():
     return get_collection('roles')

@blp.route('/roles', methods=['POST'])
@jwt_required()
@roles_required(required_roles=['admin'])
def create_role():
    try:
        data = request.get_json()
        result, error = create_document(get_roles_collection(), data)
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'id': result}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/roles', methods=['GET'])
@jwt_required()
@roles_required(required_roles=['admin'])
def read_roles():
    try:
        data, error = read_all_documents(get_roles_collection())
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/roles/<id>', methods=['GET'])
@jwt_required()
@roles_required(required_roles=['admin'])
def read_one_role(id):
    try:
        data, error = read_one_document(get_roles_collection(), id)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/roles/<id>', methods=['PUT'])
@jwt_required()
@roles_required(required_roles=['admin'])
def update_role(id):
    try:
        data = request.get_json()
        result, error = update_document(get_roles_collection(), id, data)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/roles/<id>', methods=['PATCH'])
@jwt_required()
@roles_required(required_roles=['admin'])
def partial_update_role(id):
    try:
        data = request.get_json()
        result, error = partial_update_document(get_roles_collection(), id, data)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/roles/<id>', methods=['DELETE'])
@jwt_required()
@roles_required(required_roles=['admin'])
def hard_delete_role(id):
    try:
        result, error = delete_document(get_roles_collection(), id, True)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/roles/<id>/soft-delete', methods=['DELETE'])
@jwt_required()
@roles_required(required_roles=['admin'])
def soft_delete_role(id):
    try:
        result, error = delete_document(get_roles_collection(), id, False)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
