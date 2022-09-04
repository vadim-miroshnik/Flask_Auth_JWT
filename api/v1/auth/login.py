import http
from datetime import datetime
from typing import Any, Union

import jwt
from core import config
from db import cache, db
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from models.history import History
from models.user import User


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", help="This field cannot be blank", required=True)
    parser.add_argument("password", help="This field cannot be blank", required=True)

    def post(self):
        """
        Login method for users
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: UserLogin
              required:
                - username
                - password
              properties:
                username:
                  type: string
                  description: The user's username.
                  default: "JohnDoe"
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
        responses:
          200:
            description: Success user's login
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: True
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                    properties:
                      access_token:
                        type: string
                      refresh_token:
                        type: string
                message:
                  type: string
                  description: Response message
          400:
            description: Bad request response
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
        """
        data = self.parser.parse_args()
        email: str = data["email"]
        current_user = User.find_by_email(email)
        if not current_user:
            return {"message": f"User {email} doesn't exist"}, http.HTTPStatus.NOT_FOUND

        if current_user.check_password(password=data.get("password")):
            acc_token: str = create_access_token(identity=current_user.id)
            ref_token: str = create_refresh_token(identity=current_user.id)
            jti: Union[str, Any] = jwt.decode(
                jwt=ref_token, key=config.JWT_SECRET_KEY, algorithms="HS256"
            ).get("jti")
            cache.add_token(
                key=jti, expire=config.JWT_REFRESH_TOKEN_EXPIRES, value=current_user.id
            )
            history = History(
                user_id=current_user.id,
                description=f"Device: {request.user_agent.string} Login date: {datetime.now()}",
            )
            db.session.add(history)
            db.session.commit()
            return {
                "message": f"Logged in as {current_user.email}",
                "access_token": acc_token,
                "refresh_token": ref_token,
            }, http.HTTPStatus.OK
        return {"message": "Wrong credentials"}, http.HTTPStatus.BAD_REQUEST
