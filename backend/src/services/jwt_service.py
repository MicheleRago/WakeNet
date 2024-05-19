from datetime import datetime, timedelta
from flask import current_app
import jwt

def generate_jwt(user):
    payload = {
    'iat': datetime.utcnow(),
    'exp': datetime.utcnow() + timedelta(hours=24),
    'user_id': str(user.id),
    'firstname': user.firstname,
    'lastname': user.lastname,
    'email': user.email,
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'],algorithm='HS256')

def decode_jwt(token):
    data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    return data