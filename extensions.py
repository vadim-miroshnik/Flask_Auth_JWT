from flask_jwt_extended import JWTManager

from db import cache

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload) -> bool:
    access = jwt_payload.get("type")
    if access == "access":
        return cache.is_token_blacklisted(jwt_payload["jti"])
    else:
        return False
