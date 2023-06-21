import pytest


@pytest.mark.asyncio
async def test_create(client):
    response = await client.post("/snapshots/")
    assert response.status_code == 200
    assert not response.json().get('ready')


@pytest.mark.asyncio
async def test_check_status(client):
    response = await client.get("/snapshots/qwerty/")
    assert response.status_code == 200
    assert response.json().get('ready')


@pytest.mark.asyncio
async def test_download(client):
    response = await client.get("/snapshots/qwerty/download/")
    assert response.status_code == 200
    assert response.read() == b'qwerty'
