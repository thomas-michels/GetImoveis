import pytest
from unittest.mock import AsyncMock
from app.core.db.repositories.neighborhood_repository import NeighborhoodRepository
from app.core.entities import NeighborhoodInDB, Neighborhood
from tests.core.db import mock_connection

@pytest.fixture
def neighborhood_repository(mock_connection):
    conn = NeighborhoodRepository(connection=mock_connection)
    conn.execute = AsyncMock()
    return conn

@pytest.mark.asyncio
async def test_insert(neighborhood_repository):
    payload = {
        "id": 1,
        "name": "Neighborhood 1",
        "population": 123,
        "houses": 1,
        "area": 12
    }

    neighborhood_repository.conn.execute.return_value = payload

    neighbor = Neighborhood(**payload)

    result = await neighborhood_repository.insert(neighbor)

    assert isinstance(result, NeighborhoodInDB)
    assert result.name == "Neighborhood 1"

@pytest.mark.asyncio
async def test_select_by_id_found(neighborhood_repository):
    neighborhood_repository.conn.execute.return_value = {
        "id": 1,
        "name": "Neighborhood 1",
        "population": 123,
        "houses": 1,
        "area": 12
    }

    result = await neighborhood_repository.select_by_id(1)

    assert isinstance(result, NeighborhoodInDB)
    assert result.id == 1

@pytest.mark.asyncio
async def test_select_by_id_not_found(neighborhood_repository):
    neighborhood_repository.conn.execute.return_value = None

    result = await neighborhood_repository.select_by_id(999)

    assert result is None

@pytest.mark.asyncio
async def test_select_by_name_found(neighborhood_repository):
    neighborhood_repository.conn.execute.return_value = {
        "id": 1,
        "name": "Neighborhood 1",
        "population": 123,
        "houses": 1,
        "area": 12
    }

    result = await neighborhood_repository.select_by_name("Neighborhood 1")

    assert isinstance(result, NeighborhoodInDB)
    assert result.name == "Neighborhood 1"

@pytest.mark.asyncio
async def test_select_by_name_not_found(neighborhood_repository):
    neighborhood_repository.conn.execute.return_value = None

    result = await neighborhood_repository.select_by_name("Nonexistent Neighborhood")

    assert result is None
