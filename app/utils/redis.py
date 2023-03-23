from functools import lru_cache

from fastapi import Depends
from redis.asyncio.client import Redis

from config import Settings
from config import get_settings


@lru_cache
def create_redis(host: str, port: int) -> Redis:
    return Redis(host=host, port=port, encoding='utf-8', decode_responses=True)


def get_redis(settings: Settings = Depends(get_settings)) -> Redis:
    return create_redis(settings.REDIS_HOST, settings.REDIS_PORT)
