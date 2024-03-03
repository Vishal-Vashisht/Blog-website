from datetime import datetime, timezone
from typing import Any, Dict

from app.api.models.models import TokenBlocklist, User
from app.constant.custom_exceptions import InvvalidCredException
from app.constant.errors import ERRORS
from app.utils.common_utils import SericeHelper
from flask import jsonify
from flask_jwt_extended import (create_access_token, set_access_cookies,
                                unset_jwt_cookies)
from werkzeug.security import check_password_hash, generate_password_hash


class RegisterUser():
    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the RegisterUser object with username and password.

        Args:
            data (dict): A dictionary containing user data with keys "username" and "password".
        """ # noqa
        self.username = data.get("username")
        self.password = data.get("password")

    def create_user(self) -> Dict[str, Any]:
        """
        Create a new user.

        Returns:
            dict: A dictionary containing information about the newly created user.
        """ # noqa
        try:
            new_user = User.create_new_user(
                self.username, generate_password_hash(
                    self.password))
            return {"data": [{"Username": new_user.username}]}
        except Exception as e:
            raise e


class LoginUser(SericeHelper):
    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the LoginUser object with username and password.

        Args:
            data (dict): A dictionary containing user data with keys "username" and "password".
        """ # noqa
        self.username = data.get("username")
        self.password = data.get("password")

    def login(self) -> jsonify:
        """
        Authenticate user login and generate access token.

        Returns:
            jsonify: A JSON response containing login status and access token.
        """ # noqa
        try:

            user = super().is_user_exists(self.username)
            # print(type(user.password.encode('utf-8')))

            if check_password_hash(user.password, self.password):
                additional_claims = {"username": self.username}
                access_token = create_access_token(
                    identity=user.users_id,
                    additional_claims=additional_claims)
                response = jsonify({"data": [{"username": self.username,
                                              "login": True}]})
                set_access_cookies(response, access_token)
                return response
            else:
                raise InvvalidCredException(ERRORS["INVALID_CREDNTIALS"])

        except Exception as e:
            raise e


class LogoutUser():
    def __init__(self, jti: str) -> None:
        """
        Initialize the LogoutUser object with jti (JWT ID).

        Args:
            jti (Union[str, int]): The JWT ID to be revoked.
        """ # noqa
        self.jti = jti

    def logout_user(self) -> jsonify:
        """
        Revoke JWT and log out the user.

        Returns:
            jsonify: A JSON response indicating successful logout.
        """
        try:
            now = datetime.now(timezone.utc)
            TokenBlocklist.insert_revoked_jti(self.jti, now)
            response = jsonify({"msg": "JWT revoked", 'login': False})
            unset_jwt_cookies(response)
            return response
        except Exception as e:
            raise e
