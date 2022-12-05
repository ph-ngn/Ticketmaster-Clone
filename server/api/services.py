from functools import wraps
import datetime
from typing import Optional
import jwt
from flask import request
from domain import config
from .exceptions import APIException
from . import config as api_config


class JWTService:
    @staticmethod
    def generate_jwt(username: str, account_type: str) -> str:
        payload = {
            'exp': datetime.datetime.now() + datetime.timedelta(days=2),
            'iat': datetime.datetime.now(),
            'sub': username,
            'info': account_type
        }
        return jwt.encode(
            payload,
            config.get('SECRET_KEY'),
            algorithm='HS256'
        )

    @staticmethod
    def parse_auth_header(request_header: dict) -> Optional[str]:
        auth_header = request_header.get('Authorization')
        if auth_header:
            try:
                prefix, token = auth_header.split()
                if prefix != 'Bearer':
                    raise APIException('Token must be of type Bearer', 400)
                else:
                    return token

            except ValueError:
                raise APIException('Malformed authorization header', 400)
        else:
            raise APIException('Request has no authorization header', 400)

    @staticmethod
    def parse_token(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(
                token,
                config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
            return payload['sub'], payload['info']
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise APIException('Invalid or expired token', 401)


def login_required(f):
    @wraps(f)
    def wrapper(ref, *args, **kwargs):
        token = JWTService.parse_auth_header(request.headers)
        username, account_type = JWTService.parse_token(token)
        if account_type not in api_config['ALLOWED_ACCOUNT_TYPES'][type(ref).__name__]:
            raise APIException('Account type not allowed for this api', 403)

        return f(ref, username, *args, **kwargs)
    return wrapper


def params_required(f):
    @wraps(f)
    def wrapper(ref, *args, **kwargs):
        if not kwargs:
            raise APIException("Extra params are required")
        if set(kwargs).symmetric_difference(api_config['REQUIRED_PARAMS'][type(ref).__name__]):
            raise APIException("Missing or extra params")
        if not all(kwargs.values()):
            raise APIException("Params' values can not be empty")

        return f(ref, *args, **kwargs)
    return wrapper


def get_skip_and_limit():
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 0))
        page -= 1 if page > 0 else page
        return page * limit, limit
    except ValueError:
        raise APIException('page and limit parameters must be a number')


def get_search():
    return request.args.get('search', None)
