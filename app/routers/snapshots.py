import asyncio
from uuid import uuid4 as uuid

import aiofiles
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from redis import asyncio as aioredis

from config import Settings

settings = Settings()

redis = aioredis.StrictRedis(host='redis', port=settings.redis_port, encoding='utf-8', decode_responses=True)


router = APIRouter(prefix='/snapshots', tags=['snapshots'])


class Snapshot(BaseModel):
    id: str
    ready: bool


@router.post('/', response_model=Snapshot)
async def create_snapshot(background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(__generate_snapshot, snapshot_id := str(uuid()))
    return {'id': snapshot_id, 'ready': False}


@router.get('/{snapshot_id}', response_model=Snapshot)
async def get_snapshot_info(snapshot_id: str) -> dict:
    return {'id': snapshot_id, 'ready': await __is_snapshot_ready(snapshot_id)}


@router.get('/{snapshot_id}/download')
async def download_snapshot(snapshot_id: str) -> StreamingResponse:
    is_ready = await __is_snapshot_ready(snapshot_id)
    if not is_ready:
        raise HTTPException(404, 'Snapshot not ready')

    async def iterate_snapshot():
        async with aiofiles.open(settings.snapshot_filename, 'rb') as file:
            while chunk := await file.read(
                settings.snapshot_chunk_size_in_bytes
            ):
                yield chunk

    return StreamingResponse(
        content=iterate_snapshot(),
        media_type='application/x-zip-compressed',
        headers={
            'Content-Disposition': f'attachment; filename=snapshot-{snapshot_id}.zip'
        },
    )


async def __generate_snapshot(snapshot_id: str) -> None:
    """Fake snapshot generation"""
    await redis.set(f'{settings.redis_snapshot_ids_key}:{snapshot_id}', '')
    await asyncio.sleep(settings.snapshot_generation_time_in_seconds)
    await redis.set(f'{settings.redis_snapshot_ids_key}:{snapshot_id}', '1')


async def __is_snapshot_ready(snapshot_id: str) -> bool:
    if not (await redis.exists(f'{settings.redis_snapshot_ids_key}:{snapshot_id}')):
        raise HTTPException(404, 'Snapshot not found')

    return await redis.get(f'{settings.redis_snapshot_ids_key}:{snapshot_id}') != ''
