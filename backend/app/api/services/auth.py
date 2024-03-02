from werkzeug.security import generate_password_hash, check_password_hash
from app.api.models.models import User
from flask_jwt_extended import create_access_token, set_access_cookies
from app.utils.common_utils import SericeHelper
from app.constant.custom_exceptions import InvvalidCredException
from app.constant.errors import ERRORS
from flask import jsonify


class RegisterUser():
    def __init__(self, data) -> None:
        self.username = data.get("username")
        self.password = data.get("password")

    def create_user(self):
        try:
            new_user = User.create_new_user(
                self.username, generate_password_hash(
                    self.password))
            return {"data": [{"Username": new_user.username}]}
        except Exception as e:
            raise e


class LoginUser(SericeHelper):
    def __init__(self, data) -> None:
        self.username = data.get("username")
        self.password = data.get("password")

    def login(self):
        try:

            user = super().is_user_exists(self.username)
            # print(type(user.password.encode('utf-8')))

            if check_password_hash(user.password, self.password):
                access_token = create_access_token(identity=self.username)
                response = jsonify({"data": [{"username": self.username,
                                              "login": True}]})
                set_access_cookies(response, access_token)
                return response
            else:
                raise InvvalidCredException(ERRORS["INVALID_CREDNTIALS"])

        except Exception as e:
            raise e
