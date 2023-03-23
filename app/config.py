from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    SNAPSHOT_CHUNK_SIZE: int = 4 * 1024
    SNAPSHOT_FILENAME: str = 'resources/snapshot.zip'
    SNAPSHOT_GENERATION_TIME: int = 30

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_SNAPSHOT_KEY: str = 'snapshot:{}'


@lru_cache
def get_settings() -> Settings:
    return Settings()
