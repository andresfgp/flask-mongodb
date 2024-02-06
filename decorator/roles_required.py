# decorator/roles_required.py
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def roles_required(required_roles=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Check if a valid JWT is present in the request
                verify_jwt_in_request()

                # Get the current user's identity from the JWT
                current_user = get_jwt_identity()

                # Check if required roles are specified
                if required_roles is None:
                    # No specific roles required, anyone with a valid token can access
                    return fn(*args, **kwargs)

                # Check if the user identity is available and has a 'role' attribute
                if current_user and isinstance(current_user, dict) and 'role' in current_user:
                    # Check if the user has at least one of the required roles
                    if current_user['role'] not in required_roles:
                        return jsonify({'error': 'Permission denied'}), 403
                else:
                    return jsonify({'error': 'Invalid user identity'}), 401

                # Call the protected function if permissions are granted
                return fn(*args, **kwargs)

            except Exception as e:
                return jsonify({'error': str(e)}), 500

        return wrapper

    return decorator
