import http

from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restful import Resource, reqparse
from models.role import UserRoles


class Authorization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", required=True)
    parser.add_argument("param_name", required=False)

    def get(self):
        """
        User's roles
        ---
        tags:
          - role
        responses:
          200:
            description: return user roles (guest for anonymous users)
            schema:
              properties:
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
        verify_jwt_in_request(optional=True, locations='headers')
        user_id: str = get_jwt_identity()
        return UserRoles.get_user_roles_detailed(user_id=user_id), http.HTTPStatus.OK

    def post(self):
        """
        User's roles and rights
        ---
        tags:
          - role
        parameters:
          - in: body
            name: body
            schema:
              id: Authorization
              properties:
                url:
                  type: string
                  description: service route url
                param_name:
                  type: string
                  description: a special parameter indicating any rights, e. g. subscription level
        responses:
          200:
            description: return param value and successful authorization status
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
          404:
            description: the necessary permissions were not found
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
        verify_jwt_in_request(optional=True)
        user_id: str = get_jwt_identity()
        roles = UserRoles.get_user_roles_detailed(user_id=user_id)

        data = self.parser.parse_args()
        url: str = data.get("url")
        param_name: str = data.get("param_name")

        for role in roles:
            for right in role.get("rights"):
                if url.startswith(right.get("url")) and param_name == right.get("param_name"):
                    return {"authorization": "passed", param_name: right.get("param_value")}, http.HTTPStatus.OK

        return {"authorization": "failed", "description": "insufficient privileges"}, http.HTTPStatus.NOT_FOUND

