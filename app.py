from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://aussie-tea-user:aussie123@aussie-tea.xcz2kza.mongodb.net/form?retryWrites=true&w=majority"


mongo = PyMongo(app)
# Helper function to check if document exists
def document_exists(collection, document_id):
    return bool(collection.find_one({'_id': ObjectId(document_id)}))

# CREATE (POST)
@app.route('/contact', methods=['POST'])
def create():
    try:
        data = request.get_json()
        result = mongo.db['contact'].insert_one(data)
        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ALL (GET)
@app.route('/contact', methods=['GET'])
def read():
    try:
        data = list(mongo.db['contact'].find())
        # Convert ObjectId to string for each document
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ONE (GET)
@app.route('/contact/<id>', methods=['GET'])
def read_one(id):
    try:
        if document_exists(mongo.db['contact'], id):
            data = mongo.db['contact'].find_one({'_id': ObjectId(id)})
            # Convert ObjectId to string
            data['_id'] = str(data['_id'])
            return jsonify({'result': data}), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE (PUT)
@app.route('/contact/<id>', methods=['PUT'])
def update(id):
    try:
        if document_exists(mongo.db['contact'], id):
            data = request.get_json()
            result = mongo.db['contact'].replace_one({'_id': ObjectId(id)}, data)
            return jsonify({'message': 'Document replaced successfully'}), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# UPDATE (PATCH)
@app.route('/contact/<id>', methods=['PATCH'])
def partial_update(id):
    try:
        if document_exists(mongo.db['contact'], id):
            data = request.get_json()
            # Update only the fields provided in the request
            result = mongo.db['contact'].update_one({'_id': ObjectId(id)}, {'$set': data})
            return jsonify({'message': 'Document partially updated successfully'}), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE (DELETE)
@app.route('/contact/<id>', methods=['DELETE'])
def delete(id):
    try:
        if document_exists(mongo.db['contact'], id):
            result = mongo.db['contact'].delete_one({'_id': ObjectId(id)})
            return jsonify({'message': 'Document deleted successfully'}), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
