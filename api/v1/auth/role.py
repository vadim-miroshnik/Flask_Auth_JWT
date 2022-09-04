import http
import uuid

from api import is_admin_permissions
from db import db
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.role import Role, RoleRights, UserRoles
from models.user import User
from pydantic import BaseModel, Field
from pydantic.schema import Optional


class Right(BaseModel):
    url: str
    param_name: Optional[str]
    param_value: Optional[str]


class EditRole(BaseModel):
    role: str
    deleted: bool = Field(default=False)


class RoleCRUD(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("role", type=str, help="Input role name", required=False)
    parser.add_argument(
        "rights", type=dict, required=False, action="append", default=[]
    )
    parser.add_argument("deleted", type=bool, required=False, default=False)

    def post(self):
        """
        Role CRUD method
        ---
        tags:
          - role
        parameters:
          - in: body
            name: body
            schema:
              id: RoleCRUD
              properties:
                role:
                  type: string
                  description: role
                rights:
                  type: list[Right]
                  description: The role's rights.
        responses:
          201:
            description: Message that role was created
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
        role = data.get("role")
        if not role:
            all_roles = Role.get_all_roles_detailed()
            return {"roles": all_roles}, http.HTTPStatus.OK
        role_object = Role.find_by_name(role)
        if data.get("deleted"):
            if not role_object:
                return {
                    "message": f"Can't delete: role {role} not found"
                }, http.HTTPStatus.NOT_FOUND
            Role.query.filter(Role.name == role).delete()
            db.session.commit()
            return {
                "message": f"Role {role} was successfully deleted"
            }, http.HTTPStatus.OK
        if not role_object:
            role_object = Role(name=role)
            db.session.add(role_object)
            message = f"Role {role} was successfully created"
        else:
            message = f"Role {role} was successfully updated"
        for right in data.get("rights"):
            deleted = right.pop("deleted", False)
            validated_right = Right.parse_obj(right)
            if deleted:
                db.session.query(RoleRights).delete().where(
                    RoleRights.role == role and RoleRights.url == validated_right.url
                )
                continue
            right_object = RoleRights.get_by_role_and_url(role, validated_right.url)
            if right_object:
                right_object.param_name = validated_right.param_name
                right_object.param_value = validated_right.param_value
            else:
                right_object = RoleRights(role=role, **dict(validated_right))
                db.session.add(right_object)
        db.session.commit()
        response = role_object.get_detailed()
        return {"message": message, "result": response}, http.HTTPStatus.CREATED


class UserRoleCRUD(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("user_id", type=uuid.UUID, help="Input user_id", required=False)
    parser.add_argument("email", type=str, help="Input user email", required=False)
    parser.add_argument("roles", type=dict, required=False, action="append")

    @jwt_required()
    @is_admin_permissions()
    def post(self):
        """
        User role CRUD method
        ---
        tags:
          - role
        parameters:
          - in: body
            name: body
            schema:
              id: UserRoleCRUD
              properties:
                user_id:
                  type: string
                  description: user_id
                email:
                  type: string
                  description: user email
                roles:
                  type: list[EditRole]
                  description: The user's roles
        responses:
          201:
            description: Message that user roles was updated
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
        user_id = data.get("user_id")
        if not user_id:
            if not data.get("email"):
                return {
                    "message": "Required one of this fields: user_id or email"
                }, http.HTTPStatus.BAD_REQUEST
            user_id = User.find_by_email(data.get("email")).id
        user = User.query.get(user_id)
        if not user:
            return {
                "message": f"User id {user_id} not found"
            }, http.HTTPStatus.NOT_FOUND
        if not data.get("roles"):
            user_roles = UserRoles.get_user_roles_detailed(user_id)
            return {
                "message": f"User id {user_id} roles and rights",
                "roles": user_roles,
            }, http.HTTPStatus.OK
        for role in data.get("roles"):
            validated_role = EditRole.parse_obj(role)
            role_object = Role.query.get(validated_role.role)
            if not role_object:
                return {
                    "message": f"Role {validated_role.role} is not exists"
                }, http.HTTPStatus.NOT_FOUND
            if validated_role.deleted:
                db.session.query(UserRoles).delete().where(
                    UserRoles.user_id == user_id
                    and UserRoles.role == validated_role.role
                )
            else:
                if UserRoles.is_exists_user_role(user_id, validated_role.role):
                    continue
                new_user_role = UserRoles(user_id=user_id, role=validated_role.role)
                db.session.add(new_user_role)
        db.session.commit()
        response = UserRoles.get_user_roles_detailed(user_id)
        return {
            "message": f"User roles for user id {user_id} are successfully updated",
            "result": response,
        }, http.HTTPStatus.CREATED
