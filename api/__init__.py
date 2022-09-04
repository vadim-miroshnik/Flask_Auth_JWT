import http
from functools import wraps

from core import config
from db import cache, db, db_url
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import (JWTManager, get_jwt_identity,
                                verify_jwt_in_request)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_restful import Api
from models.role import BaseRoles, UserRoles

ma = Marshmallow()
api = Api()
jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload) -> bool:
    access = jwt_payload.get("type")
    if access == "access":
        return cache.is_token_blacklisted(jwt_payload["jti"])
    else:
        return False


def is_admin_permissions():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id: str = get_jwt_identity()
            if UserRoles.is_exists_user_role(user_id, BaseRoles.superuser.value):
                return func(*args, **kwargs)
            else:
                return {
                    "message": "permission error",
                    "description": "Only for users, who has 'admin' role!",
                    "errors": [],
                }, http.HTTPStatus.FORBIDDEN

        return decorator

    return wrapper


def create_app():
    app = Flask(__name__)
    limiter = Limiter(
        app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"]
    )

    swagger = Swagger(
        app,
        template={
            "swagger": "2.0",
            "info": {
                "title": "Auth service",
                "version": "1.0",
            },
            "consumes": [
                "application/json",
            ],
            "produces": [
                "application/json",
            ],
            "components": {
                "securitySchemes": {
                    "JWTAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                        "description": "Example: \n> Authorization: Bearer <token>",
                    }
                },
            },
            "security": [{"JWTAuth": []}],
        },
    )

    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.JWT_REFRESH_TOKEN_EXPIRES
    app.config["JWT_BLACKLIST_ENABLED"] = config.JWT_BLACKLIST_ENABLED
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"]: list = ["access", "refresh"]
    app.config["SWAGGER"] = {
        "title": "Swagger JWT Authentiation App",
        "uiversion": 3,
        "openapi": "3.0.3",
    }
    app.config["SQLALCHEMY_DATABASE_URI"]: str = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]: bool = False

    db.init_app(app=app)
    from .v1.auth import api_bp_auth

    ma.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(api_bp_auth)
    return app
