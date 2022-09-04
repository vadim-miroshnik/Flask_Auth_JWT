import http

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from db import db
from models.user import User


class Profile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email")
    parser.add_argument("password")

    @jwt_required()
    def get(self):
        """
        Get own profile method for users
        ---
        tags:
          - profile
        responses:
          200:
            description: 

          404:
            description: 

        """
        user_id: str = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user.email, http.HTTPStatus.OK
        return {"message": "error"}, http.HTTPStatus.NOT_FOUND

    @jwt_required()
    def patch(self):
        """
        Update profile method for users
        ---
        tags:
          - profile
        parameters:
          - in: body
            name: body
            schema:
              id: Profile
              properties:
                email:
                  type: string
                  description: The user's username.
                  default: "test@test.com"
        responses:
          200:
            description: Success

          400:
            description: Error
        """
        data = self.parser.parse_args()
        user_id: str = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        new_email: str = data.get("email")
        if new_email:
            user.email = new_email
        new_password: str = data.get("password")
        if new_password:
            user.set_password(password=new_password)
        try:
            db.session.add(user)
            db.session.commit()
            return new_email, http.HTTPStatus.OK
        except Exception:
            db.session.rollback()
            return {"message": "Something went wrong"}, http.HTTPStatus.BAD_REQUEST
