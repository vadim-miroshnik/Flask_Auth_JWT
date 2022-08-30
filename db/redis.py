import os
from typing import Union
from dotenv import load_dotenv

from db.cache import Cache
from redis import Redis

load_dotenv()

REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PORT: int = int(os.getenv("REDIS_PORT"))


class RedisCache(Cache):
    def add_token(self, key: str, expire: int, value: Union[bytes, str]):
        self.cache.setex(name=f"{key}", time=expire, value=f"{value}")

    def delete_token(self, key: str):
        self.cache.delete(f"{key}")

    def is_token_blacklisted(self, jti) -> bool:
        return bool(self.cache.get(name=jti))


redis_cache: RedisCache = RedisCache(
    cache_instance=Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True, charset="utf-8"
    )
)
