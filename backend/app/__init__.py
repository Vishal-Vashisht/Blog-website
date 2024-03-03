import os

from app.api.controllers.auth import auth_bp
from app.api.controllers.post import post_bp
from app.api.controllers.postlike import post_like_bp
from app.api.controllers.comments import commnet_bp
from app.api.models.models import Migrations, db, migrate
from app.utils.jwt_utils import (check_if_token_in_block_list,
                                 expired_token_callback,
                                 invalid_token_callback, refresh_expiring_jwts,
                                 unauthorized_token_callback)
from config.redis_config import redis_client
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from serializers.serializers import ma

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"config.{os.environ.get("environment")}")
    redis_client.init_app(app)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt = JWTManager(app)
    # Token authentication
    jwt.token_in_blocklist_loader(check_if_token_in_block_list)
    jwt.expired_token_loader(expired_token_callback)
    jwt.invalid_token_loader(invalid_token_callback)
    jwt.unauthorized_loader(unauthorized_token_callback)

    # resgister blueprint
    app.register_blueprint(post_bp)
    app.register_blueprint(post_like_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(commnet_bp)

    # Register a command to created the table in database
    with app.app_context():
        @app.cli.command('create-db')
        def create_db():
            Migrations()

        @app.after_request
        def refresh_exp_jwt(response):
            return refresh_expiring_jwts(response)

    return app
