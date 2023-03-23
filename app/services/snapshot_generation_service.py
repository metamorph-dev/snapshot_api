import asyncio

from fastapi import Depends
from redis.asyncio.client import Redis

from config import Settings
from config import get_settings
from utils.redis import get_redis


class SnapshotGenerationService:
    """Fake snapshot generation service"""

    def __init__(self, settings: Settings, redis: Redis) -> None:
        self._settings = settings
        self._redis = redis

    async def execute(self, snapshot_id: str) -> None:
        snapshot_key: str = self._settings.REDIS_SNAPSHOT_KEY.format(snapshot_id)
        await self._redis.set(snapshot_key, '')
        await asyncio.sleep(self._settings.SNAPSHOT_GENERATION_TIME)
        await self._redis.set(snapshot_key, '1')


def get_snapshot_generation_service(
        settings: Settings = Depends(get_settings),
        redis: Redis = Depends(get_redis),
) -> SnapshotGenerationService:
    return SnapshotGenerationService(settings, redis)
