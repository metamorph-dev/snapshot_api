import aiofiles
from fastapi import Depends
from redis.asyncio.client import Redis

from config import Settings
from config import get_settings
from utils.redis import get_redis


class SnapshotChunkingService:
    def __init__(self, settings: Settings, redis: Redis) -> None:
        self._settings = settings
        self._redis = redis

    async def execute(self):
        async with aiofiles.open(self._settings.SNAPSHOT_FILENAME, 'rb') as file:
            while chunk := await file.read(self._settings.SNAPSHOT_CHUNK_SIZE):
                yield chunk


def get_snapshot_chunking_service(
        settings: Settings = Depends(get_settings),
        redis: Redis = Depends(get_redis),
) -> SnapshotChunkingService:
    return SnapshotChunkingService(settings, redis)
