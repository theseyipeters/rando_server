from flask import Blueprint, request, jsonify
from pymongo.errors import DuplicateKeyError
from extensions import mongo
from utils.auth_utils import create_jwt_token
from passlib.context import CryptContext

auth_bp = Blueprint('auth_bp', __name__)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

@auth_bp.route('/signup', methods=['POST'])
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

    # Check if passwords match
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    hashed_password = pwd_context.hash(password)

    try:
        mongo.db.users.insert_one({
            'email': email,
            'username': username,
            'role': role,
            'password': hashed_password
        })
        return jsonify({'message': 'User created successfully'}), 201
    except DuplicateKeyError:
        return jsonify({'error': 'Username or email already exists'}), 409
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate required fields
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        user = mongo.db.users.find_one({'username': username})

        if user and pwd_context.verify(password, user['password']):
            token = create_jwt_token({'username': username, 'role': user['role']})
            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
