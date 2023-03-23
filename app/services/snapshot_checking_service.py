from fastapi import Depends
from redis.asyncio.client import Redis

from config import Settings
from config import get_settings
from exceptions.snapshot_not_found import SnapshotNotFound
from utils.redis import get_redis


class SnapshotCheckingService:
    """Fake snapshot checking service"""

    def __init__(self, settings: Settings, redis: Redis) -> None:
        self._settings = settings
        self._redis = redis

    async def execute(self, snapshot_id: str) -> bool:
        snapshot_key = self._settings.REDIS_SNAPSHOT_KEY.format(snapshot_id)

        result = await self._redis.get(snapshot_key)
        if result is None:
            raise SnapshotNotFound

        return result != ''


def get_snapshot_checking_service(
        settings: Settings = Depends(get_settings),
        redis: Redis = Depends(get_redis),
) -> SnapshotCheckingService:
    return SnapshotCheckingService(settings, redis)
