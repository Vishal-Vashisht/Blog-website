from app.api.models.models import Logs
from app.api.services.auth import LoginUser, LogoutUser, RegisterUser
from app.constant.custom_exceptions import (InvvalidCredException,
                                            UserDoesNotExistException,
                                            UserExistException)
from app.constant.errors import ERRORS
from config.logger_handler import logger
from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from marshmallow import ValidationError
from serializers.serializers import LoginSchema, RegisterSchema

# from flask import request

register_schema = RegisterSchema()
login_schema = LoginSchema()


class RegisterAPI(MethodView):

    def post(self):
        """
        Handle POST request for user registration.

        Returns:
            tuple: A tuple containing response data, status code, and headers.
        """
        try:
            # POST request handling logic goes here
            # Validation of the data
            validated_data = register_schema.load(request.get_json())
            return (
                register_schema.dump(RegisterUser(
                    validated_data).create_user()),
                201,
            )

        except ValidationError as valerror:
            # Return validation error with status code 400
            return str(valerror), 400
        except UserExistException as userexist:
            return userexist.messgae, 409
        except Exception as e:
            try:
                # Attempt to log the error
                Logs.create_log(str(e))

            except Exception as log_error:
                logger.exception(str(log_error))
                # If logging fails, return internal server error
                return ERRORS["INTERNAL_SERVER_ERROR"], 500
            # Return internal server error if logging succeeds
            logger.exception(str(e))
            return ERRORS["INTERNAL_SERVER_ERROR"], 500


class LoginAPI(MethodView):
    def post(self):
        """
        Handle POST request for user login.

        Returns:
            tuple: A tuple containing response data and status code.
        """
        try:
            # POST request handling logic goes here
            # Validation of the data
            validated_data = login_schema.load(request.get_json())
            return (LoginUser(validated_data).login(), 200)

        except ValidationError as valerror:
            # Return validation error with status code 400
            return str(valerror), 400
        except InvvalidCredException as Invlaidcred:
            return Invlaidcred.messgae, 401
        except UserDoesNotExistException as usernotexist:
            return usernotexist.messgae, 404
        except Exception as e:
            try:
                # Attempt to log the error
                Logs.create_log(str(e))

            except Exception as log_error:
                logger.exception(str(log_error))
                # If logging fails, return internal server error
                return ERRORS["INTERNAL_SERVER_ERROR"], 500
            # Return internal server error if logging succeeds
            logger.exception(str(e))
            return ERRORS["INTERNAL_SERVER_ERROR"], 500


class LogoutAPI(MethodView):

    decorators = [jwt_required()]

    def post(self):
        """
        Handle POST request for user logout.

        Returns:
            tuple: A tuple containing response data and status code.
        """
        try:
            jti = get_jwt()['jti']
            return LogoutUser(jti).logout_user()
        except Exception as e:
            try:
                # Attempt to log the error
                Logs.create_log(str(e))

            except Exception as log_error:
                logger.exception(str(log_error))
                # If logging fails, return internal server error
                return ERRORS["INTERNAL_SERVER_ERROR"], 500
            # Return internal server error if logging succeeds
            logger.exception(str(e))
            return ERRORS["INTERNAL_SERVER_ERROR"], 500


# Register the blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
auth_bp.add_url_rule("/register/", view_func=RegisterAPI.as_view("Registerapi")) # noqa
auth_bp.add_url_rule("/login/", view_func=LoginAPI.as_view("Loginapi"))
auth_bp.add_url_rule("/logout/", view_func=LogoutAPI.as_view("Logoutapi"))
