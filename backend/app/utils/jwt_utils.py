from datetime import datetime, timedelta, timezone
from app.api.models.models import TokenBlocklist
from app.constant.errors import JWT_ERRORS
from app.utils.common_utils import SericeHelper
from flask import jsonify
from flask_jwt_extended import (get_jwt, get_jwt_identity, set_access_cookies,
                                create_access_token)


def check_if_token_in_block_list(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = SericeHelper.token_in_block_list(jti)
    return token_in_redis is not None


# @jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify(JWT_ERRORS["JWT_TOKEN_EXPIRED"]), 401


# invalid_token_loader
def invalid_token_callback(error):
    return jsonify(JWT_ERRORS["JWT_TOKEN_INVALID"]), 401


def unauthorized_token_callback(error_string):
    return jsonify(JWT_ERRORS['JWT_AUTH_REQUIRED']), 401


def refresh_expiring_jwts(response):
    try:
        jti = get_jwt()['jti']
        # Check of the token is alreday revoked if revoked not revoked then refresh the token else not # noqa
        if TokenBlocklist.query.filter_by(jti=jti).first() is None:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response # noqa
        return response
