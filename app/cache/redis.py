from typing import Any
from redis import Redis
import json


class RedisCacheBackend:
    def __init__(self, redis_url : str, cache_ttl:int):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.cache_ttl = cache_ttl
    
    def set(self, key: str, value: Any) -> None:
        self.redis.set(key, json.dumps(value), ex=self.cache_ttl)

    def get(self, key: str) -> Any | None:
        data = self.redis.get(key)
        if data is None:
            return None  
        return json.loads(data)

    def delete(self, key: str) -> int:
        return self.redis.delete(key)