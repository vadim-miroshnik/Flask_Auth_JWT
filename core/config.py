from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY: str = "jwt_secret"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_BLACKLIST_ENABLED: bool = True
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"

BASE_DIR: str = Path(__file__).resolve().parent.parent
