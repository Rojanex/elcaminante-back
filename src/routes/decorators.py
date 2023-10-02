from firebase_admin import auth
from functools import wraps
from flask import request, jsonify


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            id_token = request.headers['Authorization']
            try:
                decoded_token = auth.verify_id_token(id_token)
                if decoded_token['role'] != role:
                    return jsonify({"message": "Access denied"}), 403
                else:
                    print('correct_ role')
            except Exception as e:
                return jsonify({"message": "Invalid token"}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator