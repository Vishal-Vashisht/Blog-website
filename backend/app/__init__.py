from app.api.controllers.post import post_bp
from app.api.controllers.postlike import post_like_bp
from app.api.controllers.auth import auth_bp
from app.api.models.models import Migrations, db, migrate
from config.redis_config import redis_client
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from serializers.serializers import ma


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.dev")
    redis_client.init_app(app)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    JWTManager(app)

    # resgister blueprint
    app.register_blueprint(post_bp)
    app.register_blueprint(post_like_bp)
    app.register_blueprint(auth_bp)

    # Register a command to created the table in database
    with app.app_context():
        @app.cli.command('create-db')
        def create_db():
            Migrations()

    return app
