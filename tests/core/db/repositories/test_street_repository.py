import pytest
from app.core.db.repositories.street_repository import StreetRepository
from app.core.entities import StreetInDB, Street
from tests.core.db import mock_connection

@pytest.fixture
def street_repository(mock_connection):
    return StreetRepository(connection=mock_connection)

@pytest.mark.asyncio
async def test_insert(street_repository):
    
    street_repository.conn.execute.return_value = {
        "id": 1,
        "name": "Street 1",
        "neighborhood_id": 1,
        "zip_code": "12345-100",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }

    street = Street(
        name="Street 1",
        neighborhood_id=1,
        zip_code="12345-100",
        flood_quota=None,
        latitude=None,
        longitude=None,
    )

    result = await street_repository.insert(street)
    
    assert isinstance(result, StreetInDB)
    assert result.name == "Street 1"

@pytest.mark.asyncio
async def test_select_by_id_found(street_repository):
    
    street_repository.conn.execute.return_value = {
        "id": 1,
        "name": "Street 1",
        "neighborhood_id": 1,
        "zip_code": "12345-100",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }
    
    result = await street_repository.select_by_id(1)
    
    assert isinstance(result, StreetInDB)
    assert result.id == 1

@pytest.mark.asyncio
async def test_select_by_id_not_found(street_repository):
    
    street_repository.conn.execute.return_value = None

    result = await street_repository.select_by_id(999)
    
    assert result is None

@pytest.mark.asyncio
async def test_select_by_name_found(street_repository):
    
    street_repository.conn.execute.return_value = {
        "id": 1,
        "name": "Street 1",
        "neighborhood_id": 1,
        "zip_code": "12345-100",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }
    
    result = await street_repository.select_by_name("Street 1")

    assert isinstance(result, StreetInDB)
    assert result.name == "Street 1"

@pytest.mark.asyncio
async def test_select_by_name_not_found(street_repository):
    
    street_repository.conn.execute.return_value = None
    
    result = await street_repository.select_by_name("Nonexistent Street")
    
    assert result is None

@pytest.mark.asyncio
async def test_select_by_zip_code_found(street_repository):
    
    street_repository.conn.execute.return_value = {
        "id": 1,
        "name": "Street 1",
        "neighborhood_id": 1,
        "zip_code": "12345-100",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }
    
    result = await street_repository.select_by_zip_code("12345-100")
    
    assert isinstance(result, StreetInDB)
    assert result.zip_code == "12345-100"

@pytest.mark.asyncio
async def test_select_by_zip_code_not_found(street_repository):
    
    street_repository.conn.execute.return_value = None

    result = await street_repository.select_by_zip_code("99999-100")

    assert result is None
