import http

from db import db
from flask_restful import Resource, reqparse
from models.user import User
from models.role import UserRoles, BaseRoles


class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str, help="This field cannot be blank", required=True, trim=True)
    parser.add_argument("password", help="This field cannot be blank", required=True)

    def post(self):
        """
        Registration method for users
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: UserRegistration
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  description: The user's email.
                  default: "test@test.com"
                password:
                  type: string
                  description: The user's password.
                  default: "test123"
        responses:
          201:
            description: Message that user was created
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
                    default: ...
                  default: []
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
                errors:
                  type: array
                  description: Data with error validation messages
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
        """
        data = self.parser.parse_args()
        email: str = data.get("email")
        password: str = data.get("password")
        if User.find_by_email(email):
            return {
                "message": "wrong data",
                "errors": [
                    {"username": f"User {email} already exists"},
                ],
            }, http.HTTPStatus.BAD_REQUEST
        new_user = User(email=email)
        new_user.set_password(password=password)
        db.session.add(new_user)
        db.session.commit()
        UserRoles.assign_user_role(new_user.id, BaseRoles.regular.value)
        return {"message": f"User {email} was created"}, http.HTTPStatus.CREATED
