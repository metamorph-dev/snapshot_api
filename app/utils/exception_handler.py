from functools import wraps
from typing import Callable

from fastapi import HTTPException

from exceptions.snapshot_not_found import SnapshotNotFound


def handle_exceptions():
    def wrapper(func: Callable):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except SnapshotNotFound:
                raise HTTPException(404, 'Snapshot not found')

        return wrapped

    return wrapper
