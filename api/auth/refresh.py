import http

from db import cache
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_restful import Resource


class TokensRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh token method for users
        ---
        tags:
          - user
        responses:
          200:
            description: Success user's token refresh
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
          401:
            description: Authorization error response
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                errors:
                  type: array
                  description: Response data
                  items:
                    type: object
                    default: ...
                  default: []
                description:
                  type: string
                  description: Response description
                message:
                  type: string
                  description: Response message
        """
        jti = get_jwt().get("jti")
        if cache.is_token_blacklisted(jti):
            user_id: str = get_jwt_identity()
            acc_token: str = create_access_token(user_id)
            ref_token: str = create_refresh_token(user_id)
            return {
                "success": True,
                "errors": [],
                "message": "Refreshed",
                "access_token": acc_token,
                "refresh_token": ref_token,
            }, http.HTTPStatus.OK
        return {
            "success": False,
            "errors": [],
            "message": "token revoked",
            "description": "The refresh token has been revoked.",
        }, http.HTTPStatus.UNAUTHORIZED
