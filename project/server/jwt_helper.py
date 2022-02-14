from flask import request, jsonify
from functools import wraps
import jwt

from project.server.models.user_model import User
from project.server.config import BaseConfig


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        auth_token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            auth_token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not auth_token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            payload = jwt.decode(
                auth_token, 
                BaseConfig.SECRET_KEY,
                algorithms='HS256'
            )
            current_user = User.query.filter_by(id = payload['sub']).first()
        except:
            return jsonify({
                'message' : 'Token is invalid'
            }), 401
        # returns the current logged in users contex to the routes
        return f(self, current_user, *args, **kwargs)
  
    return decorated

def encode_merchant_token(merchant_id, signature):
    """
    Generates the Auth Token of Merchant
    :return: string
    """
    try:
        payload = {
            'merchantId': merchant_id,
            'signature': signature
        }
        return jwt.encode(
            payload,
            BaseConfig.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_merchant_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(
            auth_token, 
            BaseConfig.SECRET_KEY,
            algorithms='HS256'
        )
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'