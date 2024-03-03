from app.api.models.models import Logs
from app.api.services.comments import (CommentCreate, CommentDelete,
                                       CommentUpdate)
from app.constant.errors import ERRORS
from config.logger_handler import logger
from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from serializers.serializers import (CommentDeleteSchema, CommentSchema,
                                     CommentUpdateSchema)

comment_schema = CommentSchema()
comment_delete_schema = CommentDeleteSchema()
comment_update_schema = CommentUpdateSchema()


class CommentsAPI(MethodView):

    decorators = [jwt_required()]

    def post(self):
        """
        Handle POST request for creating comments.

        Returns:
            tuple: A tuple containing response data and status code.
        """
        try:

            validated_data = comment_schema.load(request.get_json())

            return comment_schema.dump(
                CommentCreate(
                    validated_data, get_jwt_identity).process_comment()), 201

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
            validated_data = comment_update_schema.load(request.get_json())

            return comment_update_schema.dump(
                CommentUpdate(
                    validated_data).update_comment()
                ), 200
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

    def delete(self, comment_id):
        """
        Handle DELETE request for creating comments.

        Returns:
            tuple: A tuple containing response data and status code.
        """
        try:
            data = {"comment_id": comment_id}
            validated_data = comment_delete_schema.load(data)

            return comment_delete_schema.dump(
                CommentDelete(
                    validated_data).delete_comment()
                ), 403
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


# Create the blueprint
commnet_bp = Blueprint("comments", __name__, url_prefix='/api/v1/comment')

commnet_bp.add_url_rule("/", view_func=CommentsAPI.as_view('comments'))
commnet_bp.add_url_rule("/delete/<int:comment_id>",
                        view_func=CommentsAPI.as_view('commentsdelete'))
