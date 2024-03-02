from app.api.models.models import Posts, User
from app.constant.custom_exceptions import (PostNotFoundException,
                                            UserExistException,
                                            UserDoesNotExistException)
from app.constant.errors import ERRORS
from flask_marshmallow import Marshmallow, Schema
from marshmallow import ValidationError, fields, validate, validates_schema
from sqlalchemy import func

ma = Marshmallow()


class PostsSchema(Schema):
    post_content = fields.Str(required=True, validate=validate.Length(min=5))
    data = fields.List(fields.Dict(), dump_only=True)


class PostLikeSchema(Schema):
    post_id = fields.Int()
    data = fields.List(fields.Dict(), dump_only=True)

    @validates_schema
    def validate_like_data(self, data, *args, **kwargs):
        post_id = data.get("post_id")
        if post_id is None:
            raise ValidationError(ERRORS["POST_ID_REQU"])

        if Posts.query.get(post_id) is None:
            raise PostNotFoundException(ERRORS["POST_NOT_FOUND"])


class RegisterSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    data = fields.List(fields.Dict(), dump_only=True)

    @validates_schema
    def validate_user_on_registration(self, data, *args, **kwargs):
        _username = data.get("username")
        _password = data.get("password")

        if (_username and _password) is None:
            raise ValidationError(ERRORS["USER_NAME_AND_PASS_REQUIRED"])

        lower_user = _username.lower()
        if User.query.filter(func.lower(User.username) == lower_user).first() is not None: # noqa
            raise UserExistException(ERRORS["USER_EXISTS"])

        if len(_password) < 8:
            raise ValidationError(ERRORS["SHORT_PASS_LEN"])


class LoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    data = fields.List(fields.Dict(), dump_only=True)

    @validates_schema
    def validate_user_on_registration(self, data, *args, **kwargs):
        _username = data.get("username")
        _password = data.get("password")

        if (_username and _password) is None:
            raise ValidationError(ERRORS["USER_NAME_AND_PASS_REQUIRED"])

        lower_user = _username.lower()
        if User.query.filter(func.lower(User.username) == lower_user).first() is None: # noqa
            raise UserDoesNotExistException(ERRORS["USER_DOES_NOT_EXISTS"])
