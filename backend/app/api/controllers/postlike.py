from app.api.models.models import Logs
from app.constant import custom_exceptions as ce
from app.constant.errors import ERRORS
from config.logger_handler import logger
from flask import Blueprint, request
from flask.views import MethodView
from marshmallow import ValidationError
from serializers.serializers import PostLikeSchema
from app.api.services.postlike import PostLikeDislike

postlike_schema = PostLikeSchema()


class PostLikeAPI(MethodView):

    # Post request to like dislike the post
    def post(self):
        try:

            validated_data = postlike_schema.load(request.json)

            return postlike_schema.dump(
                PostLikeDislike(
                    validated_data).post_like_dislike_process()), 200

        except ValidationError as valerror:
            return str(valerror), 400
        except ce.PostNotFoundException as postnotfound:
            return postnotfound.message, 404
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


# Create the blueprint for post like dislike api
post_like_bp = Blueprint(
    "liked_dislike", __name__,
    url_prefix='/api/v1/postlike')

post_like_bp.add_url_rule(
    '/',
    view_func=PostLikeAPI.as_view('postlikedislike'))
