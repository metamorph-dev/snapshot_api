from os import PathLike

from pydantic import BaseSettings


class Settings(BaseSettings):
    snapshot_chunk_size_in_bytes: int = 4 * 1024
    snapshot_filename: str | bytes | PathLike = 'resources/snapshot.zip'
    snapshot_generation_time_in_seconds: int = 30

    redis_url: str
    redis_port: int
    redis_snapshot_ids_key: str = 'snapshot_ids'
