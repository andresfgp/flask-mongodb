from flask_bcrypt import Bcrypt
from bson import ObjectId

bcrypt = Bcrypt()

def document_exists(collection, document_id):
    return bool(collection.find_one({'_id': ObjectId(document_id)}))

def create_document(collection, data):
    try:
        result = collection.insert_one(data)
        return str(result.inserted_id), None
    except Exception as e:
        return None, str(e)

def read_all_documents(collection):
    try:
        data = list(collection.find())
        # Convert ObjectId to string for each document
        for item in data:
            item['_id'] = str(item['_id'])
        return data, None
    except Exception as e:
        return None, str(e)

def read_one_document(collection, document_id):
    try:
        if document_exists(collection, document_id):
            data = collection.find_one({'_id': ObjectId(document_id)})
            # Convert ObjectId to string
            data['_id'] = str(data['_id'])
            return data, None
        else:
            return None, 'Document not found'
    except Exception as e:
        return None, str(e)

def update_document(collection, document_id, data):
    try:
        if document_exists(collection, document_id):
            # Encrypt the password before updating
            if 'password' in data:
                data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            result = collection.replace_one({'_id': ObjectId(document_id)}, data)
            return 'Document replaced successfully', None
        else:
            return None, 'Document not found'
    except Exception as e:
        return None, str(e)

def partial_update_document(collection, document_id, data):
    try:
        if document_exists(collection, document_id):
            # Update only the fields provided in the request
            if 'password' in data:
                data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': data})
            return 'Document partially updated successfully', None
        else:
            return None, 'Document not found'
    except Exception as e:
        return None, str(e)

def delete_document(collection, document_id):
    try:
        if document_exists(collection, document_id):
            result = collection.delete_one({'_id': ObjectId(document_id)})
            return 'Document deleted successfully', None
        else:
            return None, 'Document not found'
    except Exception as e:
        return None, str(e)
