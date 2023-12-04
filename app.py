from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson import ObjectId
import os
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "your_secret_key" 
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://aussie-tea-user:aussie123@aussie-tea.xcz2kza.mongodb.net/form?retryWrites=true&w=majority"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Helper function to check if document exists
def document_exists(collection, document_id):
    return bool(collection.find_one({'_id': ObjectId(document_id)}))

# MongoDB Collections
users_collection = mongo.db.users
roles_collection = mongo.db.roles
contact_collection = mongo.db.contact

# User class for Flask-Login
class User(UserMixin):
    pass

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        user = User()
        user.id = str(user_data['_id'])
        return user
    return None

# Login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.get_json()['email']
        password = request.get_json()['password']
        user = users_collection.find_one({'email': email})
        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User()
            user_obj.id = str(user['_id'])
            login_user(user_obj)
            flash('Login successful', 'success')
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'error': 'Method not allowed'}), 405

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return jsonify({'message': 'Logout successful'}), 200

# Helper function to check if document exists
def document_exists(collection, document_id):
    return bool(collection.find_one({'_id': ObjectId(document_id)}))

# CREATE (POST) a new user
@app.route('/users', methods=['POST'])
@login_required
def create_user():
    try:
        data = request.get_json()
        # Encrypt the password before saving to the database
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        result = users_collection.insert_one(data)
        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ALL (GET) users
@app.route('/users', methods=['GET'])
@login_required
def read_users():
    try:
        data = list(users_collection.find())
        # Convert ObjectId to string for each document
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ONE (GET) user
@app.route('/users/<id>', methods=['GET'])
@login_required
def read_one_user(id):
    try:
        if document_exists(users_collection, id):
            data = users_collection.find_one({'_id': ObjectId(id)})
            # Convert ObjectId to string
            data['_id'] = str(data['_id'])
            return jsonify({'result': data}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE (PUT) user
@app.route('/users/<id>', methods=['PUT'])
@login_required
def update_user(id):
    try:
        if document_exists(users_collection, id):
            data = request.get_json()
            # Encrypt the password before updating
            if 'password' in data:
                data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            result = users_collection.replace_one({'_id': ObjectId(id)}, data)
            return jsonify({'message': 'User replaced successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# UPDATE (PATCH) user
@app.route('/users/<id>', methods=['PATCH'])
@login_required
def partial_update_user(id):
    try:
        if document_exists(users_collection, id):
            data = request.get_json()
            # Update only the fields provided in the request
            if 'password' in data:
                data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            result = users_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
            return jsonify({'message': 'User partially updated successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE (DELETE) user
@app.route('/users/<id>', methods=['DELETE'])
@login_required
def delete_user(id):
    try:
        if document_exists(users_collection, id):
            result = users_collection.delete_one({'_id': ObjectId(id)})
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CREATE (POST) a new role
@app.route('/roles', methods=['POST'])
@login_required
def create_role():
    try:
        data = request.get_json()
        result = roles_collection.insert_one(data)
        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ALL (GET) roles
@app.route('/roles', methods=['GET'])
@login_required
def read_roles():
    try:
        data = list(roles_collection.find())
        # Convert ObjectId to string for each document
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ONE (GET) role
@app.route('/roles/<id>', methods=['GET'])
@login_required
def read_one_role(id):
    try:
        if document_exists(roles_collection, id):
            data = roles_collection.find_one({'_id': ObjectId(id)})
            # Convert ObjectId to string
            data['_id'] = str(data['_id'])
            return jsonify({'result': data}), 200
        else:
            return jsonify({'error': 'Role not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE (PUT) role
@app.route('/roles/<id>', methods=['PUT'])
@login_required
def update_role(id):
    try:
        if document_exists(roles_collection, id):
            data = request.get_json()
            result = roles_collection.replace_one({'_id': ObjectId(id)}, data)
            return jsonify({'message': 'Role replaced successfully'}), 200
        else:
            return jsonify({'error': 'Role not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# UPDATE (PATCH) role
@app.route('/roles/<id>', methods=['PATCH'])
@login_required
def partial_update_role(id):
    try:
        if document_exists(roles_collection, id):
            data = request.get_json()
            # Update only the fields provided in the request
            result = roles_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
            return jsonify({'message': 'Role partially updated successfully'}), 200
        else:
            return jsonify({'error': 'Role not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE (DELETE) role
@app.route('/roles/<id>', methods=['DELETE'])
@login_required
def delete_role(id):
    try:
        if document_exists(roles_collection, id):
            result = roles_collection.delete_one({'_id': ObjectId(id)})
            return jsonify({'message': 'Role deleted successfully'}), 200
        else:
            return jsonify({'error': 'Role not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CREATE (POST) a new contact
@app.route('/contact', methods=['POST'])
def create_contact():
    try:
        data = request.get_json()
        data['user_id'] = current_user.id  # Add the current user's ID to the contact
        result = contact_collection.insert_one(data)
        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ALL (GET) contacts
@app.route('/contact', methods=['GET'])
@login_required
def read_contacts():
    try:
        data = list(contact_collection.find({'user_id': current_user.id}))
        # Convert ObjectId to string for each document
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ONE (GET) contact
@app.route('/contact/<id>', methods=['GET'])
@login_required
def read_one_contact(id):
    try:
        data = contact_collection.find_one({'_id': ObjectId(id), 'user_id': current_user.id})
        if data:
            # Convert ObjectId to string
            data['_id'] = str(data['_id'])
            return jsonify({'result': data}), 200
        else:
            return jsonify({'error': 'Contact not found or not authorized'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE (PUT) contact
@app.route('/contact/<id>', methods=['PUT'])
@login_required
def update_contact(id):
    try:
        data = request.get_json()
        result = contact_collection.replace_one({'_id': ObjectId(id), 'user_id': current_user.id}, data)
        if result.matched_count > 0:
            return jsonify({'message': 'Contact replaced successfully'}), 200
        else:
            return jsonify({'error': 'Contact not found or not authorized'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE (PATCH) contact
@app.route('/contact/<id>', methods=['PATCH'])
@login_required
def partial_update_contact(id):
    try:
        data = request.get_json()
        # Update only the fields provided in the request
        result = contact_collection.update_one({'_id': ObjectId(id), 'user_id': current_user.id}, {'$set': data})
        if result.matched_count > 0:
            return jsonify({'message': 'Contact partially updated successfully'}), 200
        else:
            return jsonify({'error': 'Contact not found or not authorized'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE (DELETE) contact
@app.route('/contact/<id>', methods=['DELETE'])
@login_required
def delete_contact(id):
    try:
        result = contact_collection.delete_one({'_id': ObjectId(id), 'user_id': current_user.id})
        if result.deleted_count > 0:
            return jsonify({'message': 'Contact deleted successfully'}), 200
        else:
            return jsonify({'error': 'Contact not found or not authorized'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Other routes (CRUD operations, etc.)...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
