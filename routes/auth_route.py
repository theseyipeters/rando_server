from flask import Blueprint, request, jsonify
from pymongo.errors import DuplicateKeyError
from extensions import mongo
from utils.auth_utils import create_jwt_token
from passlib.context import CryptContext
from datetime import datetime
import uuid
import re

auth_bp = Blueprint('auth_bp', __name__)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_role(role):
    valid_roles = {
        "Frontend Engineer", "Backend Engineer", "Full-stack Engineer", 
        "Mobile Developer", "DevOps Engineer", "API Developers", 
        "Data Analyst", "Data Scientist", "Project Manager"
    }
    return role in valid_roles

# def generate_numeric_id():
#     return str(int(uuid.uuid4().int >> 64))

@auth_bp.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    role = data.get('role')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Validate required fields
    if not all([email, username, role, password, confirm_password]):
        return jsonify({'error': 'All fields are required'}), 400

    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if not validate_role(role):
        return jsonify({'error': 'Invalid role'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    hashed_password = pwd_context.hash(password)

    user_id = str(uuid.uuid4().int)[:12]

    try:
        user_data = {
            'user_id': user_id,
            'email': email,
            'username': username,
            'role': role,
            'password': hashed_password,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        inserted_user = mongo.db.users.insert_one(user_data)
        user_data['_id'] = str(inserted_user.inserted_id)  # Convert ObjectId to string
        user_data.pop('password')  # Do not return the password hash
        return jsonify({"success": "true", 'message': 'User created successfully', "data": user_data}), 201
    except DuplicateKeyError:
        return jsonify({'error': 'Username or email already exists'}), 409
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        user = mongo.db.users.find_one({'username': username})

        if user and pwd_context.verify(password, user['password']):
            token = create_jwt_token({
                'user_id': user['user_id'],
                'username': username,
                'role': user['role']
            })
            response_data = {
                "email": user.get('email', ''),
                "username": user.get('username', ''),
                "role": user['role'],
                "created_at": user['created_at'].isoformat(),
                "updated_at": user['updated_at'].isoformat(),
                "id": user['user_id'],  # Use user_id instead of MongoDB _id
                "isNew": True,
                "token": token
            }
            return jsonify({"success": "true", "message": "Login successful", "data": response_data}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
