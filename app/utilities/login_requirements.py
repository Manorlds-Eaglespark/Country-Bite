import os
import jwt
from functools import wraps
from flask import request
from flask import make_response, request, jsonify, json

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        access_token = get_token()
        if access_token:
            access_token = str(access_token).split(" ")[0]
            user_detail = decode_token(access_token)
            if not isinstance(user_detail, list):
                return make_response(jsonify({"status": 401, "error": user_detail})), 401
            current_user  =  user_detail[0] 
            user_country =  user_detail[1]
            return f(current_user, user_country, *args, **kwargs)
        else:
            return make_response(jsonify({"status":401, "error": "A Resource Token is required. Sign-in or log-in"})), 401
    return wrap

def get_token(): 
    auth_header = request.headers.get('Authorization')
    return auth_header

def decode_token(token):
    try:
        payload = jwt.decode(
            token, str(
                os.getenv('SECRET')), algorithms='HS256')
        return [payload['sub'], payload['country'], payload['rle']]
    except jwt.ExpiredSignatureError:
        return "Expired token. Please login to get a new token"
    except jwt.InvalidTokenError:
        return "Invalid token. Please register or login"
    return None
    