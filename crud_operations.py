# crud_operations.py
from flask_bcrypt import Bcrypt
from bson import ObjectId
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

bcrypt = Bcrypt()

def document_exists(collection, document_id):
    return bool(collection.find_one({'_id': ObjectId(document_id)}))

def get_current_user():
    verify_jwt_in_request(optional=True)
    return get_jwt_identity()

def set_defaults(data, current_user_id):
    metadata = {
        'createdAt': str(datetime.utcnow()),
        'createdBy': current_user_id or 'Guest',
        'isDeleted': False
    }
    data.setdefault('metadata', metadata)
    return data

def update_defaults(data, current_user_id):
    metadata = {
        'updatedAt': str(datetime.utcnow()),
        'updatedBy': current_user_id or 'Guest'
    }
    data.setdefault('metadata', {}).update(metadata)
    return data

def encrypt_password(data):
    password = data.get('password')
    if password:
        data['password'] = bcrypt.generate_password_hash(password).decode('utf-8')
    return data

def replace_document(collection, document_id, data):
    return collection.replace_one({'_id': ObjectId(document_id)}, data)

def create_document(collection, data):
    try:
        current_user_id = get_current_user()
        data = set_defaults(data, current_user_id)
        result = collection.insert_one(data)
        return str(result.inserted_id), None
    except Exception as e:
        return None, f"Error creating element: {e}"

def read_all_documents(collection):
    try:
        query = {'metadata.isDeleted': False}
        data = list(collection.find(query))
        for item in data:
            item['_id'] = str(item['_id'])
        return data, None
    except Exception as e:
        return None, f"Error reading elements: {e}"

def read_one_document(collection, document_id):
    try:
        query = {'_id': ObjectId(document_id), 'metadata.isDeleted': False}
        data = collection.find_one(query)
        if data:
            data['_id'] = str(data['_id'])
            return data, None
        else:
            return None, 'Element not found'
    except Exception as e:
        return None, f"Error reading element: {e}"

def update_document(collection, document_id, data):
    try:
        current_user_id = get_current_user()
        if document_exists(collection, document_id):
            data = update_defaults(data, current_user_id)
            data = encrypt_password(data)
            result = replace_document(collection, document_id, data)
            if result.modified_count > 0:
                return 'Element replaced successfully', None
            else:
                return None, 'Element not found or no changes made'
        else:
            return None, 'Element not found'
    except Exception as e:
        return None, f"Error updating element: {e}"

def partial_update_document(collection, document_id, data):
    try:
        current_user_id = get_current_user()
        if document_exists(collection, document_id):
            data = set_defaults(data, current_user_id)
            data = encrypt_password(data)
            
            # Implementing soft delete with 'metadata.is_deleted' field
            if data.get('metadata.isDeleted') is True:
                data['metadata']['deletedAt'] = str(datetime.utcnow())
                data['metadata']['deletedBy'] = current_user_id or 'Guest'

            result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': data})
            if result.modified_count > 0:
                return 'Element partially updated successfully', None
            else:
                return None, 'Element not found or no changes made'
        else:
            return None, 'Element not found'
    except Exception as e:
        return None, f"Error updating element: {e}"

def delete_document(collection, document_id, hard_delete=False):
    try:
        if document_exists(collection, document_id):
            result = None
            if hard_delete:
                result = collection.delete_one({'_id': ObjectId(document_id)})
            else:
                query = {'_id': ObjectId(document_id)}
                data = {
                    '$set': {
                        'metadata.isDeleted': True,
                        'metadata.deletedAt': str(datetime.utcnow()),
                        'metadata.deletedBy': get_current_user() or 'Guest'
                    }
                }
                result = collection.update_one(query, data)
            if result:
                if hard_delete:
                    if result.deleted_count > 0:
                        return 'Element hard deleted successfully', None
                    else:
                        return None, 'Element not found or no changes made'
                else:
                    return f'Element {"hard" if hard_delete else "soft"} deleted successfully', None
            else:
                return None, 'Element not found'
        else:
            return None, 'Element not found'
    except Exception as e:
        return None, f"Error deleting element: {e}"

def delete_documents(collection, document_ids, hard_delete=False):
    results = None
    for document_id in document_ids:
        delete_status, error_message = delete_document(collection, document_id, hard_delete)
        if delete_status:
            results=document_id

    if not results:  # Check the flag to determine if no documents were successfully deleted
        return None, 'No elements found'
    if not error_message:  # Check the flag to determine if no documents were successfully deleted
        return None, error_message

    return results, None