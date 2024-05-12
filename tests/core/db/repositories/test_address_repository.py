import pytest
from app.core.db.repositories.address_repository import AddressRepository
from app.core.entities import PlainAddress
from tests.core.db import mock_connection


@pytest.fixture
def address_repository(mock_connection):
    return AddressRepository(connection=mock_connection)

@pytest.mark.asyncio
async def test_search_all(address_repository):
    address_repository.conn.execute.return_value = [
        {
            "neighborhood_id": 1,
            "neighborhood_name": "Neighborhood 1",
            "street_id": 1,
            "street_name": "Street 1",
            "zip_code": "12345-100",
            "flood_quota": None,
            "latitude": None,
            "longitude": None,
        },
        {
            "neighborhood_id": 2,
            "neighborhood_name": "Neighborhood 2",
            "street_id": 2,
            "street_name": "Street 2",
            "zip_code": "54321-100",
            "flood_quota": None,
            "latitude": None,
            "longitude": None,
        },
    ]

    result = await address_repository.search_all()

    assert len(result) == 2
    assert isinstance(result[0], PlainAddress)
    assert isinstance(result[1], PlainAddress)

@pytest.mark.asyncio
async def test_search_by_zip_code(address_repository):
    address_repository.conn.execute.return_value = {
        "neighborhood_id": 1,
        "neighborhood_name": "Neighborhood 1",
        "street_id": 1,
        "street_name": "Street 1",
        "zip_code": "12345-100",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }

    result = await address_repository.search_by_zip_code("12345-100")

    assert isinstance(result, PlainAddress)

@pytest.mark.asyncio
async def test_search_by_zip_code_not_found(address_repository):
    address_repository.conn.execute.return_value = None

    result = await address_repository.search_by_zip_code("99999-99")

    assert result is None

@pytest.mark.asyncio
async def test_search_by_street(address_repository):
    address_repository.conn.execute.return_value = {
        "neighborhood_id": 1,
        "neighborhood_name": "Neighborhood 1",
        "street_id": 1,
        "street_name": "Street 1",
        "zip_code": "12345-100",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }

    result = await address_repository.search_by_street("Street 1")

    assert isinstance(result, PlainAddress)

@pytest.mark.asyncio
async def test_search_by_street_not_found(address_repository):
    address_repository.conn.execute.return_value = None

    result = await address_repository.search_by_street("Nonexistent Street")

    assert result is None

@pytest.mark.asyncio
async def test_search_by_neighborhood(address_repository):
    address_repository.conn.execute.return_value = {
        "neighborhood_id": 1,
        "neighborhood_name": "Neighborhood 1",
        "street_id": None,
        "street_name": None,
        "zip_code": None,
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }

    result = await address_repository.search_by_neighborhood("Neighborhood 1")

    assert isinstance(result, PlainAddress)

@pytest.mark.asyncio
async def test_search_by_neighborhood_not_found(address_repository):
    address_repository.conn.execute.return_value = None

    result = await address_repository.search_by_neighborhood("Nonexistent Neighborhood")

    assert result is None
