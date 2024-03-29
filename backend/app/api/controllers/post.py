from app.api.models.models import Logs
from app.api.services.post import PostCreator, PostGetter, PostUpdate
from app.constant.errors import ERRORS
from config.logger_handler import logger
from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from serializers.serializers import PostsSchema, PostUpdateSchema

postschema = PostsSchema()
postupdateschema = PostUpdateSchema()


class PostAPI(MethodView):
    decorators = [jwt_required()]

    def get(self):
        """
        Handle Get request for creating comments.

        Returns:
            tuple: A tuple containing response data and status code.
        """
        try:
            PostGetter().process_all_posts()
            return (
                postschema.dump(PostGetter().process_all_posts()),
                200)

        except ValidationError as valerror:
            # Return validation error with status code 400
            return str(valerror), 400
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

    def post(self):
        """
        Handle POST request for creating comments.

        Returns:
            tuple: A tuple containing response data and status code.
        """
        try:
            # POST request handling logic goes here
            # Validation of the data
            validated_data = postschema.load(request.get_json())
            return (
                postschema.dump(PostCreator(
                    validated_data, get_jwt_identity).process_data()),
                201
                )

        except ValidationError as valerror:
            # Return validation error with status code 400
            return str(valerror), 400
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

    def patch(self):
        """
        Handle PATCH request for creating comments.

        Returns:
            tuple: A tuple containing response data and status code.
        """
        try:
            validated_data = postupdateschema.load(request.get_json())
            return (postupdateschema.dump(
                PostUpdate(validated_data).post_update()), 200)
        except ValidationError as valerror:
            # Return validation error with status code 400
            return str(valerror), 400
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


# Creating blueprint
post_bp = Blueprint(
    'post', __name__,
    url_prefix='/api/v1')

# URL to create, update, delete and get all the posts
post_bp.add_url_rule('/post/', view_func=PostAPI.as_view('postapi'))
