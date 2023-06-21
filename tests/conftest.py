import asyncio
from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from main import app as main_app
from services.snapshot_checking_service import get_snapshot_checking_service
from services.snapshot_chunking_service import get_snapshot_chunking_service
from services.snapshot_generation_service import get_snapshot_generation_service


@pytest.fixture(scope='session')
def app():
    async def mock_get_snapshot_checking_service() -> Mock:
        mock = AsyncMock()
        mock.execute.return_value = True
        return mock

    async def mock_get_snapshot_chunking_service() -> Mock:
        async def execute():
            yield b'qwerty'

        mock = AsyncMock()
        mock.execute = execute
        return mock

    main_app.dependency_overrides[get_snapshot_generation_service] = lambda: Mock()
    main_app.dependency_overrides[get_snapshot_checking_service] = mock_get_snapshot_checking_service
    main_app.dependency_overrides[get_snapshot_chunking_service] = mock_get_snapshot_chunking_service

    return main_app


@pytest_asyncio.fixture(scope="module")
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest_asyncio.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
