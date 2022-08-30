import enum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, Index

from db import db
from .mixins import IdCreatedUpdatedMixin


class BaseRoles(enum.Enum):
    superuser = 'superuser'
    admin = 'admin'
    regular = 'regular'
    subscriber = 'subscriber'
    guest = 'guest'


class Role(db.Model):
    __tablename__ = "roles"
    __table_args__ = {"schema": "auth"}

    name = db.Column(db.String(length=64), primary_key=True)

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    def get_detailed(self):
        right = func.jsonb_build_object(
            "url",
            RoleRights.url,
            "param_name",
            RoleRights.param_name,
            "param_value",
            RoleRights.param_value
        )
        rights = func.coalesce(func.json_agg(right, distinct=True).filter(RoleRights.role != None), "[]")
        role_detailed = (
            db.session.query(Role.name, rights)
            .outerjoin(RoleRights, Role.name == RoleRights.role)
            .filter(Role.name == self.name)
            .group_by(Role.name)
            .first()
        )
        return {"role": role_detailed[0], "rights": role_detailed[1]}

    @classmethod
    def get_all_roles_detailed(cls):
        right = func.jsonb_build_object(
            "url",
            RoleRights.url,
            "param_name",
            RoleRights.param_name,
            "param_value",
            RoleRights.param_value
        )
        rights = func.coalesce(func.json_agg(right, distinct=True).filter(RoleRights.role != None), "[]")
        queryset = (
            db.session.query(cls.name, rights).outerjoin(RoleRights, Role.name == RoleRights.role).group_by(cls.name)
        )
        results = []
        for role in queryset:
            results.append({"role": role[0], "rights": role[1]})
        return results


class RoleRights(IdCreatedUpdatedMixin):
    __tablename__ = "roles_rights"
    __table_args__ = {"schema": "auth"}

    role = db.Column(db.String(length=64), db.ForeignKey("auth.roles.name", ondelete="CASCADE"), nullable=False)
    url = db.Column(db.Text, nullable=False)
    param_name = db.Column(db.String(length=128))
    param_value = db.Column(db.String(length=128))

    @classmethod
    def get_by_role_and_url(cls, role, url):
        return cls.query.filter_by(role=role, url=url).first()


class UserRoles(IdCreatedUpdatedMixin):
    __tablename__ = "users_roles"
    __table_args__ = {"schema": "auth"}

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("auth.users.id", ondelete="CASCADE"), nullable=True)
    role = db.Column(db.String(length=64), db.ForeignKey("auth.roles.name", ondelete="CASCADE"), nullable=False)

    @classmethod
    def is_exists_user_role(cls, user_id, role):
        obj = cls.query.filter_by(user_id=user_id, role=role).first()
        return obj is not None

    @classmethod
    def assign_user_role(cls, user_id, role):
        new_user_role = cls(user_id=user_id, role=role)
        db.session.add(new_user_role)
        db.session.commit()

    @classmethod
    def get_user_roles_detailed(cls, user_id):
        right = func.jsonb_build_object(
            "url",
            RoleRights.url,
            "param_name",
            RoleRights.param_name,
            "param_value",
            RoleRights.param_value
        )
        rights = func.coalesce(func.json_agg(right, distinct=True).filter(RoleRights.role != None), "[]")
        queryset = (
            db.session.query(cls.role, rights)
            .outerjoin(RoleRights, cls.role == RoleRights.role)
            .filter(cls.user_id == user_id)
            .group_by(cls.user_id, cls.role)
        )
        results = []
        for role in queryset:
            results.append({"role": role[0], "rights": role[1]})
        return results
