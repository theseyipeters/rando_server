import jwt
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
from config import Config

def create_jwt_token(user_data):
    token = jwt.encode({
        'user_id': user_data['user_id'],
        'username': user_data['username'],
        'role': user_data['role'],
        'exp': datetime.utcnow() + timedelta(hours=24)  # Example expiration time
    }, Config.SECRET_KEY, algorithm="HS256")
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in the Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # The header should be in the format "Bearer <token>"
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user_id = data['user_id']  # Ensure user_id is included in the token
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': 'An error occurred while decoding the token!', 'error': str(e)}), 401

        return f(user_id, *args, **kwargs)
    
    return decorated