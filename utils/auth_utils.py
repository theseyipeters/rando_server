# server/auth_utils.py

import jwt
from datetime import datetime, timedelta
from config import Config

def create_jwt_token(username):
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token
