# resources/images.py
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify
from werkzeug.utils import secure_filename
from init_app import get_gridfs
from bson import ObjectId
from io import BytesIO
from flask import send_file

blp = Blueprint("Images", "images", description="Operations on images")

create_gridfs = get_gridfs()

@blp.route('/', strict_slashes=False, methods=['POST'])
def upload_image():
    gridfs = create_gridfs()
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in request'}), 404

    image = request.files['image']
    filename = secure_filename(image.filename)

    image_id = gridfs.put(image, filename=filename)

    return jsonify({'message': 'Image uploaded successfully', 'image_id': str(image_id)}), 200

@blp.route('/<image_id>', strict_slashes=False, methods=['GET'])
def get_image(image_id):
    gridfs = create_gridfs()
    try:
        object_id = ObjectId(image_id)
    except:
        return jsonify({'error': 'Invalid image ID'}), 400


    grid_out = gridfs.get(object_id)
    if not grid_out:
        return jsonify({'error': 'Image not found'}), 404

    # Create a BytesIO object and stream the file data into it
    data = BytesIO()
    data.write(grid_out.read())
    data.seek(0)
    # Send the file data as a response
    return send_file(
        data,
        mimetype=grid_out.content_type,
        as_attachment=True,
        attachment_filename=grid_out.filename
    )

@blp.route('/<image_id>', strict_slashes=False, methods=['PUT'])
def update_image(image_id):
    gridfs = create_gridfs()
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in request'}), 404

    try:
        object_id = ObjectId(image_id)
    except:
       return jsonify({'error': 'Invalid image ID'}), 400

    image = request.files['image']
    new_filename = secure_filename(image.filename)

    gridfs.delete(object_id)
    new_image_id = gridfs.put(image, filename=new_filename)

    return jsonify({'message': 'Image updated successfully', 'new_image_id': str(new_image_id)}), 200

@blp.route('/<image_id>', strict_slashes=False, methods=['DELETE'])
def delete_image(image_id):
    gridfs = create_gridfs()
    try:
        object_id = ObjectId(image_id)
    except Exception as e:
        return jsonify({'error': 'Invalid image ID'}), 400

    if not gridfs.exists(object_id):
        return jsonify({'error': 'Image not found'}), 404

    try:
        gridfs.delete(object_id)
        return jsonify({'message': 'Image deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Error deleting file'}), 400
