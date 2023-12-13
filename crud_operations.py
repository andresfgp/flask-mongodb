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
        'created_at': str(datetime.utcnow()),
        'created_by': current_user_id or 'Guest',
        'is_deleted': False
    }
    data.setdefault('metadata', metadata)
    return data

def update_defaults(data, current_user_id):
    metadata = {
        'updated_at': str(datetime.utcnow()),
        'updated_by': current_user_id or 'Guest'
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
        return None, f"Error creating document: {e}"

def read_all_documents(collection):
    try:
        query = {'metadata.is_deleted': False}
        data = list(collection.find(query))
        for item in data:
            item['_id'] = str(item['_id'])
        return data, None
    except Exception as e:
        return None, f"Error reading documents: {e}"

def read_one_document(collection, document_id):
    try:
        query = {'_id': ObjectId(document_id), 'metadata.is_deleted': False}
        data = collection.find_one(query)
        if data:
            data['_id'] = str(data['_id'])
            return data, None
        else:
            return None, 'Document not found'
    except Exception as e:
        return None, f"Error reading document: {e}"

def update_document(collection, document_id, data):
    try:
        current_user_id = get_current_user()
        if document_exists(collection, document_id):
            data = update_defaults(data, current_user_id)
            data = encrypt_password(data)
            result = replace_document(collection, document_id, data)
            if result.modified_count > 0:
                return 'Document replaced successfully', None
            else:
                return None, 'Document not found or no changes made'
        else:
            return None, 'Document not found'
    except Exception as e:
        return None, f"Error updating document: {e}"

def partial_update_document(collection, document_id, data):
    try:
        current_user_id = get_current_user()
        if document_exists(collection, document_id):
            data = set_defaults(data, current_user_id)
            data = encrypt_password(data)
            
            # Implementing soft delete with 'metadata.is_deleted' field
            if data.get('metadata.is_deleted') is True:
                data['metadata']['deleted_at'] = str(datetime.utcnow())
                data['metadata']['deleted_by'] = current_user_id or 'Guest'

            result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': data})
            if result.modified_count > 0:
                return 'Document partially updated successfully', None
            else:
                return None, 'Document not found or no changes made'
        else:
            return None, 'Document not found'
    except Exception as e:
        return None, f"Error updating document: {e}"

def delete_document(collection, document_id, hard_delete=True):
    try:
        if document_exists(collection, document_id):
            result = None
            if hard_delete:
                result = collection.delete_one({'_id': ObjectId(document_id)})
            else:
                query = {'_id': ObjectId(document_id)}
                data = {
                    '$set': {
                        'metadata.is_deleted': True,
                        'metadata.deleted_at': str(datetime.utcnow()),
                        'metadata.deleted_by': get_current_user() or 'Guest'
                    }
                }
                result = collection.update_one(query, data)
            if result:
                if hard_delete:
                    if result.deleted_count > 0:
                        return 'Document hard deleted successfully', None
                    else:
                        return None, 'Document not found or no changes made'
                else:
                    return f'Document {"hard" if hard_delete else "soft"} deleted successfully', None
            else:
                return None, 'Document not found'
        else:
            return None, 'Document not found'
    except Exception as e:
        return None, f"Error deleting document: {e}"
