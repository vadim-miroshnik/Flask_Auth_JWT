from abc import ABC, abstractmethod
from typing import Union


class Cache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    def add_token(self, key: str, expire: int, value: Union[bytes, str]):
        pass

    @abstractmethod
    def delete_token(self, key: str):
        pass

    @abstractmethod
    async def is_token_blacklisted(self, jti):
        pass
