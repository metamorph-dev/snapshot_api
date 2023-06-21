from uuid import uuid4

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from models import Snapshot
from services.snapshot_checking_service import SnapshotCheckingService
from services.snapshot_checking_service import get_snapshot_checking_service
from services.snapshot_chunking_service import SnapshotChunkingService
from services.snapshot_chunking_service import get_snapshot_chunking_service
from services.snapshot_generation_service import SnapshotGenerationService
from services.snapshot_generation_service import get_snapshot_generation_service
from utils.exception_handler import handle_exceptions

router = APIRouter(prefix='/snapshots', tags=['snapshots'])


@router.post('/', response_model=Snapshot)
async def create(
        background_tasks: BackgroundTasks,
        service: SnapshotGenerationService = Depends(get_snapshot_generation_service),
) -> dict:
    background_tasks.add_task(service.execute, snapshot_id := str(uuid4()))
    return {'id': snapshot_id}


@router.get('/{snapshot_id}/', response_model=Snapshot)
@handle_exceptions()
async def read(
        snapshot_id: str,
        service: SnapshotCheckingService = Depends(get_snapshot_checking_service),
) -> dict:
    return {'id': snapshot_id, 'ready': (await service.execute(snapshot_id))}


@router.get('/{snapshot_id}/download/')
@handle_exceptions()
async def download(
        snapshot_id: str,
        checking_service: SnapshotCheckingService = Depends(get_snapshot_checking_service),
        chunking_service: SnapshotChunkingService = Depends(get_snapshot_chunking_service),
) -> StreamingResponse:
    ready = await checking_service.execute(snapshot_id)
    if not ready:
        raise HTTPException(400, 'Snapshot not ready')

    return StreamingResponse(
        content=chunking_service.execute(),
        media_type='application/x-zip-compressed',
        headers={'Content-Disposition': f'attachment; filename=snapshot-{snapshot_id}.zip'},
    )
