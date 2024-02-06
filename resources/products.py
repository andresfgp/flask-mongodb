# resources/products.py
from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask_bcrypt import Bcrypt
from crud_operations import create_document, read_all_documents, read_one_document, update_document, partial_update_document, delete_document, delete_documents
from decorator.roles_required import roles_required
from schemas.products import ProductSchema, ProductUpdateSchema, ProductPatchSchema
from init_app import get_collection

product_schema = ProductSchema()
product_update_schema = ProductUpdateSchema()
product_patch_schema = ProductPatchSchema()

blp = Blueprint("Products", "products", description="Operations on products")
bcrypt = Bcrypt()

def get_products_collection():
     return get_collection('products')
    
@blp.route('/',strict_slashes=False, methods=['POST'])
@jwt_required()
@roles_required(required_roles=['admin']) 
def create_product():
    try:
        data = request.get_json()

        # Validate product data
        errors = product_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400

        # Check if email already exists
        existing_product = get_products_collection().find_one({'name': data['name']})
        if existing_product:
            return jsonify({'error': 'Product already exists'}), 400

        result, error = create_document(get_products_collection(), data)
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'id': result}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/', strict_slashes=False, methods=['GET'])
@jwt_required()
@roles_required(required_roles=['admin'])
def read_products():
    try:
        data, error = read_all_documents(get_products_collection())
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/<id>', strict_slashes=False, methods=['GET'])
@jwt_required()
@roles_required(required_roles=['admin'])
def read_one_product(id):
    try:
        data, error = read_one_document(get_products_collection(), id)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/<id>', strict_slashes=False, methods=['PUT'])
@jwt_required()
@roles_required(required_roles=['admin'])
def update_product(id):
    try:
        data = request.get_json()

        # Validate product data for update
        errors = product_update_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400

        # Check if email already exists
        existing_product = get_products_collection().find_one({'name': data['name'], '_id': {'$ne': id}})
        if existing_product:
            return jsonify({'error': 'Product already exists'}), 400

        # Default role as user
        data['role'] = data.get('role', 'user')

        result, error = update_document(get_products_collection(), id, data)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blp.route('/<id>', strict_slashes=False, methods=['PATCH'])
@jwt_required()
@roles_required(required_roles=['admin'])
def partial_update_product(id):
    try:
        data = request.get_json()

        # Validate product data for patch
        errors = product_patch_schema.validate(data)
        if errors:
            return jsonify({'error': errors}), 400
        
        object_id = ObjectId(id)
        existing_product = get_products_collection().find_one({'_id': object_id})
        if not existing_product:
            return jsonify({'error': 'Product not found'}), 404

        # Check if email already exists
        if 'name' in data:
            existing_product_with_name = get_products_collection().find_one({'name': data['name'], '_id': {'$ne': id}})
            if existing_product_with_name:
                return jsonify({'error': 'Product already exists'}), 400

        result, error = partial_update_document(get_products_collection(), id, data)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@blp.route('/', strict_slashes=False, methods=['DELETE'])
@jwt_required()
@roles_required(required_roles=['admin'])
def bulk_delete_products():
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({'error': 'Invalid or no JSON data provided'}), 400

        document_ids = request_data.get('ids')
        if not document_ids:
            return jsonify({'error': 'No document IDs provided'}), 400

        hard_delete = request_data.get('hardDelete', False)
        results, error = delete_documents(get_products_collection(), document_ids, hard_delete)
        if error:
            return jsonify({'error': error}), 404
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500