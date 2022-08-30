import os

from flasgger import Swagger
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_restful import Api

from core import config
from db import db, db_url
from extensions import jwt

ma = Marshmallow()
api = Api()


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
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization"
                },
            },
            "securityRequirements": {
                "Bearer": ""
            },
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
    }
    app.config["SQLALCHEMY_DATABASE_URI"]: str = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]: bool = False

    db.init_app(app=app)
    from api.auth import api_bp_auth

    jwt.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    app.register_blueprint(api_bp_auth)
    return app


if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0", port=os.getenv("FLASK_PORT"))
