from functools import wraps

import jwt
from flask import abort
from flask import current_app as app
from flask import request


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(
            auth_token, app.config.get("SECRET_KEY"), algorithms="HS256", verify=True
        )
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return "invalid"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.headers.get("Authorization")
        if auth_token:
            auth_token = auth_token.split(" ")[-1]
        payload = decode_auth_token(auth_token)
        if payload == "expired":
            abort(401, "Signature expired. Please log in again.")
        elif payload == "invalid":
            abort(401, "Invalid token. Please log in again.")
        setattr(decorated, "email", payload)
        return f(*args, **kwargs)

    return decorated

def check_internal_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # app.logger.info(app.config['API_KEY'])
        # app.logger.info(request.headers.get('API-KEY'))
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            abort(404, "api key not found!!")
        if api_key != app.config.get("X_API_KEY"):
            abort(401, "Invalid Key")
        return f(*args, **kwargs)
    return decorated