# resources/contact.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from crud_operations import create_document, read_all_documents, read_one_document, update_document, partial_update_document, delete_document
from decorator.roles_required import roles_required
from init_app import get_collection

blp = Blueprint("Contact", "contact", description="Operations on contact")

def get_contact_collection():
     return get_collection('contact')

@blp.route('/contact', methods=['POST'])
@jwt_required()
# @roles_required(required_roles=['admin'])
def create_contact():
    try:
        data = request.get_json()
        result, error = create_document(get_contact_collection(), data)
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'id': result}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/contact', methods=['GET'])
@jwt_required()
@roles_required(required_roles=['admin'])
def read_contacts():
    try:
        data, error = read_all_documents(get_contact_collection())
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/contact/<id>', methods=['GET'])
@jwt_required()
def read_one_contact(id):
    try:
        print('entre')
        data, error = read_one_document(get_contact_collection(), id)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/contact/<id>', methods=['PUT'])
@jwt_required()
def update_contact(id):
    try:
        data = request.get_json()
        result, error = update_document(get_contact_collection(), id, data)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/contact/<id>', methods=['PATCH'])
@jwt_required()
def partial_update_contact(id):
    try:
        data = request.get_json()
        result, error = partial_update_document(get_contact_collection(), id, data)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/contact/<id>', methods=['DELETE'])
@jwt_required()
def hard_delete_contact(id):
    try:
        result, error = delete_document(get_contact_collection(), id, True)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/contact/<id>/soft-delete', methods=['DELETE'])
@jwt_required()
@roles_required(required_roles=['admin'])
def soft_delete_contact(id):
    try:
        result, error = delete_document(get_contact_collection(), id, False)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
