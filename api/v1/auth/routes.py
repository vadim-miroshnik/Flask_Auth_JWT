from re import I
from . import api
from .login import UserLogin
from .logout import UserLogoutAccess, UserLogoutRefresh
from .refresh import TokensRefresh
from .registration import UserRegistration
from .history import LoginHistory
from .role import RoleCRUD, UserRoleCRUD
from .profile import Profile
from .authorization import Authorization

api.add_resource(UserRegistration, "/registration")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogoutAccess, "/logout/access")
api.add_resource(UserLogoutRefresh, "/logout/refresh")
api.add_resource(TokensRefresh, "/refresh")
api.add_resource(Profile, "/profile")
api.add_resource(LoginHistory, "/history")
api.add_resource(RoleCRUD, "/roles")
api.add_resource(UserRoleCRUD, "/user_roles")
api.add_resource(Authorization, "/authorization")
